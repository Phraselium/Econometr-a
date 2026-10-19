"""V17 · Fase 1 · Inventario de lo que la auditoría y D3 necesitan frente a lo que ya hay en data/raw (análisis a posteriori).

Cada necesidad del plan (fase 1) lista sus rutas candidatas; el script comprueba cuáles existen y escribe
output/v17/f1/inventario.md y output/v17/f1/inventario.csv. Determinista, sin red; no lee data/sealed.
"""
from __future__ import annotations

import csv
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "output" / "v17" / "f1"

# necesidad -> (bloque, [rutas en data/raw que la cubren total o parcialmente], nota)
NECESIDADES: list[tuple[str, str, list[str], str]] = [
    ("Viviendas turísticas por sección y municipio (INE VTE)", "Turismo local",
     ["data/raw/ine_v2_vut.csv", "data/raw/ine_vut_nacional_ccaa_prov.csv", "data/raw/v16/alquiler_turismo"], ""),
    ("Registros autonómicos de vivienda turística", "Turismo local",
     ["data/raw/gva_vut_municipio.csv", "data/raw/v11/gva_vut", "data/raw/v11/euskadi_vut", "data/raw/v17/turismo_local"], ""),
    ("InsideAirbnb (grandes ciudades)", "Turismo local", ["data/raw/v17/turismo_local"], "terceros: CC BY 4.0; solo agregados"),
    ("Parque de alquiler por sección (denominador local; Censo 2021)", "Turismo local",
     ["data/raw/v11/ine_censo2021", "data/raw/v17/turismo_local"], ""),
    ("Población por nacionalidad y país de nacimiento (ECP)", "Migración y hogares",
     ["data/raw/ine_ecp_ccaa_nacionalidad.csv", "data/raw/ine_ecp_ccaa_paises.csv", "data/raw/v11/ine_ecp"], ""),
    ("Saldo migratorio exterior por nacionalidad (EVR)", "Migración y hogares",
     ["data/raw/ine_migraciones_nacionalidad.csv", "data/raw/v11/ine_evr"], ""),
    ("Nacimientos y defunciones por nacionalidad (MNP)", "Migración y hogares", ["data/raw/v11/ine_mnp"], ""),
    ("Migración interior entre provincias (EVR)", "Migración y hogares",
     ["data/raw/ine_v2_migraciones_prov.csv", "data/raw/v11/ine_evr"], ""),
    ("Tenencia por nacionalidad o país de nacimiento (Censo 2021, ECEPOV)", "Migración y hogares",
     ["data/raw/v11/ine_censo2021", "data/raw/v11/ine_ecepov", "data/raw/v11/ine_censos_microdatos"], ""),
    ("Hogares y tamaño medio por edad (ECP, EPA, Proyección de hogares)", "Migración y hogares",
     ["data/raw/ine_hogares_60131.csv", "data/raw/ine_epa_hogares.csv", "data/raw/ine_v2_hogares_prov.csv"], ""),
    ("Compras con y sin hipoteca (agregados)", "Crédito y compras",
     ["data/raw/ine_v2_hipotecas_prov.csv", "data/raw/ine_etdp_compraventas.csv", "data/raw/v17/credito"], "terceros: solo agregados"),
    ("Compras de no residentes y de extranjeros", "Crédito y compras",
     ["data/raw/mivau_transacciones_extranjeros.csv", "data/raw/mivau_transacciones_residencia.csv"], ""),
    ("Compras de personas jurídicas", "Crédito y compras", ["data/raw/v17/credito"], ""),
    ("Crédito hipotecario nuevo", "Crédito y compras",
     ["data/raw/ecb_nuevo_credito_vivienda_es.csv", "data/raw/bde_credito_finalidad.csv"], ""),
    ("LTV, LTI y esfuerzo financiero (Banco de España)", "Crédito y compras", ["data/raw/v17/credito"], ""),
    ("Estadísticas catastrales de titularidad", "Titularidad", ["data/raw/v11/catastro_titularidad"], ""),
    ("Catastro por transparencia (más de diez viviendas)", "Titularidad", ["data/raw/v17/titularidad"], ""),
    ("Observatori Metropolità de l'Habitatge de Barcelona", "Titularidad", ["data/raw/v17/titularidad"], ""),
    ("Ministerio: oferta de alquiler de grandes propietarios", "Titularidad", ["data/raw/v17/titularidad"], ""),
    ("Vivienda social y pública frente a la UE (OCDE AHD, Eurostat)", "Parque social",
     ["data/raw/v17/parque_social", "data/raw/mivau_v2_protegida.csv"], ""),
    ("Renta disponible de los hogares (contabilidad nacional)", "Renta", ["data/raw/ine_cnt_renta_disponible.csv"], ""),
    ("Renta por sección (ADRH)", "Renta", ["data/raw/v16/renta_parque"], ""),
    ("Suelo urbano y urbanizable por municipio (SIU)", "Oferta y capacidad",
     ["data/raw/mivau_v2_suelo.csv", "data/raw/v16/oferta_suelo"], ""),
    ("Visados, iniciadas y terminadas", "Oferta y capacidad",
     ["data/raw/mivau_visados.csv", "data/raw/mivau_v2_iniciadas_terminadas_prov.csv", "data/raw/mivau_fin_obra.csv"], ""),
    ("Empleo en la construcción (EPA por rama)", "Oferta y capacidad",
     ["data/raw/ine_epa_ocupados.csv", "data/raw/eurostat_empleo_nuts2.csv", "data/raw/v17/oferta_capacidad"], ""),
    ("Costes de la construcción (INE ICC, Eurostat)", "Oferta y capacidad",
     ["data/raw/eurostat_costes.csv", "data/raw/v17/oferta_capacidad"], ""),
    ("Plazos de licencias", "Oferta y capacidad", ["data/raw/v17/oferta_capacidad"], ""),
    ("Viviendas previstas en grandes áreas (Banco de España)", "Oferta y capacidad",
     ["docs/v17/referencias/bde_informes.md"], "cifra de documento, no serie"),
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    filas = []
    for nec, bloque, rutas, nota in NECESIDADES:
        hay = [r for r in rutas if (RAIZ / r).exists() and (not (RAIZ / r).is_dir() or any((RAIZ / r).iterdir()))]
        estado = "cubierta" if hay else "falta"
        nueva = "sí" if any("v17" in r for r in hay) else "no"
        filas.append({"bloque": bloque, "necesidad": nec, "estado": estado, "fuente_nueva_v17": nueva,
                      "rutas_presentes": "; ".join(hay) or "-", "nota": nota})
    with (OUT / "inventario.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, list(filas[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(filas)
    L = ["# V17 · Fase 1 · Inventario de datos para la auditoría", "",
         "Análisis a posteriori (V17). Generado por src/v17/f1_inventario.py. «cubierta»: hay al menos una fuente previa; "
         "«parcial»: solo parte; «falta»: no hay nada en data/raw.", "",
         "| Bloque | Necesidad | Estado | Nueva en V17 | Rutas presentes | Nota |", "|---|---|---|---|---|---|"]
    L += [f"| {f['bloque']} | {f['necesidad']} | {f['estado']} | {f['fuente_nueva_v17']} | {f['rutas_presentes']} | {f['nota']} |" for f in filas]
    (OUT / "inventario.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    n = {e: sum(f["estado"] == e for f in filas) for e in ("cubierta", "falta")}
    print(f"f1_inventario V17: {len(filas)} necesidades; {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
