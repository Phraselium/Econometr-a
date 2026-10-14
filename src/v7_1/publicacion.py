"""V7.1-S5 · `make publicacion`: genera publicacion/, metodologia/ y reproducir/ desde output/ y docs/. Nunca se editan a mano.

- Copia cada fichero desde su fuente versionada (tabla FUENTES), con una cabecera «generado; no editar» en los .md.
- Reescribe los enlaces relativos de los .md: si el destino también se publica, apunta a la copia publicada; si no, a
  la ruta del repositorio. Los anclajes (#…) se conservan.
- Escribe un MANIFIESTO.md por carpeta con la fuente y el sha256 de cada fichero.
Antes de copiar, regenera los entregables con render v5 y render v8 (V8.1). Determinista y sin red. tests/v7_1/test_publicacion.py lo regenera en un directorio temporal y compara byte a byte.
"""
from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CARPETAS = ("publicacion", "metodologia", "reproducir")
ATLAS = sorted(p.relative_to(RAIZ).as_posix() for p in (RAIZ / "output" / "v7_1" / "atlas").glob("*") if p.is_file())

# destino -> fuente (rutas relativas a la raíz del repositorio)
FUENTES: dict[str, str] = {
    "publicacion/una_pagina.md": "output/v5/una_pagina.md",
    "publicacion/lo_que_sabemos.md": "output/v5/lo_que_sabemos.md",
    "publicacion/policy_brief.md": "output/v5/policy_brief.md",
    "publicacion/informe_tecnico.md": "output/v5/informe_tecnico.md",
    "publicacion/working_paper.md": "output/v5/working_paper.md",
    "publicacion/nota_metodologica.md": "output/v5/nota_metodologica.md",
    "publicacion/articulo_colegio.md": "output/v5/articulo_colegio.md",
    "publicacion/que_cambio.md": "output/v5/que_cambio.md",
    "publicacion/ponencia/diapositivas.md": "output/v5/ponencia/diapositivas.md",
    "publicacion/ponencia/guion.md": "output/v5/ponencia/guion.md",
    **{f"publicacion/atlas_regional/{Path(a).name}": a for a in ATLAS},
    "publicacion/verificador/verificador.md": "output/v5/verificador/verificador.md",
    "publicacion/verificador/verificador_v7_1.md": "output/v7_1/verificador_v7_1.md",
    "publicacion/verificador/fichas_v7_1.json": "output/v7_1/fichas/fichas_verificador.json",
    # V8 (F6): verificador y fichas de V8 (texto y JSON generados por src/v8/f6_verificador.py)
    "publicacion/verificador/verificador_v8.md": "output/v8/verificador_v8.md",
    "publicacion/verificador/fichas_v8.json": "output/v8/fichas_verificador_v8.json",
    # V8 (F6): entregables (tablas_v8.xlsx se copia en binario: los ficheros que no son .md se copian tal cual).
    "publicacion/por_que_ha_subido.md": "output/v8/por_que_ha_subido.md",
    "publicacion/informe_econometrico_v8.md": "output/v8/informe_econometrico.md",
    "publicacion/tablas_modelos_destacados.md": "output/v8/tablas_modelos_destacados.md",
    "publicacion/tablas_modelos_destacados.csv": "output/v8/tablas_modelos_destacados.csv",
    "publicacion/tablas_v8.xlsx": "output/v8/tablas_v8.xlsx",
    "publicacion/cifras_clave.csv": "output/v5/cifras_clave.csv",
    # V10: atlas descriptivo (texto generado por src/v10/atlas_texto.py)
    "publicacion/atlas_descriptivo.md": "output/v10/atlas_descriptivo.md",
    "publicacion/tablas_atlas.xlsx": "output/v10/tablas_atlas.xlsx",
    "publicacion/dosis_coste.csv": "output/v7_1/S1/dosis_coste.csv",
    "metodologia/anexo_metodologico.md": "output/v6_2/anexo_metodologico.md",
    "metodologia/guia_revisor.md": "docs/v7_1/guia_revisor.md",
    "metodologia/capas.md": "docs/v7_1/capas.md",
    "metodologia/historial_conclusiones.md": "docs/v6_1/historial_conclusiones.md",
    "metodologia/validacion_montecarlo.md": "docs/v7/validacion_herramientas.md",
    "metodologia/preregistro_v7.md": "docs/v7/hipotesis.md",
    "metodologia/preregistro_v8.md": "docs/v8/hipotesis.md",
    "metodologia/desviaciones_v8.md": "docs/v8/desviaciones.md",
    "metodologia/revision_v8_F4.md": "docs/v8/revision_F4.md",
    "metodologia/dosis_coste.md": "output/v7_1/S1/resumen.md",
    "reproducir/instrucciones.md": "README_REPLICACION.md",
    "reproducir/tiempos.md": "docs/v7_1/tiempos.md",
    "reproducir/evaluacion_2027.md": "docs/v7_1/evaluacion_2027.md",
    "reproducir/ensayo_evaluate_v7.md": "output/v7_1/S4/ensayo.md",
}
CLAVE_LIBS = ("numpy", "pandas", "scipy", "statsmodels", "linearmodels", "arch", "scikit-learn", "lightgbm", "xgboost", "pymc",
              "torch", "openpyxl", "matplotlib", "pytest", "ruff")
