"""M5 · Evaluación de instrumentos con una rúbrica idéntica (v4). Se evalúan instrumentos, no partidos.

Entradas (sin red):
- data/raw/v4/medidas_programas.csv: anexo de procedencia. Solo se usa para contar en cuántos documentos aparece cada
  instrumento; los nombres de partido no se copian a ninguna salida.
- output/v3/PD/resultados.json: simulaciones P-D de v3 (rangos de elasticidades).
- output/v4/M3/clasificacion_municipios.csv: clases territoriales (C4, coste en nivel supuesto).
- docs/v4/literatura_v4.md y docs/v3/literatura_v3.md: estado de las referencias (aquí se citan, no se leen).
Rúbrica por instrumento: mecanismo · evidencia (capa y literatura) · efecto esperado con rango · plazo · coste fiscal ·
riesgos · distribución (quién gana y quién pierde) · dónde funciona (clase M3) · signo estable en la rejilla.
Salidas: output/v4/M5/matriz_instrumentos.csv y .md, incidencia_ayudas_demanda.csv, fichas_verificador.json, resultado.json.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
OUT = RAIZ / "output" / "v4" / "M5"
SEED = 20261010

CLASES = {1: "falta y brecha positiva moderada (coste supuesto)", 2: "falta y precio muy por encima de coste + suelo (coste supuesto)",
          3: "falta pero no rentable construir (coste supuesto)", 4: "no falta"}


def _n_docs() -> dict[str, set]:
    f = RAIZ / "data" / "raw" / "v4" / "medidas_programas.csv"
    if not f.exists():
        return {}
    d = pd.read_csv(f)
    col_ins = [c for c in d.columns if c.lower().startswith("instrumento")][0]
    col_doc = [c for c in d.columns if c.lower().startswith("documento")][0]
    d["id"] = d[col_ins].astype(str).str.split().str[0]
    return d.groupby("id")[col_doc].agg(lambda x: set(x)).to_dict()


def _pd() -> dict[str, tuple[float, float, str]]:
    f = RAIZ / "output" / "v3" / "PD" / "resultados.json"
    out = {}
    for x in json.loads(f.read_text()) if f.exists() else []:
        out[x["metrica"]] = (x["rango_min"], x["rango_max"], x["capa"])
    return out


def _r(pdres: dict, clave: str, unidad: str = "%") -> str:
    for k, (lo, hi, capa) in pdres.items():
        if k.startswith(clave):
            return f"{lo:,.1f} a {hi:,.1f} {unidad} ({capa}; P-D v3)".replace(",", "X").replace(".", ",").replace("X", ".")
    return "sin simulación"


def incidencia() -> pd.DataFrame:
    """Parte de una ayuda a la demanda que se traslada al precio (la captan los vendedores o arrendadores):
    |εd| / (εs + |εd|). Rejilla con rangos plausibles (supuestos, C4 en la convención A)."""
    filas = []
    for es in (0.2, 0.5, 1.0, 2.0):
        for ed in (0.3, 0.6, 1.0, 1.5):
            filas.append({"elasticidad_oferta": es, "elasticidad_demanda_abs": ed,
                          "parte_al_precio": ed / (es + ed), "parte_al_beneficiario": es / (es + ed)})
    return pd.DataFrame(filas)


def matriz(nd: dict, pdres: dict, inc: pd.DataFrame, clases: dict) -> list[dict]:
    lo_i, hi_i = inc.parte_al_precio.min(), inc.parte_al_precio.max()
    inc_txt = f"entre el {100 * lo_i:.0f} % y el {100 * hi_i:.0f} % de la ayuda se traslada al precio (rejilla de elasticidades, C4)"
    donde_oferta = f"clases 1-2 de M3 ({clases.get(1, 0) + clases.get(2, 0)} municipios; C4)"
    donde_rigida = f"clases 2-3 (oferta rígida o no rentable; {clases.get(2, 0) + clases.get(3, 0)} municipios; C4)"
    M = [
        dict(id="I02/N8", instrumento="Parque público o social de alquiler a gran escala", mecanismo="Oferta pública por debajo de mercado; saca demanda del mercado privado.",
             evidencia="C2 en P-D v3 (signo ≤ 0, nulo si desplaza a la construcción privada); Baum-Snow y Marion (2009, VERIFICADA, magnitud no extraída)",
             efecto=_r(pdres, "variación del esfuerzo medio nacional (25 mil/año"), plazo="largo (5-10 años)", coste="alto (coste unitario sin dato verificado)",
             riesgos="desplazamiento de la promoción privada; gestión y mantenimiento", distribucion="ganan los adjudicatarios; coste para contribuyentes",
             donde=donde_oferta, signo="≤ 0 (posiblemente nulo)"),
        dict(id="I04/I20", instrumento="Suelo público y colaboración público-privada (derecho de superficie, cooperativas)", mecanismo="Baja el coste del suelo para vivienda asequible.",
             evidencia="sin diseño propio; sin literatura verificada con magnitud", efecto="sin simulación propia", plazo="medio-largo",
             coste="medio (renuncia a ingresos por suelo)", riesgos="volumen limitado por el suelo público disponible", distribucion="ganan los adjudicatarios; coste de oportunidad del suelo",
             donde=donde_oferta, signo="sin evaluar"),
        dict(id="P1", instrumento="Más construcción (cualquier vía) donde falta", mecanismo="Aumenta la oferta neta frente a la creación de hogares.",
             evidencia="C2 en P-D v3 (signo estable en toda la rejilla); M1 (déficit 2021-2024 C1 sin bajas)",
             efecto=_r(pdres, "variación del esfuerzo medio con +50 mil"), plazo="medio-largo", coste="depende de la vía (pública o privada)",
             riesgos="cuellos de botella de suelo, licencias y capacidad del sector (M3, sin datos verificados de coste)", distribucion="ganan los hogares entrantes; pierden los propietarios con plusvalías esperadas",
             donde=donde_oferta, signo="sí (estricto)"),
        dict(id="N1/I13", instrumento="Agilización de licencias y seguridad jurídica urbanística", mecanismo="Menos plazo e incertidumbre del permiso: oferta más elástica.",
             evidencia="Hilber y Vermeulen (2016, VERIFICADA, magnitud no extraída); sin datos de plazos en España (S8)", efecto="sin simulación propia", plazo="corto-medio",
             coste="bajo", riesgos="menor control de calidad o de impacto", distribucion="ganan promotores y compradores futuros", donde=donde_oferta, signo="sin evaluar"),
        dict(id="N2", instrumento="Aumento de edificabilidad o densidad", mecanismo="Eleva el techo de oferta en suelo ya urbano.",
             evidencia="Saiz (2010) y Glaeser-Gyourko (2018), VERIFICADAS (calibración)", efecto="sin simulación propia", plazo="medio", coste="bajo",
             riesgos="congestión y servicios públicos", distribucion="ganan los propietarios de suelo y los compradores futuros", donde=donde_oferta, signo="sin evaluar"),
        dict(id="I12/N5", instrumento="Industrialización de la construcción", mecanismo="Menos coste y plazo por vivienda.",
             evidencia="sin referencia verificada (NO VERIFICADA)", efecto="sin simulación propia", plazo="medio", coste="bajo-medio (incentivos)",
             riesgos="escala mínima de mercado", distribucion="ganan compradores si baja el coste", donde="clase 3 de M3 (no rentable a coste actual; C4)", signo="sin evaluar"),
        dict(id="I10/I27/N7", instrumento="Movilización de vivienda vacía (incentivos, registro, recargo o impuesto)", mecanismo="Pone en uso vivienda desocupada.",
             evidencia="C2 en P-D v3 (signo estable); Segú (2020, VERIFICADA): la vacancia cae un 13 % relativo en Francia",
             efecto=_r(pdres, "variación del esfuerzo medio nacional (10 %)") + "; aporte máximo con el 30 %: " + _r(pdres, "aporte máximo (30 %)", "% de la brecha"),
             plazo="corto-medio", coste="bajo (el recargo recauda)", riesgos="vacías mal medidas (Censo por consumo eléctrico; C4); solo el 27-40 % está donde hay presión",
             distribucion="pierden los propietarios de vacías; ganan los inquilinos donde hay presión", donde="municipios del tercil alto de presión", signo="sí (estricto)"),
        dict(id="I01", instrumento="Regulación de precios del alquiler (topes, zonas tensionadas)", mecanismo="Limita la renta de los contratos nuevos o su crecimiento.",
             evidencia="C4 propio (H3-3: −5,4 % renta en Cataluña 2020-2022; fuera de C3); Jofre-Monseny et al. (2023, VERIFICADA, Q1): −4,5 %; Diamond et al. (2019, VERIFICADA, Q1): −15 % de oferta en San Francisco",
             efecto=_r(pdres, "variación del esfuerzo medio de los inquilinos"), plazo="inmediato", coste="bajo (administrativo)",
             riesgos="reducción de oferta o desvío a otros usos (contratos −4,9 % [−9,9; +0,5], C4)", distribucion="ganan los inquilinos con contrato; pueden perder los que buscan vivienda y los arrendadores",
             donde=donde_rigida, signo="no (depende de la respuesta de la oferta)"),
        dict(id="I16", instrumento="Regulación del alquiler turístico y de temporada", mecanismo="Devuelve viviendas al alquiler residencial.",
             evidencia="C2 de cantidad (≤2,7 % del stock de alquiler 2020-2024); C4 en precio (H3-1 sellado sin distinguirse de 0)",
             efecto=_r(pdres, "variación del esfuerzo medio nacional con X = 50 %"), plazo="corto", coste="bajo",
             riesgos="desvío a temporada o habitaciones; efecto local mayor que el nacional", distribucion="pierden los titulares de VUT y el sector turístico; ganan inquilinos locales",
             donde="secciones con alto peso de VUT", signo="no"),
        dict(id="I06/I07/I08/I09/N9", instrumento="Ayudas a la demanda (avales, ayudas al alquiler, fiscalidad de la compra)", mecanismo="Reduce el coste para el beneficiario.",
             evidencia="Gibbons y Manning (2006, VERIFICADA): 60-67 % de la incidencia en arrendadores; Carozzi, Hilber y Yu (2024, VERIFICADA, Q1): precios al alza sin más construcción donde la oferta es rígida",
             efecto=inc_txt, plazo="inmediato", coste="alto y recurrente (ayudas) o diferido (avales: riesgo contingente)",
             riesgos="capitalización en precios y rentas con oferta rígida", distribucion="ganan los beneficiarios (en parte) y los vendedores o arrendadores; pierden los no beneficiarios que compran o alquilan",
             donde="mayor eficacia donde la oferta es elástica; menor en las clases 2-3 de M3", signo="no (para el conjunto del mercado)"),
        dict(id="I14", instrumento="Seguridad jurídica del propietario y procedimientos de desalojo", mecanismo="Menor riesgo percibido: más oferta de alquiler.",
             evidencia="sin datos (V09; solicitud S10)", efecto="sin simulación propia", plazo="corto-medio", coste="bajo (administración de justicia)",
             riesgos="hogares vulnerables sin alternativa habitacional", distribucion="ganan los arrendadores; pueden perder hogares vulnerables", donde="sin dato territorial", signo="sin evaluar"),
        dict(id="I05/N6/I26/N3", instrumento="Captura de plusvalías y fiscalidad del suelo (suelo ocioso, impuesto sobre el valor del suelo)", mecanismo="Recupera rentas del suelo e incentiva su uso.",
             evidencia="sin referencia verificada con magnitud (NO VERIFICADA)", efecto="sin simulación propia", plazo="medio-largo", coste="recauda",
             riesgos="valoración y litigiosidad", distribucion="pierden los propietarios de suelo; ganan las administraciones y los compradores futuros", donde=donde_oferta, signo="sin evaluar"),
        dict(id="I21", instrumento="Limitación de compras de no residentes o con fin de inversión", mecanismo="Reduce la demanda de inversión.",
             evidencia="peso de compradores extranjeros no residentes ≈7 % de las compraventas (MIVAU, C4); sin diseño sobre el precio",
             efecto="sin simulación propia", plazo="inmediato", coste="bajo", riesgos="desplazamiento a otros vehículos de inversión",
             distribucion="pierden vendedores en zonas costeras e islas; posible alivio local", donde="costa e islas (supuesto declarado en M4)", signo="sin evaluar"),
        dict(id="I29", instrumento="Reducción de tributos sobre la promoción y construcción", mecanismo="Baja el coste de producir vivienda.",
             evidencia="sin diseño propio; la incidencia depende de la elasticidad de oferta (V10)", efecto="sin simulación propia", plazo="medio", coste="medio (menor recaudación)",
             riesgos="captura por el precio del suelo con oferta rígida", distribucion="ganan promotores y, en parte, compradores", donde="clase 3 de M3 (no rentable a coste actual; C4)", signo="sin evaluar"),
    ]
    for m in M:
        ids = m["id"].split("/")
        m["n_documentos"] = len(set().union(*[nd.get(i, set()) for i in ids]))   # documentos distintos
    return M


def fichas(inc: pd.DataFrame) -> list[dict]:
    lo_i, hi_i = inc.parte_al_precio.min(), inc.parte_al_precio.max()
    m1 = json.loads((RAIZ / "output" / "v4" / "M1" / "hechos.json").read_text())
    return [
        dict(id="M5-V1", tema="Ayudas a la demanda", enunciado="Las ayudas a los jóvenes para comprar o alquilar abaratan su acceso a la vivienda.",
             capa="C4", magnitud=(f"Con la rejilla de elasticidades (oferta 0,2-2; demanda 0,3-1,5), entre el {100 * lo_i:.0f} % y el {100 * hi_i:.0f} % "
                                  "de la ayuda se traslada al precio o la renta. El beneficiario paga menos en neto, salvo con oferta totalmente rígida; "
                                  "los no beneficiarios pagan más."),
             intervalo=f"{100 * lo_i:.0f}-{100 * hi_i:.0f} % de la ayuda al precio", cota="C4: depende de elasticidades sin estimación española verificada",
             literatura="Gibbons y Manning (2006), JPubE, VERIFICADA, cuartil no verificado: 60-67 % de incidencia en arrendadores; Carozzi, Hilber y Yu (2024), JUE, VERIFICADA, Q1.",
             veredicto="ANALIZADA, NO CONCLUYENTE",
             regla=("Para el beneficiario la ayuda reduce el coste neto en casi toda la rejilla, pero «abaratar el acceso» para los jóvenes en "
                    "conjunto depende de cuánto se traslade al precio, que no está estimado para España. Capa C4: como máximo no concluyente."),
             limites="Sin evaluación verificada de los avales ICO ni de las ayudas españolas.", evidencia=["output/v4/M5/incidencia_ayudas_demanda.csv"],
             convenciones={"A (estricta: traducción a precio en C4)": "ANALIZADA, NO CONCLUYENTE",
                           "B (estructural: traducción a precio como C2)": "PARCIALMENTE: abarata para el beneficiario y encarece para los no beneficiarios en toda la rejilla."}),
        dict(id="M5-V2", tema="Geografía del déficit", enunciado="Faltan viviendas en toda España.",
             capa="C4", magnitud=("2021-2025: ninguna provincia con excedente; 7 provincias suman el 50 % del déficit y 19 el 80 %; "
                                  "249 municipios con excedente (71 mil viviendas). Hechos de M1 en C4 (hogares provinciales de fuente única)."),
             intervalo="7 provincias = 50 % del déficit", cota="—", literatura="—", veredicto="ANALIZADA, NO CONCLUYENTE",
             regla="Hay déficit en todas las provincias, pero muy concentrado y con municipios en excedente; capa C4 (fuente única de hogares provinciales).",
             limites="Los municipios usan Catastro (sin territorios forales). " + (m1[0].get("limites", [""])[0] if m1 and isinstance(m1[0].get("limites"), list) else ""),
             evidencia=["output/v4/M1/hechos.json"]),
        dict(id="M5-V3", tema="Demografía", enunciado="Los hogares crecen por la inmigración.",
             capa="C4", magnitud=("2021-2025: hogares +1,01 millones (C1: ECP y EPA corregida). En la descomposición contable, el componente de "
                                  "población de nacionalidad extranjera supone el 56-58 % (rango 53-76 % según la corrección de la EPA), con jefatura "
                                  "de fuente única (C4)."),
             intervalo="56-58 % de ΔH (componente contable)", cota="—", literatura="—", veredicto="ANALIZADA, NO CONCLUYENTE",
             regla=("La descomposición es contable, no causal, y sus componentes son C4. Es compatible con la afirmación como descripción del "
                    "crecimiento de hogares 2021-2025; no lo es para 2008-2013, cuando el componente extranjero fue ≈0."),
             limites="Nacionalidad, no país de nacimiento; sin migración interior.", evidencia=["output/v4/M2/hechos.json"]),
        dict(id="M5-V4", tema="Compras de no residentes", enunciado="Limitar las compras de no residentes bajaría los precios de la vivienda.",
             capa="C4", magnitud="Compradores extranjeros no residentes ≈7 % de las compraventas en 2025 (MIVAU), concentrados en costa e islas (C4). Sin diseño sobre el precio.",
             intervalo="≈7 % de las compraventas", cota="—", literatura="—", veredicto="ANALIZADA, NO CONCLUYENTE",
             regla="Hay un peso descriptivo (C4), pero ningún diseño ni cota sobre el precio.", limites="Fuentes no independientes (MIVAU y Notariado).",
             evidencia=["output/v4/M4/hechos.json"]),
        dict(id="M5-V5", tema="Fiscalidad de la construcción", enunciado="Bajar los impuestos a la construcción abarataría la vivienda.",
             capa="C4", magnitud="Sin diseño ni datos de incidencia; con oferta rígida parte de la rebaja puede trasladarse al precio del suelo.",
             intervalo="n/d", cota="—", literatura="—", veredicto="NO ANALIZADA: FALTAN DATOS",
             regla="Falta una serie de cargas tributarias de la promoción por municipio y una estimación de la elasticidad de oferta.", limites="—", evidencia=[]),
    ]


def main() -> dict:
    (OUT / "tablas").mkdir(parents=True, exist_ok=True)
    nd, pdres, inc = _n_docs(), _pd(), incidencia()
    cm = RAIZ / "output" / "v4" / "M3" / "clasificacion_municipios.csv"
    clases = pd.read_csv(cm).clase_modal.value_counts().to_dict() if cm.exists() else {}
    M = matriz(nd, pdres, inc, clases)
    df = pd.DataFrame(M)
    df.to_csv(OUT / "matriz_instrumentos.csv", index=False)
    inc.to_csv(OUT / "tablas" / "incidencia_ayudas_demanda.csv", index=False)
    cols = ["id", "instrumento", "n_documentos", "evidencia", "efecto", "plazo", "coste", "riesgos", "distribucion", "donde", "signo"]
    md = ("# Matriz de instrumentos (M5)\n\nRúbrica idéntica para todos. Se evalúan instrumentos, no partidos: la procedencia de las "
          "medidas está en data/raw/v4/medidas_programas.csv. «n_documentos» cuenta en cuántos documentos (de los analizados) aparece "
          "el instrumento; 0 = no propuesto. «Signo» = signo estable del efecto sobre el esfuerzo de acceso en la rejilla simulada. "
          "Ninguna simulación incluye costes; la ordenación no es coste-beneficio.\n\n"
          "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
          + "".join("| " + " | ".join(str(r[c]) for c in cols) + " |\n" for r in M))
    (OUT / "matriz_instrumentos.md").write_text(md, encoding="utf-8")
    fs = fichas(inc)
    (OUT / "fichas_verificador.json").write_text(json.dumps(fs, ensure_ascii=False, indent=1))
    res = {"rama": "M5", "pregunta": "¿Qué instrumentos funcionarían, con la misma vara?", "capa": "C2/C4",
           "datos": "medidas_programas.csv (procedencia), P-D v3, M3, literatura v3/v4", "N": len(M), "metodo": "rúbrica idéntica; incidencia con rejilla de elasticidades",
           "estimacion": {"signo_estable_estricto": [m["id"] for m in M if m["signo"].startswith("sí")],
                          "signo_debil": [m["id"] for m in M if m["signo"].startswith("≤")],
                          "signo_no_estable": [m["id"] for m in M if m["signo"].startswith("no")],
                          "sin_evaluar": [m["id"] for m in M if m["signo"].startswith("sin")]},
           "ic95": None, "p_ajustado": None, "nivel_evidencia": "EXPLORATORIO (C4) salvo filas C2 de P-D",
           "diagnosticos": {"incidencia_rango": [float(inc.parte_al_precio.min()), float(inc.parte_al_precio.max())]},
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None}, "notas": "SEED sin uso (determinista)"}
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    return res


if __name__ == "__main__":
    np.random.seed(SEED)
    print(json.dumps(main()["estimacion"], ensure_ascii=False))
