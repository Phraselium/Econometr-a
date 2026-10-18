"""V16 · Fase 7 · Ensambla el informe integral desde output/v16/informe/plantilla/*.md (las escribe el redactor, con marcadores {{id}}
de output/v5/cifras_clave.csv) y sustituye cada marcador con las mismas funciones que el resto de entregables (src/v5/render.py).

Escribe output/v16/informe/informe_integral.md y output/v16/informe/resultado.json. Falla (código 1) si queda algún marcador sin
cifra o algún «[FALTA CIFRA». Lo copia a publicacion/informe_integral/ `make publicacion` (src/v7_1/publicacion.py). Sin red, determinista.
Uso: python3 src/v16/f7_informe.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v5"))
import render as R  # noqa: E402

DIR = RAIZ / "output" / "v16" / "informe"
PLANT = DIR / "plantilla"
CABECERA = """# Vivienda en España: informe integral (V16)

Informe integral de la versión V16 del proyecto (docs/v16/plan.md, fase 7). Toda cifra procede de output/v5/cifras_clave.csv, con su
capa (C1 hechos con al menos dos fuentes; C2 cotas; C3 y C3s efectos; C4 exploratorio). Los resultados de V15 y V16 tienen
pre-registro interno, sin sello de tiempo externo (etiquetas prereg-v15 y prereg-v16 en el remoto). Generado por src/v16/f7_informe.py;
no se edita a mano.
"""


def ensamblar() -> tuple[str, dict]:
    ck = pd.read_csv(RAIZ / "output" / "v5" / "cifras_clave.csv").set_index("id")
    partes = sorted(PLANT.glob("[0-9][0-9]_*.md"))
    trozos, falta, ids = [CABECERA], [], set()
    for p in partes:
        txt, f = R.render(p, ck)
        falta += [f"{p.name}: {i}" for i in f]
        ids |= {m.group(1) for m in R.MARC.finditer(p.read_text(encoding="utf-8"))}
        trozos.append(txt.strip() + "\n")
    texto = "\n\n".join(trozos)
    pendientes = re.findall(r"\[FALTA CIFRA[^\]]*\]", texto)
    capas = ck.loc[sorted(i for i in ids if i in ck.index), "capa"].value_counts().to_dict()
    res = dict(rama="V16-F7", pregunta="Informe integral (fase 7)", capa="C1-C4 (la de cada cifra)", partes=[p.name for p in partes],
               marcadores=len(ids), ids_por_capa={str(k): int(v) for k, v in capas.items()}, marcadores_sin_cifra=falta,
               falta_cifra=pendientes, notas="Ensamblado determinista; las cifras vienen de cifras_clave.")
    return texto, res


def main() -> int:
    texto, res = ensamblar()
    DIR.mkdir(parents=True, exist_ok=True)
    (DIR / "informe_integral.md").write_text(texto, encoding="utf-8")
    (DIR / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"f7_informe: {len(res['partes'])} partes, {res['marcadores']} cifras distintas, "
          f"{len(res['marcadores_sin_cifra'])} marcadores sin cifra, {len(res['falta_cifra'])} [FALTA CIFRA]")
    for x in res["marcadores_sin_cifra"] + res["falta_cifra"]:
        print("  -", x)
    return 1 if res["marcadores_sin_cifra"] or res["falta_cifra"] else 0


if __name__ == "__main__":
    sys.exit(main())
