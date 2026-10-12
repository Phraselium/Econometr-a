"""K6 v6.1: fichas del verificador a partir de K1 y K2 (lee solo salidas versionadas de output/v6_1). Sin red."""
from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
O = RAIZ / "output" / "v6_1"


def h(mod):
    return {x["id"]: x for x in json.loads((O / mod / "hechos.json").read_text())}


def es(x, d=2):
    return f"{x:.{d}f}".replace(".", ",")


def main():
    k2, k1 = h("K2"), h("K1")
    s, e, p = k2["K2-CUOTA-COMPRA-SINPOB-SIN"], k2["K2-CUOTA-COMPRA-SINPOB-EXT"], k2["K2-CUOTA-COMPRA-SIN"]
    a = k2["K2-CUOTA-ALQ-SINPOB-SIN"]
    fichas = [dict(
        id="K2-V1", tema="Inmigración",
        enunciado="La llegada de inmigrantes sube el precio de la vivienda o el alquiler.",
        capa="C4",
        magnitud=(f"Cuota de extranjeros (t-1), EF dobles, provincias de entrenamiento. Asociación TOTAL (sin controlar por población; la inmigración "
                  f"es un componente contable de su crecimiento): valor tasado {es(s['valor'])} % por pp [{es(s['min'])}; {es(s['max'])}], con demanda externa {es(e['valor'])} "
                  f"[{es(e['min'])}; {es(e['max'])}]; alquiler de stock {es(a['valor'])} [{es(a['min'])}; {es(a['max'])}]. Asociación DIRECTA (a igual "
                  f"población): valor tasado {es(p['valor'])} [{es(p['min'])}; {es(p['max'])}]. Correlación cuota-población dentro de provincia "
                  f"{es(k2['K2-CORR-POB-DENTRO']['valor'])}."),
        intervalo="IC95 agrupados por provincia (output/v6_1/K2/inmigracion.md)", cota="—",
        literatura="Saiz (2007); Sá (2015): orientan el signo; ver docs/literatura.md (cuartil según marca).",
        veredicto="ANALIZADA, NO CONCLUYENTE",
        regla=("Con capa C4 el veredicto es como máximo ANALIZADA, NO CONCLUYENTE. El signo y el mercado cambian con el método (2SLS/MCO), "
               "la medida de alquiler y los controles. Controlar por población es un mal control (la población crece por la propia inmigración): "
               "el signo negativo de la asociación directa en compra no significa que la inmigración abarate la vivienda. A su vez, la total "
               "puede recoger otros factores ligados al crecimiento de la población; ninguna de las dos identifica un efecto."),
        limites=("41 provincias de entrenamiento (sin las 11 selladas, incluidas las islas); no reproduce la muestra de 49 provincias de v2; "
                 "primera etapa débil del instrumento en esta muestra."),
        evidencia=["output/v6_1/K2/inmigracion.md", "output/v6_1/K2/pasos_inmigracion.csv", "docs/v6_1/historial_conclusiones.md"]),
        dict(
        id="K1-V1", tema="Predicción del precio y del alquiler",
        enunciado="Los modelos de inteligencia artificial predicen el precio y el alquiler mejor que los métodos sencillos.",
        capa="C4",
        magnitud=(f"En la validación sellada v6, el mejor modelo supera a la línea base más exigente en {k1['K1-N-MEJOR']['valor']} de 9 tareas "
                  f"(alquiler de stock en provincia, municipio y distrito; precio de tasación trimestral y, frágil, anual; volumen trimestral espacial). "
                  f"Alquiler provincial: {es(k1['K1-RMSE-alq_provincia']['valor'])} % frente a {es(k1['K1-BASE-alq_provincia']['valor'])} % (AR con factor común)."),
        intervalo="DM-HLN y permutación exacta por provincias, Holm (output/v6_1/K1/tabla_modelos_k1.md)", cota="—",
        literatura="Harvey, Leybourne y Newbold (1997) para el contraste.",
        veredicto="ANALIZADA, NO CONCLUYENTE",
        regla=("Con capa C4 el veredicto es como máximo ANALIZADA, NO CONCLUYENTE. La ventaja solo aparece en las tareas en que se supera a la base más exigente; no distinguible en precio municipal, Registradores y volumen anual. "
               "Predicción, no causalidad."),
        limites="Segunda mirada a la muestra sellada para comparadores nuevos; 11 provincias selladas; poca potencia.",
        evidencia=["output/v6_1/K1/tabla_modelos_k1.md", "output/v6_1/K1/notas.md"])]
    for f in fichas:
        d = O / f["id"].split("-")[0]
        (d / "fichas_verificador.json").write_text(json.dumps([f], ensure_ascii=False, indent=1))
    print(f"k6_fichas: {len(fichas)} fichas")


if __name__ == "__main__":
    main()
