"""V17 · Fase 3 · Tabla final «antes / después / por qué» de la auditoría crítica (análisis a posteriori).

Une las tablas de los tres grupos (output/v17/auditoria/{demanda_precios,oferta_titularidad,regulacion_ayudas}.csv), una fila por
afirmación auditada, y enlaza la ficha de cada fila y de cada pregunta D3. No lee datos: solo salidas de la auditoría.
Salidas: output/v17/auditoria/tabla_final.{csv,md}. Determinista; sin red.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ALCANCE_TERRITORIAL = "sin lectura de datos"
RAIZ = Path(__file__).resolve().parents[2]
AUD = RAIZ / "output" / "v17" / "auditoria"
GRUPOS = {"demanda_precios": "Demanda y precios", "oferta_titularidad": "Oferta y titularidad", "regulacion_ayudas": "Regulación y ayudas"}
ORDEN = {"incorrecta": 0, "engañosa": 1, "se sostiene con matices": 2, "se sostiene": 3}


def celda(x) -> str:
    return " ".join(str(x).split()).replace("|", "/") if pd.notna(x) else ""


def main() -> int:
    partes = []
    for g, nombre in GRUPOS.items():
        d = pd.read_csv(AUD / f"{g}.csv")
        partes.append(d.assign(grupo=nombre, ficha=[f"output/v17/auditoria/filas/{i}.md" for i in d.id_fila]))
    t = pd.concat(partes, ignore_index=True)
    falta = [f for f in t.ficha if not (RAIZ / f).exists()]
    malos = sorted(set(t.veredicto) - set(ORDEN))
    if falta or malos:
        print(f"f3_auditoria V17: fichas que faltan {falta}; veredictos fuera de la escala {malos}")
        return 1
    t = t.assign(_o=t.veredicto.map(ORDEN)).sort_values(["_o", "grupo", "id_fila"], kind="stable").drop(columns="_o")
    cols = ["grupo", "id_fila", "veredicto", "texto_antes", "texto_despues", "por_que", "confianza", "parada", "ficha"]
    t[cols].to_csv(AUD / "tabla_final.csv", index=False)
    n = t.veredicto.value_counts().reindex(list(ORDEN)).dropna().astype(int)
    L = ["# V17 · Fase 3 · Auditoría crítica: antes / después / por qué", "",
         "Análisis a posteriori (V17). Generado por src/v17/f3_auditoria.py a partir de las tablas de los tres grupos, tras dos rondas "
         "del abogado del diablo por fila y las decisiones del autor sobre las paradas P1 y P2 (2026-10-19) y sobre la ronda 2 "
         "(2026-10-20; docs/v17/decisiones.md, K6). Los textos «después» que corrigen lo publicado tienen su entrada en ERRATA.md. "
         "La confianza usa la escala del Banco de España; ninguna fila cambia la capa de una cifra publicada.", "",
         "Veredictos: " + "; ".join(f"{k}: {v}" for k, v in n.items()) + f" (total {len(t)} filas).", "",
         "| Grupo | Fila | Veredicto | Antes | Después | Por qué | Confianza | Parada | Ficha |", "|---|---|---|---|---|---|---|---|---|"]
    L += [f"| {r.grupo} | {r.id_fila} | {r.veredicto} | {celda(r.texto_antes)} | {celda(r.texto_despues)} | {celda(r.por_que)} | "
          f"{celda(r.confianza)} | {celda(r.parada)} | [{r.id_fila}](filas/{r.id_fila}.md) |" for r in t.itertuples()]
    preg = sorted((AUD / "preguntas").glob("D3-*.md"))
    L += ["", "## Preguntas D3", "", "Respuestas cuantitativas y contables (C4, a posteriori), una ficha por pregunta:", ""]
    L += [f"- [{p.stem}](preguntas/{p.name})" for p in preg]
    (AUD / "tabla_final.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"f3_auditoria V17: {len(t)} filas; {n.to_dict()}; {len(preg)} preguntas D3")
    return 0


if __name__ == "__main__":
    sys.exit(main())
