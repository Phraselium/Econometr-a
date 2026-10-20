#!/usr/bin/env python3
"""V15-B1 · Guardas PreToolUse para Bash. Lee el JSON del hook por la entrada estándar y sale con código 2 (bloquea, con el
motivo en stderr) si el comando:
  (a) usa un heredoc sin comillas («<<EOF» en lugar de «<<'EOF'»): el shell expandiría `…` y $(…) (incidente D3 de V13);
  (b) menciona la muestra sellada salvo a través de src/holdout.py;
  (c) lanza `make check` mientras ya hay uno en marcha (bloqueo /tmp/econometra_make_check.lock con su PID, o un proceso vivo);
  (d) lanza `make v15_f4*` o `make v15_f5*` sin la etiqueta prereg-v15 en el remoto apuntando a 542b4fd (V16: pre-registro
      interno sin sello externo; src/v16/etiquetas.py);
  (f) lanza `make v16_f5*`, `v16_f6*`, `v16_f7*` o `make v16` sin la etiqueta prereg-v16 en el remoto (V16);
  (g) lanza `make v18_f3` o posteriores, o `make v18`, sin la etiqueta local plan-replicacion-v18 con su commit en la rama
      remota (V18, B1; src/v18/etiqueta.py). El plan de la fase 3 se escribe y etiqueta antes; `make v18_f3` lo comprueba;
  (e) además de permissions.deny: make clean, make all, make v7, make evaluate_v7, git push --force/-f, git filter-repo,
      rm -rf data, rm -rf output (no cuenta el texto de un heredoc entrecomillado que solo escribe un fichero con cat o tee).
La regla (a) no mira el cuerpo de un heredoc ya entrecomillado (el shell no lo expande).
Uso como función: `evaluar(comando, raiz) -> motivo | None` (tests/v15/test_guardas.py).
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

LOCK = Path(os.environ.get("ECONOMETRA_LOCK_CHECK", "/tmp/econometra_make_check.lock"))
SELLADO = "data/" + "sealed"   # partido: este fichero no debe parecer un acceso
HEREDOC_SIN_COMILLAS = re.compile(r"(?<!<)<<-?\s*([A-Za-z_][A-Za-z0-9_]*)\b")
PROHIBIDOS = [
    (re.compile(r"\bmake\b[^;&|]*\s(clean|all)\b"), "make clean / make all están prohibidos sin orden expresa del autor"),
    (re.compile(r"\bmake\b[^;&|]*\s(v7|evaluate_v7)(\s|$|;|&|\|)"), "make v7 y make evaluate_v7 están prohibidos (evaluación de 2027)"),
    (re.compile(r"\bgit\s+push\b[^;&|]*\s(--force|-f)(\s|$|=)"), "git push --force está prohibido"),
    (re.compile(r"\bgit\s+filter-repo\b"), "git filter-repo está prohibido"),
    (re.compile(r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*f?[a-zA-Z]*\s+(\./)?(data|output)(/|\s|$)"), "rm -rf data / rm -rf output están prohibidos"),
]


def _vivo(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ValueError):
        return False


def _make_check_en_marcha() -> bool:
    if LOCK.exists():
        try:
            if _vivo(int(LOCK.read_text().split()[0])):
                return True
        except (ValueError, IndexError):
            pass
    if os.environ.get("ECONOMETRA_LOCK_SOLO_FICHERO"):
        return False
    for p in Path("/proc").glob("[0-9]*/cmdline"):
        try:
            c = p.read_bytes().replace(b"\0", b" ").decode(errors="ignore").strip()
        except OSError:
            continue
        if re.match(r"^make\s+(-\S+\s+)*check(\s|$)", c):
            return True
    return False


def _etiqueta_ok(raiz: Path, cual: str) -> bool:
    """V16: la puerta es una etiqueta de pre-registro interno publicada en el remoto (src/v16/etiquetas.py)."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("etiquetas_v16", raiz / "src" / "v16" / "etiquetas.py")
        e = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(e)
        return (e.prereg_v15_publicada if cual == "v15" else e.prereg_v16_publicada)(raiz)[0]
    except Exception:  # noqa: BLE001 (sin módulo o sin red: la puerta queda cerrada)
        return False


def _etiqueta_v18_ok(raiz: Path) -> bool:
    """V18: puerta del plan de replicación (src/v18/etiqueta.py)."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("etiqueta_v18", raiz / "src" / "v18" / "etiqueta.py")
        e = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(e)
        return e.puerta(raiz)[0]
    except Exception:  # noqa: BLE001 (sin módulo: la puerta queda cerrada)
        return False


CUERPO = re.compile(r"(?m)^([^\n]*?)<<-?\s*(['\"])([A-Za-z_][A-Za-z0-9_]*)\2[^\n]*\n(.*?)^\3\s*$", re.S)


def _sin_cuerpos(cmd: str, solo_texto: bool = False) -> str:
    """Quita el cuerpo de los heredocs entrecomillados (el shell no lo expande). Con solo_texto, solo los que escriben un
    fichero con cat o tee: en el cuerpo de un heredoc para python o bash, «make all» sí sería una orden."""
    def rep(m):
        if solo_texto and not re.search(r"\b(cat|tee)\b", m.group(1)):
            return m.group(0)
        return m.group(1) + "<<'cuerpo'\n"
    return CUERPO.sub(rep, cmd)


def evaluar(cmd: str, raiz: Path) -> str | None:
    if HEREDOC_SIN_COMILLAS.search(_sin_cuerpos(cmd)):
        return "(a) heredoc sin comillas: use <<'EOF' (el shell expandiría `…` y $(…); incidente D3)"
    if SELLADO in cmd and "src/holdout.py" not in cmd:
        return "(b) la muestra sellada solo se toca a través de src/holdout.py"
    if re.search(r"\bmake\b[^;&|]*\scheck(\s|$|;|&|\|)", cmd) and _make_check_en_marcha():
        return "(c) ya hay un make check en marcha: un solo make check a la vez"
    if re.search(r"\bmake\b[^;&|]*\sv15_f[45]", cmd) and not _etiqueta_ok(raiz, "v15"):
        return "(d) fases 4-5 de V15 bloqueadas: la etiqueta prereg-v15 no está en el remoto apuntando a 542b4fd"
    if re.search(r"\bmake\b[^;&|]*\s(v16_f[5-7]\w*|v16)(\s|$|;|&|\|)", cmd) and not _etiqueta_ok(raiz, "v16"):
        return "(f) fases 5-7 de V16 bloqueadas: la etiqueta prereg-v16 no existe en el remoto"
    if re.search(r"\bmake\b[^;&|]*\s(v18_f[3-6]\w*|v18)(\s|$|;|&|\|)", _sin_cuerpos(cmd, solo_texto=True)) \
            and not _etiqueta_v18_ok(raiz):
        return "(g) fases 3-6 de V18 bloqueadas: falta la etiqueta local plan-replicacion-v18 con su commit en la rama remota"
    orden = _sin_cuerpos(cmd, solo_texto=True)
    for pat, motivo in PROHIBIDOS:
        if pat.search(orden):
            return "(e) " + motivo
    return None


def main() -> int:
    try:
        datos = json.load(sys.stdin)
    except ValueError:
        return 0
    if datos.get("tool_name") != "Bash":
        return 0
    cmd = (datos.get("tool_input") or {}).get("command", "")
    raiz = Path(os.environ.get("CLAUDE_PROJECT_DIR", Path(__file__).resolve().parents[2]))
    motivo = evaluar(cmd, raiz)
    if motivo:
        print(f"Guarda V15: {motivo}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
