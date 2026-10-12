"""V7: validación limpia DIFERIDA (`make evaluate_v7`). Fuera de `make all`.

Evalúa UNA sola vez los modelos de predicción congelados de R5 con datos publicados DESPUÉS de la fecha verificable del
pre-registro V7 (release o DOI; docs/v7/notas_release.md):
  - trimestrales por CCAA 2026T3-2027T2 (IPV, IPC alquiler; y los regresores que usen los modelos);
  - anuales 2026, cuando se publiquen.

Pasos:
  1. Comprueba que existe la congelación (output/v7/R5/modelos_congelados.json) y que su sha256 coincide con el anotado en
     docs/v7/notas_release.md (la congelación es anterior a la apertura).
  2. Descarga (CON red) los datos nuevos a data/raw/v7_eval/<fecha>/ con los scripts fetch_* existentes, sin tocar data/raw.
  3. Si no hay ningún periodo posterior a 2026T2, sale SIN registrar apertura («aún no hay datos»).
  4. Si ya hay una apertura registrada en docs/v7/evaluate_v7_accesos.md, se niega (una sola evaluación).
  5. Registra la apertura (fecha UTC, periodos, sha256 de la congelación) ANTES de evaluar y después evalúa: RMSE a 1-4
     trimestres frente a la base fuerte de K1 (AR con factor común) y AR(4); DM-HLN y permutación por CCAA; Holm.
  6. Escribe output/v7/evaluate/resultado.json y añade el resultado al registro de accesos.

Uso: python3 src/v7/evaluate_v7.py [--simular]   (--simular: ensayo con datos de entrenamiento troceados; no registra)
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CONG = RAIZ / "output" / "v7" / "R5" / "modelos_congelados.json"
NOTAS = RAIZ / "docs" / "v7" / "notas_release.md"
ACCESOS = RAIZ / "docs" / "v7" / "evaluate_v7_accesos.md"
OUT = RAIZ / "output" / "v7" / "evaluate"
ULTIMO_ENTRENO = "2026Q2"


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def ya_abierto() -> bool:
    return ACCESOS.exists() and "APERTURA" in ACCESOS.read_text(encoding="utf-8")


def sha_anotado() -> str | None:
    if not NOTAS.exists():
        return None
    for ln in NOTAS.read_text(encoding="utf-8").splitlines():
        if ln.strip().startswith("sha256_modelos_congelados:"):
            return ln.split(":", 1)[1].strip()
    return None


def descargar(destino: Path) -> None:
    """Descarga con los scripts fetch_* existentes hacia un directorio aparte (no reescribe data/raw)."""
    destino.mkdir(parents=True, exist_ok=True)
    import os
    env = {**os.environ, "RAW_DIR": str(destino), "FORCE": "1"}   # utils_fetch respeta RAW_DIR (no toca data/raw)
    for s in ("src/fetch_ine.py", "src/fetch_ine_v2.py", "src/fetch_mivau.py"):
        subprocess.run([sys.executable, s], cwd=RAIZ, env=env, check=False)


def main(simular: bool = False) -> int:
    if not CONG.exists():
        print("evaluate_v7: falta output/v7/R5/modelos_congelados.json (R5 no ha congelado los modelos).")
        return 2
    s = sha256(CONG)
    if not simular and sha_anotado() != s:
        print("evaluate_v7: el sha256 de la congelación no coincide con docs/v7/notas_release.md: no se evalúa.")
        return 2
    if not simular and ya_abierto():
        print("evaluate_v7: la validación diferida ya se abrió una vez (docs/v7/evaluate_v7_accesos.md).")
        return 3
    sys.path.insert(0, str(RAIZ / "src" / "v7"))
    import r5_prediccion as R5   # interfaz que implementa R5: nuevos_periodos(), evaluar_congelado()
    hoy = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if simular:
        res = R5.evaluar_congelado(CONG, datos=None, simular=True)
        print(json.dumps(res, ensure_ascii=False, indent=1)[:2000])
        return 0
    destino = RAIZ / "data" / "raw" / "v7_eval" / hoy[:10]
    descargar(destino)
    nuevos = R5.nuevos_periodos(destino, despues_de=ULTIMO_ENTRENO)
    if not nuevos:
        print("evaluate_v7: aún no hay periodos posteriores a 2026T2; no se registra apertura.")
        return 0
    with ACCESOS.open("a", encoding="utf-8") as f:
        f.write(f"| {hoy} | APERTURA | periodos {nuevos[0]}-{nuevos[-1]} | sha256 congelación {s} |\n")
    res = R5.evaluar_congelado(CONG, datos=destino, simular=False)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    with ACCESOS.open("a", encoding="utf-8") as f:
        f.write(f"| {dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} | EVALUACIÓN | "
                f"{json.dumps(res.get('resumen', {}), ensure_ascii=False)[:300]} | |\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(simular="--simular" in sys.argv))
