"""v6.2: ficha del verificador del déficit 2021-2024 a partir de L3 (sustituye a V05 de v4). Sin red; lee output/v6_2/L3."""
from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
L3 = RAIZ / "output" / "v6_2" / "L3"


def miles(x):
    return f"{float(x):,.0f}".replace(",", ".")


def main():
    h = {x["id"]: x for x in json.loads((L3 / "hechos.json").read_text())}
    s, b, d5 = h["L3-DEF-2124-SINBAJAS"], h["L3-DEF-2124-CONBAJAS"], h["L3-DEF-2125"]
    ficha = dict(
        id="L3-V1", tema="Déficit",
        enunciado="Faltan cientos de miles de viviendas en España.",
        capa="C2",
        magnitud=(f"Déficit acumulado 2021-2024 (aumento de hogares menos viviendas terminadas), sin bajas del parque: {miles(s['min'])}-{miles(s['max'])} "
                  f"viviendas según la corrección del salto de la EPA en 2021 (siete variantes) y la fuente de terminadas (Ministerio o Catastro); "
                  f"con bajas supuestas, {miles(b['min'])}-{miles(b['max'])}. 2021-2025: {miles(d5['min'])}-{miles(d5['max'])} (C4: terminadas de 2025 frágiles)."),
        intervalo=f"cota {miles(s['min'])}-{miles(s['max'])} viviendas (sin bajas)", cota="C2: supuestos explícitos sobre la corrección de la EPA",
        literatura="Banco de España (2024, 2025): estimaciones de 375.000-600.000 viviendas en periodos parecidos (output/v5/D3/convergencia.md).",
        veredicto="PARCIALMENTE",
        regla=("El signo (más hogares que viviendas terminadas) lo confirman dos fuentes de hogares y dos de terminadas en todas las variantes; "
               "la cuantía es una cota porque la amplitud entre correcciones de la EPA supera la tolerancia de C1 (±15 %). «Cientos de miles» "
               "se cumple en todas las variantes; una cifra puntual no es defendible."),
        limites="Sin bajas del parque observadas; la EPA cambió de metodología en 2021T1; las terminadas de 2025 son frágiles.",
        evidencia=["output/v6_2/L3/deficit_alternativas.md", "output/v6_2/L3/resultado.json", "output/v6_2/anexo_metodologico.md"])
    (L3 / "fichas_verificador.json").write_text(json.dumps([ficha], ensure_ascii=False, indent=1))
    print("l3_ficha: 1 ficha")


if __name__ == "__main__":
    main()
