"""V17 · Fase 3 · Auditoría del grupo «regulacion_ayudas» (topes, regulación turística, ayudas a la demanda).

ANÁLISIS A POSTERIORI (V17), capa C4. Solo aritmética sobre cifras ya publicadas por terceros (fichas de literatura
versionadas en docs/v15/literatura y docs/v16/literatura) y sobre cifras del proyecto (output/v5/cifras_clave.csv y
output/v17/lectura_bde/v15_v16_micro/inferencia.csv). No estima ningún modelo nuevo: no hay especificación que registrar
en el Registry. Sin red. SEED = 20261010 (no hay nada aleatorio). No lee data/raw, data/base ni data/sealed, de modo que
ninguna fila muestra_sellada_v6 entra en el cálculo.

Uso: python3 src/v17/f3_regulacion_ayudas.py
Salida: output/v17/auditoria/regulacion_ayudas_hechos.json
"""
from __future__ import annotations

import csv
import json
import math
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEED = 20261010
OUT = ROOT / "output" / "v17" / "auditoria" / "regulacion_ayudas_hechos.json"
L1 = ROOT / "docs" / "v16" / "literatura" / "L1_control_alquileres_efectos.csv"
L5 = ROOT / "docs" / "v16" / "literatura" / "L5_ayudas_demanda_efectos.csv"
INF = ROOT / "output" / "v17" / "lectura_bde" / "v15_v16_micro" / "inferencia.csv"
CIFRAS = ROOT / "output" / "v5" / "cifras_clave.csv"
FECHA = "2026-10-19"
FICHA = "output/v17/auditoria/filas/{}.md"

# Cifras de documentos leídos que no están en los CSV de efectos (fuente y lectura en cada ficha de la auditoría).
DOC = {
    # Fack (2006), Labour Economics 13(6), DOI 10.1016/j.labeco.2006.01.001: 78 céntimos de alquiler por euro (resumen).
    "fack2006_theta": 0.78,
    # Gibbons y Manning (2006), JPubE 90(4-5), DOI 10.1016/j.jpubeco.2005.01.002: 60 % a dos tercios sobre el arrendador.
    "gm2006_theta_min": 0.60, "gm2006_theta_max": 2 / 3,
    # Bono Alquiler Joven (RD 42/2022): 250 euros al mes.
    "bono_eur_mes": 250.0,
    # García-López et al. (2020), JUE 119, 103278 (versión de trabajo leída en P5): 54 anuncios -> +1,9 %; 200 -> +7 %.
    "gl_anuncios_medio": 54, "gl_alquiler_medio": 1.9, "gl_anuncios_d10": 200, "gl_alquiler_d10": 7.0,
    "gl_areas": 220,
    # Gyódi, Mazur y Cocola-Gant (2025), Cities, DOI 10.1016/j.cities.2025.105915 (resumen): 10.700 frente a 20.000.
    "gyodi_medidos": 10_700, "gyodi_contrafactual": 20_000,
    # Monràs y García-Montalvo, UPF WP 1836, tabla IV (leída en docs/v16/literatura/L1, sección 4): PPML por tramo.
    "mm_ppml_arriba": -0.449, "mm_ppml_abajo": 0.342,
}

HECHOS: list[dict] = []


def hecho(id_, indicador, valor, minimo, maximo, unidad, periodo, cobertura, fuentes, lectura, ficha, nota=""):
    assert lectura in ("OF", "hecho", "cota", "asociación", "juicio experto", "no fiable", "no se puede saber", "sin cambio")
    r = lambda x: None if x is None else round(float(x), 4)
    HECHOS.append({"id": f"V17-AUD-RA-{id_}", "indicador": indicador, "valor": r(valor), "min": r(minimo), "max": r(maximo),
                   "unidad": unidad, "periodo": periodo, "cobertura": cobertura, "fuentes": fuentes, "capa": "C4",
                   "lectura_v17": lectura, "fecha_dato": FECHA, "ficha": FICHA.format(ficha),
                   "nota": "a posteriori" + (f"; {nota}" if nota else "")})


