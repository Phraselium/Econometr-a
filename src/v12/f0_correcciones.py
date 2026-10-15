"""V12-F0 · Correcciones previas (descriptivo; sin modelos).

1. Empalme de titularidad del Catastro: la serie JAXI 2012-2023 cuenta TITULARES catastrales (todos los cotitulares y
   titulares de cualquier derecho, por clase urbano/rústico) y los CSV 2024-2026 cuentan SUJETOS PASIVOS del IBI (un
   contribuyente por inmueble) por tramo de nº de inmuebles DENTRO DEL ÁMBITO y tipo de persona. No se encadenan. Se mide
   el salto 2023 → 2024 (titulares urbanos JAXI frente a sujetos pasivos de inmuebles urbanos y de uso residencial).
2. AEAT: declarantes aproximados con rentas de bienes inmuebles no afectos a actividades económicas = importe ÷ media.
   Precisión: la media se publica en euros (redondeo ±0,5 €), error relativo ≤ 0,5/media (~0,04 % con medias de ~1.300 €).
   OJO: el concepto incluye rendimientos del capital inmobiliario (alquileres) E imputación de rentas de inmuebles no
   alquilados (segundas viviendas, vacías); no identifica caseros. La «media» puede calcularse sobre declaraciones o
   titulares; cuotas > 1 en algunos municipios lo indican (se marcan). 2013-2015 tienen otro diseño: separan
   rendimientos del capital inmobiliario (alquileres) y rendimiento neto imputado, sin media; no hay derivación
   (aeat_inmuebles_2013_2015.csv).
Salidas: output/v12/f0/empalme_titularidad_{nacional,municipio}.csv, aeat_declarantes_inmuebles_aprox.csv, resultado.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
RAW11 = RAIZ / "data" / "raw" / "v11"
OUT = RAIZ / "output" / "v12" / "f0"
IMP = "RENTAS DE BIENES INMUEBLES NO AFECTOS A ACTIV. ECONÓMICAS"
MED = "Media de las rentas derivadas de bienes inmuebles no afectos a activ. económicas"


def empalme() -> dict:
    h = pd.read_csv(RAW11 / "catastro_titularidad/titulares_municipio_2006_2023.csv.gz", dtype={"cod_municipio": str})
    u = pd.read_csv(RAW11 / "catastro_titularidad/p_spi_mun_u.csv.gz", dtype=str)
    v = pd.read_csv(RAW11 / "catastro_titularidad/p_spi_mun_v.csv.gz", dtype=str)
    for d in (u, v):
        d["sp"] = pd.to_numeric(d.get("NUM_SUJETOS_PASIVOS"), errors="coerce")
    nac = pd.DataFrame({
        "anio": list(range(2012, 2024)) + [2024, 2025, 2026],
        "serie": ["JAXI titulares urbanos"] * 12 + ["CSV sujetos pasivos urbanos"] * 3,
        "valor": list(h.groupby("anio").titulares_urbano.sum().reindex(range(2012, 2024))) +
                 list(u.groupby("anio_fichero").sp.sum(min_count=1).reindex(["2024", "2025", "2026"]))})
    nac_v = v.groupby("anio_fichero").sp.sum(min_count=1)
    m = (h[h.anio == 2023].set_index("cod_municipio").titulares_urbano.rename("jaxi_titulares_urbanos_2023").to_frame()
         .join(u[u.anio_fichero == "2024"].set_index("CODINE").sp.rename("csv_sujetos_pasivos_urbanos_2024"))
         .join(v[v.anio_fichero == "2024"].set_index("CODINE").sp.rename("csv_sujetos_pasivos_residencial_2024")))
    m["ratio_2024_2023"] = m.csv_sujetos_pasivos_urbanos_2024 / m.jaxi_titulares_urbanos_2023
    OUT.mkdir(parents=True, exist_ok=True)
    nac.to_csv(OUT / "empalme_titularidad_nacional.csv", index=False)
    m.rename_axis("cod_municipio").reset_index().to_csv(OUT / "empalme_titularidad_municipio.csv", index=False)
    j23 = float(nac.loc[nac.anio == 2023, "valor"].iloc[0])
    c24 = float(nac.loc[nac.anio == 2024, "valor"].iloc[0])
    return {"jaxi_titulares_urbanos_2023": j23, "csv_sujetos_pasivos_urbanos_2024": c24,
            "csv_sujetos_pasivos_residencial_2024": float(nac_v.get("2024")),
            "salto_nacional_pct": round(100 * (c24 / j23 - 1), 1),
            "ratio_municipal_mediana": round(float(m.ratio_2024_2023.median()), 3),
            "ratio_municipal_p10_p90": [round(float(m.ratio_2024_2023.quantile(q)), 3) for q in (0.1, 0.9)],
            "conclusion": "cambio de definición (titulares catastrales → sujetos pasivos del IBI): no encadenar"}


def aeat() -> dict:
    a = pd.read_csv(RAW11 / "aeat_irpf_municipios/irpf_municipios_cv.csv.gz", dtype={"cod_municipio": str})
    w = a.pivot_table(index=["cod_municipio", "ejercicio"], columns="variable", values="valor").reset_index()
    w["declarantes_rentas_inmuebles_aprox"] = w[IMP] / w[MED]
    w["error_relativo_max"] = 0.5 / w[MED]
    w["cuota_sobre_declaraciones"] = w.declarantes_rentas_inmuebles_aprox / w["NÚMERO DE DECLARACIONES"]
    w["marca"] = (w.cuota_sobre_declaraciones > 1).map({True: "cuota>1: la media se calcula sobre otra base", False: ""})
    cols = ["cod_municipio", "ejercicio", "NÚMERO DE DECLARACIONES", IMP, MED, "declarantes_rentas_inmuebles_aprox",
            "error_relativo_max", "cuota_sobre_declaraciones", "marca"]
    w = w[cols].dropna(subset=["declarantes_rentas_inmuebles_aprox"]).rename(columns={
        "NÚMERO DE DECLARACIONES": "declaraciones", IMP: "importe_rentas_inmuebles", MED: "media_rentas_inmuebles"})
    w.to_csv(OUT / "aeat_declarantes_inmuebles_aprox.csv", index=False)
    # 2013-2015: otro diseño (separa alquileres e imputaciones, sin media → sin derivación del nº de declarantes)
    viejo = a[a.ejercicio <= 2015].pivot_table(index=["cod_municipio", "ejercicio"], columns="variable", values="valor")
    cols15 = {"Suma de rendimientos del capital inmobiliario": "rendimientos_capital_inmobiliario",
              "Rendimiento neto imputado de capital inmobiliario": "rendimiento_neto_imputado",
              "RENDIMIENTOS DERIVADOS DE BIENES INMUEBLES NO AFECTOS A ACTIV. ECONÓMICAS": "total_bienes_inmuebles"}
    viejo[[c for c in cols15 if c in viejo]].rename(columns=cols15).reset_index().to_csv(OUT / "aeat_inmuebles_2013_2015.csv", index=False)
    return {"municipios": int(w.cod_municipio.nunique()), "ejercicios": [int(w.ejercicio.min()), int(w.ejercicio.max())],
            "error_relativo_max_mediano": float(w.error_relativo_max.median()),
            "cuota_mediana": round(float(w.cuota_sobre_declaraciones.median()), 3), "filas_cuota_mayor_1": int((w.cuota_sobre_declaraciones > 1).sum())}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    res = {"rama": "V12-F0", "capa": "C4", "metodo": "descriptivo y contable", "empalme_titularidad": empalme(), "aeat": aeat()}
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
