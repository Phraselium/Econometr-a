"""v6.3 · VER: cifras de las fichas del verificador sin fila en cifras_clave (K4c-03, clase HUERFANA).
Lee los valores de ficheros de salida versionados (nunca tecleados) y escribe output/v6_3/VER/hechos.json y resultado.json. Sin red, determinista."""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "output" / "v6_3" / "VER"
SEED = 20261010


def J(rel):
    return json.loads((RAIZ / rel).read_text())


def buscar(o, clave):
    """Primer valor de `clave` en un JSON anidado (orden determinista)."""
    if isinstance(o, dict):
        if clave in o:
            return o[clave]
        for v in o.values():
            r = buscar(v, clave)
            if r is not None:
                return r
    elif isinstance(o, list):
        for v in o:
            r = buscar(v, clave)
            if r is not None:
                return r
    return None


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    m4 = J("output/v4/M4/hechos.json")["stock_uso_nacional"]
    m3 = next(h for h in J("output/v4/M3/hechos.json") if h["id"] == "M3-H-solares")
    m2 = next(h for h in J("output/v4/M2/hechos.json") if h["id"] == J("output/v4/M2/hechos.json")[2]["id"])
    flujo = next(x for x in m2["magnitud"] if x.get("periodo") == "2014-2019")
    cota = next(c for c in J("output/v3/PB/cotas.json") if c["id"] == "B1-nac-cantidad-viviendas")
    a23 = J("output/v5/A23/calculos.json")
    n_inc, n_gva = buscar(a23, "incasol_municipios_n"), buscar(a23, "gva_municipios_n")
    f4 = "output/v4/M4/hechos.json:stock_uso_nacional"
    L = [
        ("M4-V3", "Viviendas vacías, Censo 2021 (consumo eléctrico)", m4["vacias_consumo"], "viviendas", "2021", "España", f4, "C4", "2021"),
        ("M4-V3", "Viviendas de uso esporádico, Censo 2021 (consumo eléctrico)", m4["uso_esporadico_consumo"], "viviendas", "2021", "España", f4, "C4", "2021"),
        ("M4-V3", "Viviendas turísticas, INE VUT experimental", m4["turisticas_ine_2026M05"], "viviendas", "2026M05", "España", f4, "C4", "2026-05"),
        ("M3-V1", "Solares catastrales (uso «solar»)", m3["magnitud"], m3["unidad"], "2026", "España", "output/v4/M3/hechos.json:M3-H-solares", "C4", "2026"),
        ("B4-V1", "Aumento de la población extranjera 2014-2019 (denominador de la cota de cantidad)", flujo["delta_poblacion_extranjera"], "personas", "2014-2019", "España",
         "output/v4/M2/hechos.json:magnitud[2014-2019].delta_poblacion_extranjera", "C2", "2019"),
        ("B4-V2", "Cota C2 de viviendas de alquiler absorbidas por turismo, sustitución 1:1", cota["cota_superior"], cota["unidad"], cota["periodo"], "España",
         "output/v3/PB/cotas.json:B1-nac-cantidad-viviendas", cota["capa"], "2024-08"),
        ("A23-V2", "Municipios de Cataluña con renta de fianzas (Incasòl) en el análisis", n_inc, "municipios", "2015-2025", "Cataluña", "output/v5/A23/calculos.json:incasol_municipios_n", "C1", "2025"),
        ("A23-V2", "Municipios de la C. Valenciana con renta de fianzas (GVA) en el análisis", n_gva, "municipios", "2020-2025", "C. Valenciana", "output/v5/A23/calculos.json:gva_municipios_n", "C1", "2025"),
    ]
    hechos, cont = [], {}
    for ficha, ind, val, uni, per, cob, fuente, capa, fecha in L:
        cont[ficha] = cont.get(ficha, 0) + 1
        hechos.append(dict(id=f"VER-{ficha}-{cont[ficha]}", indicador=ind, valor=float(val), min=float(val), max=float(val), unidad=uni, periodo=per, cobertura=cob,
                           fuentes=fuente, capa=capa, fecha_dato=fecha))
    (OUT / "hechos.json").write_text(json.dumps(hechos, ensure_ascii=False, indent=1))
    res = {"rama": "VER", "pregunta": "¿Qué cifras de las fichas del verificador sin fila en cifras_clave tienen origen trazable en ficheros versionados?", "capa": "C4",
           "datos": ["output/v4/M4", "output/v4/M3", "output/v4/M2", "output/v3/PB", "output/v5/A23"], "N": {"cifras_incorporadas": len(hechos), "huerfanas_k4c": 26},
           "metodo": "lectura determinista de hechos.json/cotas.json/calculos.json; sin estimación", "estimacion": None, "ic95": None, "p_ajustado": None,
           "nivel_evidencia": "DESCRIPTIVO", "diagnosticos": None, "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
           "notas": "Fuera por no trazables o ser parámetros/constantes de diseño (no resultados): 277 y 1.806 municipios (V08), 10.000 y 104.000 (V11, dosis y brecha), 249 municipios con excedente y 53 (M5-V2/V3), 200 réplicas bootstrap, 180 escenarios (T4, recuento de rejilla), 3,79 pp (M4-V4), 7.498 y 6.947 s (tiempos de README_REPLICACION, medidos fuera del repo). Cada ficha cita la cifra en texto sin clave estructurada en un fichero versionado."}
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(len(hechos), "hechos")


if __name__ == "__main__":
    main()