def leer(p: Path) -> list[dict]:
    with p.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def fila(filas, **cond) -> dict:
    out = [f for f in filas if all(f.get(k) == v for k, v in cond.items())]
    assert len(out) == 1, (cond, len(out))
    return out[0]


def pnorm2(z: float) -> float:
    return math.erfc(abs(z) / math.sqrt(2))


# ------------------------------------------------------------------ topes
def topes() -> dict:
    l1 = leer(L1)
    def busca(autor, resultado, fuente):
        c = [f for f in l1 if autor in f["autores_anio"] and f["resultado"] == resultado and f["fuente_cifra"] == fuente]
        assert len(c) == 1, (autor, resultado, fuente)
        return c[0]
    jm = busca("Jofre", "oferta_contratos", "tabla 3, columna 2")
    mm = busca("Monràs y García-Montalvo (2022)", "oferta_contratos", "tabla IV, columna 1")
    b_jm, s_jm = float(jm["estimacion"]), float(jm["ee"])
    b_mm, s_mm = float(mm["estimacion"]), float(mm["ee"])
    ic_jm = (b_jm - 1.96 * s_jm, b_jm + 1.96 * s_jm)
    ic_mm = (b_mm - 1.96 * s_mm, b_mm + 1.96 * s_mm)
    solape = (max(ic_jm[0], ic_mm[0]), min(ic_jm[1], ic_mm[1]))
    z = (b_jm - b_mm) / math.sqrt(s_jm ** 2 + s_mm ** 2)
    hecho("TOP-CONTRATOS-DIF", "Diferencia entre las estimaciones de contratos nuevos de Jofre-Monseny et al. (0,001) y "
          "Monràs y García-Montalvo (-0,102), Ley 11/2020 (valor: diferencia en log; min/max: IC 95 % de la diferencia "
          "suponiendo independencia)",
          b_jm - b_mm, b_jm - b_mm - 1.96 * math.hypot(s_jm, s_mm), b_jm - b_mm + 1.96 * math.hypot(s_jm, s_mm), "log contratos", "2016-2022", "Cataluña, municipios",
          "docs/v16/literatura/L1_control_alquileres_efectos.csv (tablas de los autores)", "juicio experto", "topes",
          f"z = {z:.2f}, p bilateral = {pnorm2(z):.4f} suponiendo independencia; los IC 95 % de cada estudio solo se "
          f"solapan entre {solape[0]:.3f} y {solape[1]:.3f}; las muestras se solapan (mismo registro de "
          "Incasòl), por lo que el contraste es solo orientativo")
    base = float(busca("Monràs y García-Montalvo (2022)", "renta_contratos_regulados", "tabla I, panel B, columna 1")["estimacion"])
    fe_v = float(busca("Monràs y García-Montalvo (2022)", "renta_contratos_regulados", "tabla I, panel B, columna 4")["estimacion"])
    share = (base - fe_v) / base
    hecho("TOP-COMPOSICION", "Parte de la caída de la renta media atribuible a composición en Monràs y García-Montalvo "
          "(1 - coef. con efectos fijos de vivienda / coef. base)", 100 * share, None, None, "% de la caída", "2016-2021",
          "Cataluña", "Monràs y García-Montalvo, UPF WP 1836, tabla I (leída en docs/v16/literatura/L1)", "juicio experto",
          "topes", "los autores hablan de «la mitad»; el cociente con sus coeficientes da en torno a dos quintos")
    hecho("TOP-TRAMO-ARRIBA", "Contratos nuevos por encima de la referencia (PPML, exp(b)-1)",
          100 * (math.exp(DOC["mm_ppml_arriba"]) - 1), None, None, "%", "2016-2021", "Cataluña",
          "Monràs y García-Montalvo, UPF WP 1836, tabla IV", "juicio experto", "topes")
    hecho("TOP-TRAMO-ABAJO", "Contratos nuevos por debajo de la referencia (PPML, exp(b)-1)",
          100 * (math.exp(DOC["mm_ppml_abajo"]) - 1), None, None, "%", "2016-2021", "Cataluña",
          "Monràs y García-Montalvo, UPF WP 1836, tabla IV", "juicio experto", "topes")
    inf = leer(INF)
    res = {}
    for ide in ("H1-CS", "H1-SDID", "H2-CS", "H2-SDID", "H2-PPML", "Q1c-global", "Q1c-sin-grandes"):
        f = fila(inf, id_resultado=ide)
        res[ide] = (float(f["estimacion_publicada"]), f["p_conv"], f["tamano_real"], f["publicable"])
    f = fila(inf, id_resultado="H2-SDID")
    hecho("TOP-H2-SDID", "H2 (V15), contratos nuevos en zonas tensionadas de Cataluña 2024, SDID: lectura convencional "
          "(valor: estimación; min/max: IC 95 % Webb)", float(f["estimacion_publicada"]), float(f["ic95_lo"]),
          float(f["ic95_hi"]), "%", "2024T2-2026T1", "Cataluña, municipios",
          "output/v17/lectura_bde/v15_v16_micro/inferencia.csv (H2-SDID); id publicado V15-H2-sdid-att", "asociación",
          "topes", f"p = {f['p_conv']}, tamaño real {f['tamano_real']}; H2-CS y H2-PPML no fiables (tamaño > 15 %); "
          "pretendencias de contratos rechazadas en V9-D1a; no se cambia la lectura publicada")
    return {"z": z, "solape": solape, "composicion": share, "inferencia": res}


