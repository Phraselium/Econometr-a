"""Auditoría V16 fase 1: intervenciones (output/v16/f1/intervenciones.csv). C4, descriptivo. SEED=20261010."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from src.v16.auditoria._comun import RAIZ, SAL, SEED, base_resultado, escribe  # noqa: E402

np.random.seed(SEED)
D = {}
d = pd.read_csv(RAIZ / "output/v16/f1/intervenciones.csv", dtype=str)
for c in ("fecha_publicacion", "fecha_efecto", "fecha_fin"):
    d[c + "_d"] = pd.to_datetime(d[c], errors="coerce")
D["filas"] = int(len(d))
D["por_instrumento"] = d.instrumento.value_counts().to_dict()
D["cod_ine_leido_como_texto"] = "OBLIGATORIO: pandas.read_csv sin dtype=str convierte cod_ine '01' en 1 (columna int64) y rompe el cruce por código INE"
D["id_duplicados"] = d.id[d.id.duplicated(keep=False)].tolist()
D["ids_zona_con_mismo_municipio_y_efecto"] = d[d.instrumento == "zona_tensionada"].groupby(["cod_ine", "fecha_efecto"]).id.apply(list).loc[lambda s: s.map(len) > 1].tolist()
amb = {"estatal": 2, "ccaa": 2, "municipio": 5}
D["cod_ine_longitud_incoherente_con_ambito"] = d[d.apply(lambda r: len(str(r.cod_ine)) != amb.get(r.ambito, -1), axis=1)].id.tolist()
D["fechas_no_parseables"] = {c: d.loc[d[c].notna() & d[c + "_d"].isna(), "id"].tolist() for c in ("fecha_publicacion", "fecha_efecto", "fecha_fin")}

# ---------- coherencia de fechas
ef = d.fecha_efecto_d
D["efecto_sin_fecha"] = d.id[ef.isna()].tolist()
D["efecto_anterior_a_publicacion"] = [(r.id, r.fecha_publicacion, r.fecha_efecto, int((r.fecha_efecto_d - r.fecha_publicacion_d).days)) for r in d.itertuples() if pd.notna(r.fecha_publicacion_d) and pd.notna(r.fecha_efecto_d) and r.fecha_efecto_d < r.fecha_publicacion_d]
D["fin_anterior_a_efecto"] = d.id[(d.fecha_fin_d < ef)].tolist()
D["sin_fecha_publicacion"] = {"n": int(d.fecha_publicacion.isna().sum()), "por_instrumento": d[d.fecha_publicacion.isna()].instrumento.value_counts().to_dict()}
lag = (ef - d.fecha_publicacion_d).dt.days.dropna()
D["efecto_menos_publicacion_dias"] = {"mediana": float(lag.median()), "max": float(lag.max()), ">30d": d.id[(ef - d.fecha_publicacion_d).dt.days > 30].tolist()}
D["rango_fechas_efecto"] = [str(ef.min().date()), str(ef.max().date())]
D["efecto_posterior_a_2026-10-17"] = d.id[ef > "2026-10-17"].tolist()

# ---------- ITP / AJD: solapes y huecos por CCAA
x = d[d.instrumento.isin(["itp", "ajd"])].copy()
x["serie"] = np.where(x.instrumento == "ajd", "ajd", np.where(x.parametro.str.contains("máximo", na=False), "itp_max", "itp_min"))
x["valor_n"] = pd.to_numeric(x.valor, errors="coerce")
FORAL = {"15", "16"}
CC = {f"{i:02d}" for i in range(1, 18)} - FORAL
sol, hue, cob = [], [], {}
H0, H1 = pd.Timestamp("2010-01-01"), pd.Timestamp("2026-12-31")
for (cod, ser), g in x.groupby(["cod_ine", "serie"]):
    g = g.sort_values("fecha_efecto_d")
    prev = None
    for r in g.itertuples():
        if prev is not None:
            fin = prev.fecha_fin_d
            if pd.isna(fin) or r.fecha_efecto_d <= fin:
                sol.append((cod, ser, prev.id, r.id, str(prev.fecha_fin), r.fecha_efecto))
            elif r.fecha_efecto_d > fin + pd.Timedelta(days=1):
                hue.append((cod, ser, prev.id, r.id, str(fin.date()), r.fecha_efecto, int((r.fecha_efecto_d - fin).days - 1)))
        prev = r
    first, last = g.iloc[0], g.iloc[-1]
    cob[f"{cod}:{ser}"] = {"inicio": first.fecha_efecto, "fin": None if pd.isna(last.fecha_fin_d) else str(last.fecha_fin_d.date()), "tramos": int(len(g))}
D["ITP_AJD_solapes"] = sol
D["ITP_AJD_huecos"] = hue
inicio_tarde = {k: v for k, v in cob.items() if pd.Timestamp(v["inicio"]) > H0 and k.split(":")[0] in CC}
fin_antes = {k: v for k, v in cob.items() if v["fin"] is not None and pd.Timestamp(v["fin"]) < H1 and k.split(":")[0] in CC}
D["ITP_AJD_series_que_empiezan_despues_de_2010-01-01"] = inicio_tarde
D["ITP_AJD_series_cerradas_antes_de_2026-12-31"] = fin_antes
D["ITP_AJD_CCAA_regimen_comun_sin_serie_AJD"] = sorted(CC - set(x[x.serie == "ajd"].cod_ine))
D["ITP_AJD_CCAA_regimen_comun_sin_serie_ITP"] = sorted(CC - set(x[x.serie == "itp_min"].cod_ine))
D["ITP_AJD_CCAA_presentes"] = sorted(set(x.cod_ine))
D["ITP_AJD_forales_con_tipos"] = x[x.cod_ine.isin(FORAL)][["id", "valor"]].values.tolist()
# años de calendario sin cobertura por CCAA y serie
anos_sin = {}
for (cod, ser), g in x[x.cod_ine.isin(CC)].groupby(["cod_ine", "serie"]):
    falta = []
    for y in range(2010, 2027):
        mid = pd.Timestamp(f"{y}-07-01")
        ok = ((g.fecha_efecto_d <= mid) & (g.fecha_fin_d.isna() | (g.fecha_fin_d >= mid))).any()
        if not ok:
            falta.append(y)
    if falta:
        anos_sin[f"{cod}:{ser}"] = falta
D["ITP_AJD_anyos_(1_julio)_sin_tramo_vigente"] = anos_sin
# valores plausibles
D["AJD_fuera_[0.25,2.5]"] = x[(x.serie == "ajd") & ((x.valor_n < .25) | (x.valor_n > 2.5))].id.tolist()
D["ITP_fuera_[4,11]"] = x[x.serie.str.startswith("itp") & ((x.valor_n < 4) | (x.valor_n > 11))].id.tolist()
D["ITP_valor_no_numerico"] = x[x.valor_n.isna()].id.tolist()
# máximo < mínimo en el mismo tramo
mm = x[x.serie.isin(["itp_min", "itp_max"])].pivot_table(index=["cod_ine", "fecha_efecto"], columns="serie", values="valor_n")
D["ITP_max_menor_que_min"] = [f"{i[0]}:{i[1]}" for i, r in mm.iterrows() if pd.notna(r.get("itp_max")) and pd.notna(r.get("itp_min")) and r.itp_max < r.itp_min]
D["ITP_max_sin_min_pareja_o_inversa"] = [f"{i[0]}:{i[1]}" for i, r in mm.iterrows() if (pd.isna(r.get("itp_max")) != pd.isna(r.get("itp_min"))) and pd.notna(r.get("itp_max"))]
# tramos con el mismo valor que el anterior (partición artificial)
rep = []
for (cod, ser), g in x.groupby(["cod_ine", "serie"]):
    g = g.sort_values("fecha_efecto_d")
    rep += [(cod, ser, a.id, b.id) for a, b in zip(g.itertuples(), g.iloc[1:].itertuples()) if a.valor_n == b.valor_n]
D["ITP_AJD_tramos_consecutivos_con_mismo_valor"] = rep
# fechas de efecto aproximadas (1 de enero) por nota
aprox = x[x.notas.str.contains("aproximada", na=False)]
D["ITP_AJD_filas_con_fecha_efecto_aproximada"] = int(len(aprox))
D["ITP_AJD_efecto_1_enero_n"] = int((x.fecha_efecto.str[5:] == "01-01").sum())
D["ITP_AJD_filas"] = int(len(x))
D["ITP_AJD_cambios_de_tipo_en_01-01_vs_otra_fecha"] = {"01-01": int((x.fecha_efecto.str[5:] == "01-01").sum()), "otra": int((x.fecha_efecto.str[5:] != "01-01").sum())}

# ---------- zonas tensionadas
z = d[d.instrumento == "zona_tensionada"]
dur = ((z.fecha_fin_d - z.fecha_efecto_d).dt.days / 365.25)
D["zonas_n"] = int(len(z))
D["zonas_duracion_anyos_percentiles"] = {str(q): round(float(dur.quantile(q)), 2) for q in (0, .05, .5, .95, 1)}
D["zonas_sin_fin"] = int(z.fecha_fin.isna().sum())
D["zonas_fin_anterior_a_2026-10-17"] = int((z.fecha_fin_d < "2026-10-17").sum())
sz = []
for cod, g in z.groupby("cod_ine"):
    g = g.sort_values("fecha_efecto_d")
    for a, b in zip(g.itertuples(), g.iloc[1:].itertuples()):
        if b.fecha_efecto_d <= a.fecha_fin_d:
            sz.append((cod, a.id, b.id))
D["zonas_solape_mismo_municipio"] = sz
D["zonas_municipios_distintos"] = int(z.cod_ine.nunique())
D["zonas_publicacion_a_efecto_dias_max"] = float((z.fecha_efecto_d - z.fecha_publicacion_d).dt.days.max())

# ---------- verificación y prioridad
D["verificacion_recuento"] = d.verificacion.str.extract(r"^(VERIFICADA|SECUNDARIA|NO VERIFICADA)")[0].value_counts().to_dict()
sec = d[d.verificacion.str.startswith(("SECUNDARIA", "NO VERIFICADA"))].copy()
POND = {"13": 5, "09": 5, "01": 4, "10": 4, "05": 3, "12": 3, "04": 3, "07": 2, "08": 2, "02": 1, "03": 1, "06": 1, "11": 1, "14": 1, "17": 1}  # peso aproximado por volumen de compraventas (criterio de orden, no de resultado)
rows = []
for r in sec.itertuples():
    pts, why = 0, []
    if r.verificacion.startswith("NO VERIFICADA"):
        pts += 10
        why.append("NO VERIFICADA")
    if r.instrumento in ("itp", "ajd"):
        w = POND.get(r.cod_ine, 1)
        pts += w
        why.append(f"peso CCAA {w}")
        prev = x[(x.cod_ine == r.cod_ine) & (x.serie == ("ajd" if r.instrumento == "ajd" else ("itp_max" if "máximo" in str(r.parametro) else "itp_min"))) & (x.fecha_efecto_d < r.fecha_efecto_d)]
        cambio = len(prev) > 0
        if cambio:
            pts += 2
            why.append("es un cambio de tipo (ancla de la fecha de efecto)")
        if "aproximada" in str(r.notas):
            pts += 2
            why.append("fecha de efecto aproximada")
        if r.fecha_efecto[5:] != "01-01":
            pts -= 1
            why.append("fecha exacta recogida por la fuente")
        if r.cod_ine in FORAL:
            pts += 0
    else:
        pts += 5
        why.append("instrumento no fiscal con verificación incompleta")
    rows.append((r.id, r.instrumento, r.cod_ine, r.fecha_efecto, r.verificacion[:40], pts, "; ".join(why)))
pr = pd.DataFrame(rows, columns=["id", "instrumento", "cod_ine", "fecha_efecto", "verificacion", "prioridad", "motivo"]).sort_values(["prioridad", "id"], ascending=[False, True])
pr["rango"] = np.arange(1, len(pr) + 1)
(SAL / "intervenciones").mkdir(parents=True, exist_ok=True)
pr.to_csv(SAL / "intervenciones" / "prioridad_verificacion.csv", index=False)
D["verificar_n"] = int(len(pr))
D["verificar_top25"] = pr.head(25)[["id", "prioridad"]].values.tolist()
D["verificar_no_verificadas"] = pr[pr.verificacion.str.startswith("NO")].id.tolist()
D["verificar_no_fiscales_secundarias"] = pr[~pr.instrumento.isin(["itp", "ajd"])].id.tolist()

res = base_resultado("v16/auditoria/intervenciones", "¿Es coherente y completa la base de intervenciones (fechas, tramos, cobertura) y qué filas verificar primero?",
                     "output/v16/f1/intervenciones.csv (476 filas, leído con dtype=str)", int(len(d)), "reglas deterministas sobre fechas, tramos y valores; prioridad por puntuación explícita", D,
                     ["La puntuación de prioridad es un criterio de orden de trabajo, no un resultado.", "Fecha de revisión 2026-10-17."])
INF = RAIZ / "output/v16/auditoria/intervenciones/informe.md"
if __name__ == "__main__":
    escribe("intervenciones", res, INF.read_text(encoding="utf-8") if INF.exists() else "(informe pendiente)")
    print(json.dumps(D, ensure_ascii=False, indent=1, default=str)[:15000])