ENLACE = re.compile(r"(\]\()([^)\s]+)(\))")
CAB = "<!-- Generado por `make publicacion` desde {src}. No editar a mano: se regenera y un test lo comprueba. -->\n\n"


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _reescribir(txt: str, src: str, dst: str) -> str:
    inverso = {v: k for k, v in FUENTES.items()}
    sdir, ddir = (RAIZ / src).parent, (RAIZ / dst).parent

    def rep(m):
        t = m.group(2)
        if re.match(r"^(?:[a-z]+:|#|/)", t):
            return m.group(0)
        ruta, _, ancla = t.partition("#")
        if not ruta:
            return m.group(0)
        abs_ = (sdir / ruta).resolve()
        try:
            rel_repo = abs_.relative_to(RAIZ).as_posix()
        except ValueError:
            return m.group(0)
        destino = RAIZ / inverso[rel_repo] if rel_repo in inverso else abs_
        if rel_repo not in inverso and not abs_.exists():
            return m.group(0)   # enlace ya roto en la fuente: se deja igual (lo detecta el test de enlaces)
        nuevo = os.path.relpath(destino, ddir).replace(os.sep, "/")
        return f"{m.group(1)}{nuevo}{'#' + ancla if ancla else ''}{m.group(3)}"
    return ENLACE.sub(rep, txt)


def _entorno() -> str:
    libs = {}
    for ln in (RAIZ / "requirements.lock").read_text(encoding="utf-8").splitlines():
        if "==" in ln:
            n, v = ln.split("==", 1)
            libs[n.strip().lower()] = v.strip()
    L = ["# Entorno y versiones de las bibliotecas", "", "Python 3.13 (un solo hilo: OMP_NUM_THREADS = OPENBLAS_NUM_THREADS = MKL_NUM_THREADS = 1; "
         "SEED = 20261010). Lista completa y fijada: [requirements.lock](../requirements.lock).", "",
         "| Biblioteca | Versión |", "|---|---|"]
    L += [f"| {n} | {libs[n]} |" for n in CLAVE_LIBS if n in libs]
    L += ["", "Programa del sistema: `pdftotext` (poppler-utils). Instalación: `python3 -m pip install -r requirements.lock`.", ""]
    return "\n".join(L)


def construir(base: Path) -> dict[str, list[tuple[str, str, str]]]:
    man: dict[str, list[tuple[str, str, str]]] = {c: [] for c in CARPETAS}
    for dst, src in FUENTES.items():
        p = RAIZ / src
        if not p.exists():
            raise SystemExit(f"publicacion: falta la fuente {src} (ejecute antes make v7_1 / la tarea que la genera)")
        out = base / dst
        out.parent.mkdir(parents=True, exist_ok=True)
        if p.suffix == ".md":
            txt = _reescribir(p.read_text(encoding="utf-8"), src, dst)
            if dst == "publicacion/verificador/verificador.md":   # v7.1 (H12): título coherente con la versión de referencia
                txt = re.sub(r"^(# Verificador de afirmaciones[^\n]*?)\s*\(v5\)", r"\1 (fichas v5-v6.3, vigentes en v7.1)", txt, count=1)
            b = (CAB.format(src=src) + txt).encode("utf-8")
        else:
            b = p.read_bytes()
        out.write_bytes(b)
        man[dst.split("/")[0]].append((dst, src, _sha(b)))
    ent = (CAB.format(src="requirements.lock") + _entorno()).encode("utf-8")
    (base / "reproducir" / "entorno.md").write_bytes(ent)
    man["reproducir"].append(("reproducir/entorno.md", "requirements.lock", _sha(ent)))
    for c, filas in man.items():
        L = [f"# Manifiesto de {c}/", "", "Generado por `make publicacion` (src/v7_1/publicacion.py). Ningún fichero de esta carpeta se edita a mano.", "",
             "| Fichero | Fuente | sha256 |", "|---|---|---|"]
        L += [f"| {Path(d).relative_to(c).as_posix()} | {s} | `{h}` |" for d, s, h in sorted(filas)]
        (base / c / "MANIFIESTO.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    return man


def regenerar_entregables() -> None:
    """V8.1: una_pagina, lo_que_sabemos y los entregables V8 se regeneran antes de copiarlos (render v5 y render v8; ambos leen output/v5/cifras_clave.csv).
    `make v8` ya ejecuta cifras_clave y render_v8, pero no render v5: sin este paso, una_pagina y lo_que_sabemos podrían quedar con cifras de otra versión de cifras_clave."""
    for scr in ("src/v5/render.py", "src/v8/render_v8.py"):
        r = subprocess.run([sys.executable, str(RAIZ / scr)], cwd=RAIZ, capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit(f"publicacion: falla {scr} (marcadores sin resolver o error):\n{r.stdout[-800:]}{r.stderr[-800:]}")


def main() -> int:
    regenerar_entregables()
    for c in CARPETAS:
        if (RAIZ / c).exists():
            shutil.rmtree(RAIZ / c)
    man = construir(RAIZ)
    print("publicacion: " + ", ".join(f"{c}/ {len(v)} ficheros" for c, v in man.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