# ------------------------------------------------------------------ turística
def turistica() -> dict:
    por_anuncio = DOC["gl_alquiler_medio"] / DOC["gl_anuncios_medio"]
    por_anuncio_d10 = DOC["gl_alquiler_d10"] / DOC["gl_anuncios_d10"]
    assert abs(por_anuncio - por_anuncio_d10) < 0.002   # el efecto de García-López et al. es casi lineal en anuncios
    evitados = DOC["gyodi_contrafactual"] - DOC["gyodi_medidos"]
    por_area = evitados / DOC["gl_areas"]
    efecto = por_area * por_anuncio
    hecho("TUR-BCN-TRASLACION", "Traslación orientativa a alquiler del freno a los anuncios en Barcelona: anuncios evitados "
          "según el contrafactual de Gyódi et al. (2025) repartidos por igual entre las 220 áreas de García-López et al. "
          "(2020) y multiplicados por su efecto por anuncio (valor: reparto uniforme; min: solo la mitad de los anuncios "
          "evitados vuelve al alquiler residencial; max: los anuncios evitados se concentran en la mitad de las áreas)",
          efecto, 0.5 * efecto, 2 * efecto, "% de alquiler (área media)", "2015-2023",
          "Barcelona", "Gyódi, Mazur y Cocola-Gant (2025, DOI 10.1016/j.cities.2025.105915, resumen); García-López et al. "
          "(2020, DOI 10.1016/j.jue.2020.103278, P5)", "juicio experto", "turistica_regulacion",
          "combina un contrafactual descriptivo de anuncios con una elasticidad de 2007-2017; supone linealidad y que cada "
          "anuncio evitado es una vivienda residencial; no es una evaluación de la norma")
    inf = leer(INF)
    q2a = fila(inf, id_resultado="Q2a")
    hecho("TUR-Q2A", "Q2a (V16) con inferencia convencional: Δlog IPC de alquiler por DT del log de la exposición turística "
          "(valor: estimación; min/max: IC 95 %)", float(q2a["estimacion_publicada"]), float(q2a["ic95_lo"]),
          float(q2a["ic95_hi"]), "Δlog por DT", "2017-2019 frente a 2022-2025", "41 provincias de entrenamiento",
          "output/v17/lectura_bde/v15_v16_micro/inferencia.csv (Q2a); id publicado V16-Q2-1", "asociación",
          "turistica_regulacion", f"p = {q2a['p_conv']}; tamaño real {q2a['tamano_real']} (cerca del límite del 15 %); "
          "mide densidad, no regulación; depende de controles y fecha de exposición")
    return {"efecto_medio": efecto, "por_area": por_area}


# ------------------------------------------------------------------ ayudas
def ayudas() -> dict:
    l5 = leer(L5)
    centrales = {}
    for f in l5:
        if f["medida"] not in ("renta de mercado (existente)", "renta de mercado (cupones)", "renta de mercado (nuevos contratos)"):
            continue
        if not f["unidad_efecto"].startswith(("euros de alquiler", "centavos", "proporción", "dólares")):
            continue
        txt = f["estimacion"].replace(" a ", "-")
        try:
            v = float(txt)
        except ValueError:
            a, b = txt.split("-")
            v = (float(a) + float(b)) / 2
        centrales.setdefault(f["ficha"], []).append(v)
    # Un valor por estudio: el primero (columna principal) de cada ficha; Fack se sustituye por la cifra del resumen de 2006.
    por_estudio = {k: v[0] for k, v in centrales.items()}
    por_estudio["Fack"] = DOC["fack2006_theta"]
    por_estudio["GibbonsManning"] = (DOC["gm2006_theta_min"] + DOC["gm2006_theta_max"]) / 2
    thetas = sorted(por_estudio.values())
    med = statistics.median(thetas)
    hecho("AYU-RETIENE-MEDIANA", "Parte de la ayuda al alquiler que retiene el beneficiario (1 - traslación), mediana entre "
          f"{len(thetas)} estudios con diseño (valor: mediana; min/max: estudio con más y con menos traslación)",
          100 * (1 - med), 100 * (1 - max(thetas)), 100 * (1 - min(thetas)), "% de la ayuda", "1984-2020",
          "Francia, Reino Unido, EE. UU., Finlandia, Nueva Zelanda",
          "docs/v16/literatura/L5_ayudas_demanda_efectos.csv; Fack (2006) y Gibbons y Manning (2006), resúmenes",
          "juicio experto", "ayudas_demanda",
          "estudios con diseño distinto y no independientes entre países; Collinson y Ganong incluyen algo de calidad; "
          "Fack (2005) DDD supera 1 con error grande")
    lo = DOC["bono_eur_mes"] * (1 - max(thetas))
    hi = DOC["bono_eur_mes"] * (1 - min(thetas))
    hecho("AYU-BONO-RETIENE", "Euros al mes del Bono Alquiler Joven (250) que retendría el beneficiario con las traslaciones "
          "de la literatura (valor: mediana de los estudios; min: Fack 2006, 78 %; max: Eerola et al. 2026, 3,6 %)",
          DOC["bono_eur_mes"] * (1 - med), lo, hi, "euros al mes", "escenario", "España (sin evaluación propia)",
          "RD 42/2022 (250 euros); traslaciones de la literatura", "juicio experto", "ayudas_demanda",
          "traslado mecánico de magnitudes de otros países; no es una estimación sobre España")
    inf = leer(INF)
    q7 = fila(inf, id_resultado="Q7")
    hecho("AYU-Q7", "Q7a (V16) con inferencia convencional: diferencia en discontinuidades del log del alquiler en el corte de "
          "35 años (valor: estimación; min/max: IC 95 %)", float(q7["estimacion_publicada"]), float(q7["ic95_lo"]),
          float(q7["ic95_hi"]), "Δlog", "2018-2021 / 2023-2025", "inquilinos de mercado de la ECV",
          "output/v17/lectura_bde/v15_v16_micro/inferencia.csv (Q7); id publicado V16-Q7-1", "no se puede saber",
          "ayudas_demanda", f"p = {q7['p_conv']}; distorsión sin medir; placebos de edad del mismo orden (V16-Q7-4)")
    return {"thetas": por_estudio, "mediana": med}


def cifra_publicada(ide: str) -> str:
    return fila(leer(CIFRAS), id=ide)["valor"]


def main() -> dict:
    HECHOS.clear()
    r = {"topes": topes(), "turistica": turistica(), "ayudas": ayudas()}
    # Comprobación: las cifras del proyecto que se citan siguen como están publicadas.
    r["publicadas"] = {i: cifra_publicada(i) for i in ("V9-D1b-renta-att", "V9-D1b-contratos-att", "V9-D1a-contratos-att",
                                                         "B4-v3-vut-cantidad", "V16-Q7-1", "D1-H11")}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(HECHOS, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return r


if __name__ == "__main__":
    res = main()
    print(json.dumps({k: v for k, v in res.items() if k != "publicadas"}, ensure_ascii=False, indent=1, default=str))
    print(json.dumps(res["publicadas"], ensure_ascii=False))
