"""D1 · Matriz completa de instrumentos (I01-I29 y N1-N9) con rúbrica idéntica y traslado de ayudas por clase A4. Sin red.

Entradas versionadas: output/v4/M5 (vía src/v4/m5_run.matriz), output/v3/PD/resultados.json, docs/v4/instrumentos.md,
output/v5/D1/literatura_instrumentos.csv (no se sobrescribe), output/v5/A4/clasificacion_provincias.csv, output/v5/A5/recuentos.csv.
Se evalúan instrumentos, no actores. Donde faltan datos o literatura: «No evaluable: <motivo>».
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v4"))
import m5_run as m5  # noqa: E402

OUT = RAIZ / "output" / "v5" / "D1"
SEED = 20261010
FECHA = "2026-10-10"
ALIAS = {"N5": "I12", "N6": "I05", "N7": "I10", "N8": "I02", "N9": "I08"}   # equivalencias de agrupación v4
ED = (0.3, 0.6, 1.0, 1.5)   # |elasticidad de la demanda|, rejilla de P-D v3
GRID_ES = {1: 1.75, 2: 0.0, 3: 0.45}   # método B: rejilla de oferta de P-D v3 asignada a la clase (supuesto)
PRIV = "sin cifra oficial de coste incorporada al proyecto"


def tax() -> dict[str, tuple[str, str]]:
    t = {}
    for ln in (RAIZ / "docs" / "v4" / "instrumentos.md").read_text(encoding="utf-8").splitlines():
        c = [x.strip() for x in ln.strip("|").split("|")]
        if len(c) >= 3 and re.fullmatch(r"[IN]\d+", c[0]):
            t[c[0]] = (c[1], c[2])
    return t


def es_por_clase(a: pd.DataFrame) -> dict[int, dict]:
    """Método A: elasticidad de oferta por clase = respuesta de oferta A4 (C4), recortada a >= 0 (una elasticidad negativa no
    es admisible como parámetro de incidencia; supuesto declarado). Central = mediana; rango = percentiles 25-75."""
    out = {}
    for k, g in a.groupby("clase_2021_2025"):
        r = g.resp_oferta.clip(lower=0)
        out[int(k)] = dict(n=len(g), central=float(r.median()), lo=float(r.quantile(.25)), hi=float(r.quantile(.75)))
    return out


def incidencia_clase(es: dict) -> pd.DataFrame:
    f = []
    for k, e in es.items():
        if k == 9:
            f.append(dict(clase=k, metodo="A", es_lo=np.nan, es_central=np.nan, es_hi=np.nan, parte_precio_min=np.nan,
                          parte_precio_central=np.nan, parte_precio_max=np.nan, nota="No evaluable: clase sin dato de respuesta de oferta fiable"))
            continue
        for met, (lo, c, hi) in (("A", (e["lo"], e["central"], e["hi"])), ("B", (GRID_ES[k],) * 3) if k in GRID_ES else ((np.nan,) * 3)):
            p = [ed / (es_ + ed) for es_ in (lo, c, hi) for ed in ED]
            pc = [ed / (c + ed) for ed in ED]
            f.append(dict(clase=k, metodo=met, es_lo=lo, es_central=c, es_hi=hi, parte_precio_min=min(p), parte_precio_central=float(np.median(pc)),
                          parte_precio_max=max(p), nota="C4; |εd| en {0,3; 0,6; 1,0; 1,5}"))
    return pd.DataFrame(f)


def pct(x: float) -> str:
    return f"{100 * x:.0f} %"


def main() -> dict:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    pdres, inc = m5._pd(), m5.incidencia()
    base = {r["id"]: r for r in m5.matriz({}, pdres, inc, {})}
    t = tax()
    a = pd.read_csv(RAIZ / "output" / "v5" / "A4" / "clasificacion_provincias.csv", dtype={"cod_prov": str})
    es = es_por_clase(a)
    ic = incidencia_clase(es)
    ic.to_csv(OUT / "incidencia_ayudas_por_clase.csv", index=False)
    rec = pd.read_csv(RAIZ / "output" / "v5" / "A5" / "recuentos.csv").set_index("instrumento")
    lit = pd.read_csv(OUT / "literatura_instrumentos.csv")
    n_clase = a.clase_2021_2025.value_counts().to_dict()

    def f(c, m):
        r = ic[(ic.clase == c) & (ic.metodo == m)].iloc[0]
        return r

    def txt_clase(c):
        ra, rb = f(c, "A"), (f(c, "B") if c in GRID_ES else None)
        s = (f"clase {c} ({n_clase.get(c, 0)} prov.): método A (respuesta de oferta A4, εs {ra.es_lo:.2f}-{ra.es_hi:.2f}, central {ra.es_central:.2f}) "
             f"{pct(ra.parte_precio_min)}-{pct(ra.parte_precio_max)} al precio (centro {pct(ra.parte_precio_central)})")
        if rb is not None:
            s += f"; método B (rejilla P-D, εs {rb.es_central:.2f}) {pct(rb.parte_precio_min)}-{pct(rb.parte_precio_max)}"
        return s
    txt_ayudas = " | ".join(txt_clase(c) for c in (1, 2, 3)) + " | clase 9: No evaluable: sin dato de oferta"
    r_ay = ("Traslado a precios por clase A4 (parte de una ayuda general por unidad que capta el vendedor o arrendador, |εd|/(εs+|εd|); magnitud C4; "
            "cota superior para una ayuda focalizada): " + txt_ayudas)
    sig_ay = "C2 por grupo (P-D v3): el beneficiario paga igual o menos (igual con εs = 0); el no beneficiario paga más. Conjunto del mercado: sin signo estable"

    # Ficha específica por instrumento: (evidencia_lit, efecto, signo, clases) solo donde difiere del grupo v4.
    NE = "No evaluable: "
    esp = {
        "I03": ("Schuetz-Meltzer-Been 2011 (VERIFICADA, Q1); Krimmel-Wang 2026 (VERIFICADA, Q1): existencia acreditada, resultado no leído", NE + "magnitud no extraída de la literatura verificada; sin simulación propia", NE + "signo no extraído", None),
        "I04": ("Ali-Raviola 2025 (NO VERIFICADA, Crossref 429): precios del entorno estables o al alza (resumen secundario, EE. UU.)", NE + "sin literatura verificada con magnitud ni simulación propia", NE + "sin literatura verificada", None),
        "I20": ("Ali-Raviola 2025 (NO VERIFICADA; solo robustez)", NE + "sin literatura verificada con magnitud ni simulación propia", NE + "sin literatura verificada", None),
        "I05": ("Oates-Schwab 1997 (DOI verificado; cuartil no verificado): permisos de construcción +70 % en Pittsburgh, sobre todo comercial (resumen secundario, sin verificar; EE. UU. 1970-1980)", NE + "la magnitud es de un resumen secundario sin verificar y de otro país; solo robustez", NE + "sin signo verificado", None),
        "I26": ("Oates-Schwab 1997 (DOI verificado; cuartil no verificado)", NE + "magnitud de resumen secundario sin verificar (comercial, EE. UU.)", NE + "sin signo verificado", None),
        "N3": ("Oates-Schwab 1997 (DOI verificado; cuartil no verificado)", NE + "magnitud de resumen secundario sin verificar (comercial, EE. UU.)", NE + "sin signo verificado", None),
        "N6": ("Oates-Schwab 1997 (DOI verificado; cuartil no verificado); equivale a I05/I26/N3 en la agrupación v4", NE + "véase I05", NE + "véase I05", None),
        "I12": ("Shahzad et al. 2015 (NO VERIFICADA): -19 % de coste y -34 % de plazo con prefabricación (casos, Nueva Zelanda; asociación sin identificación; solo robustez)", NE + "la magnitud procede de casos sin identificación y de otro país", "asociación: menor coste y plazo (NO VERIFICADA)", None),
        "N5": ("Equivale a I12 (agrupación v4)", NE + "véase I12", NE + "véase I12", None),
        "I13": ("Ball 2011 (VERIFICADA, Q1): descriptivo; retrasos de tramitación mayores que los oficiales, asociados a respuesta lenta de la oferta (Reino Unido); sin identificación", NE + "solo asociación, sin magnitud; sin datos de plazos en España", NE + "sin identificación", None),
        "N1": ("Ball 2011 (VERIFICADA, Q1): solo asociación; Hilber-Vermeulen 2016 (v4, VERIFICADA, magnitud no extraída)", NE + "solo asociación, sin magnitud; sin datos de plazos en España", NE + "sin identificación", None),
        "N2": ("Büchler-Lutz 2024 (VERIFICADA, Q1; DiD escalonado, Zúrich); Greenaway-McGrevy-Phillips 2023 (VERIFICADA, Auckland); Saiz 2010 y Glaeser-Gyourko 2018 (v4, VERIFICADAS)", "Literatura (resumen secundario, otros países): +9 % de viviendas y de superficie residencial a 5-10 años en Zúrich, sin diferencia en alquileres hedónicos; Auckland: construcción al alza, magnitud no extraída. Sin simulación propia ni transferencia a España (C4)", "+ oferta, 0 en alquiler (otro país; no es un signo C2 propio)", None),
        "N4": ("Bono-Trannoy (INSEE; NO VERIFICADA): precio del suelo +8 a +10 % en 2 años tras un incentivo a la oferta de alquiler (Francia, 2004-2010; resumen secundario); LIHTC: Diamond-McQuade 2019 y Eriksen-Rosenthal 2010 (VERIFICADAS, resultado no leído)", "Literatura no verificada: +8 a +10 % en el precio del suelo (riesgo de capitalización en el suelo); solo robustez", "+ precio del suelo (NO VERIFICADA)", None),
        "I02": ("Baum-Snow y Marion 2009 (v4, VERIFICADA, magnitud no extraída); Diamond-McQuade 2019 y Eriksen-Rosenthal 2010 (VERIFICADAS, resultado no leído; LIHTC)", None, None, None),
        "N8": ("Equivale a I02 (agrupación v4)", None, None, None),
        "I14": ("Mora-Sanguinetti 2012 (NO VERIFICADA, Crossref 400): ineficiencia judicial con efecto positivo menor sobre la propiedad frente al alquiler (España, panel provincial)", NE + "magnitud no extraída; fuente no verificada", NE + "fuente no verificada", None),
        "I18": ("Documento de trabajo preliminar, Cataluña 2018 (NO VERIFICADA, sin DOI): sin efecto en oferta ni precio", "Literatura preliminar: efecto 0 en oferta y precio (Cataluña, reforma de 2018; solo robustez)", "0 (preliminar, NO VERIFICADA)", None),
        "I19": ("Phillips-Sullivan 2025 (VERIFICADA, ensayo aleatorio); Stergiopoulos 2019 (VERIFICADA); Evans-Sullivan-Wallskog 2016 (DOI verificado; cuartil no verificado)", NE + "resultados no extraídos; la medida no se orienta al precio ni a la oferta", NE + "resultado no leído", None),
        "I21": ("Estudios de Vancouver y Ontario (NO VERIFICADA, sin DOI): -6 % del precio en barrios con más compradores extranjeros (resumen secundario)", "Literatura no verificada: -6 % del precio en barrios con más compradores extranjeros (Canadá; solo robustez). En España el peso descriptivo es ≈7 % de las compraventas (C4)", "- precio local (NO VERIFICADA)", None),
        "I28": ("Gropp-Scholz-White 1997 (VERIFICADA, Q1): crédito menor con más exención (resumen secundario); discrepan estudios posteriores (no verificados)", NE + "magnitud no extraída; hay discrepancia entre estudios", "crédito menor para el prestatario según un estudio; discrepa la literatura posterior", None),
        "I29": ("Documento de trabajo de AMSE sobre IVA de la vivienda en Francia (NO VERIFICADA): 60 % de traslado (resumen secundario)", "Literatura no verificada: 60 % de la rebaja se traslada al comprador (Francia; solo robustez); el resto se reparte entre promotor y arrendador", "+ para el comprador, parcial (NO VERIFICADA)", None),
        "I11": ("sin evidencia hallada en la búsqueda registrada (docs/v5/literatura_instrumentos.md)", NE + "sin literatura hallada ni simulación propia", NE + "sin literatura hallada", None),
        "I15": ("sin evidencia hallada en la búsqueda registrada", NE + "sin literatura hallada ni simulación propia", NE + "sin literatura hallada", None),
        "I24": ("sin evidencia hallada en la búsqueda registrada", NE + "sin literatura hallada ni simulación propia", NE + "sin literatura hallada", None),
        "I22": ("no buscada por separado (sin consulta específica por presupuesto)", NE + "sin búsqueda ni simulación propia", NE + "sin búsqueda", None),
        "I25": ("no buscada por separado (sin consulta específica por presupuesto)", NE + "sin búsqueda ni simulación propia", NE + "sin búsqueda", None),
    }
    ids = [f"I{i:02d}" for i in range(1, 30) if i not in (17, 23)] + [f"N{i}" for i in range(1, 10)]
    clase_txt = {
        "oferta": "1 (oferta responde) y 2 (si la restricción es de suelo o edificabilidad); en 3 solo con financiación pública (inferencia de mecanismo, C4)",
        "rigida": "efecto de signo no estable; la literatura sugiere más riesgo de capitalización en 2-3 (C4)",
        "publica": "3 y 2 (donde la construcción privada no cubre el coste; inferencia de mecanismo, C4), en 1 con riesgo de desplazar la construcción privada",
        "ayudas": "mayor eficacia en 1 (oferta más elástica); menor en 2 y 3 (ver traslado por clase)",
        "vacias": "1 y 2 (provincias con presión; solo el 27-40 % de las vacías está donde hay presión, C4)",
        "sin": "No evaluable: sin evaluación por clase",
    }
    clase_de = {"I02": "publica", "N8": "publica", "I03": "oferta", "I04": "publica", "I20": "publica", "N4": "publica", "N1": "oferta", "I13": "oferta", "N2": "oferta",
                "I12": "publica", "N5": "publica", "I29": "publica", "I05": "oferta", "N6": "oferta", "I26": "oferta", "N3": "oferta", "I10": "vacias", "I27": "vacias", "N7": "vacias",
                "I01": "rigida", "I06": "ayudas", "I07": "ayudas", "I08": "ayudas", "I09": "ayudas", "N9": "ayudas"}
    # misma fila base para cada id de agrupación v4
    g = {}
    for k, r in base.items():
        for i in k.split("/"):
            g[i] = r
    rows = []
    for i in ids:
        r = g.get(i)
        nom, mec = t.get(i, (None, None))
        if r is None:
            r = {}
        nom = nom or f"{r.get('instrumento', '')} (agrupación v4 con {ALIAS.get(i, '')})"
        mec = mec or r.get("mecanismo", "")
        e = esp.get(i)
        evid = r.get("evidencia", "")
        efecto = r.get("efecto", NE + "sin simulación propia")
        signo = r.get("signo", NE + "sin simulación")
        if e:
            evid = e[0]
            efecto = e[1] if e[1] else efecto
            signo = e[2] if e[2] else signo
        if i in ("I06", "I07", "I08", "N9"):
            efecto, signo = r_ay, sig_ay
            evid = ("Eriksen-Ross 2015 (VERIFICADA, Q1): sin efecto medio en el alquiler, subidas en unidades cerca del máximo del cheque y en áreas de oferta rígida; "
                    "Hilber-Turner 2014 (VERIFICADA): la deducción hipotecaria eleva la propiedad solo en mercados poco regulados, adverso en restrictivos; "
                    "Saiz 2010 (v4, VERIFICADA); Gibbons-Manning 2006 (VERIFICADA): 60-67 % de incidencia en arrendadores; Carozzi-Hilber-Yu 2024 (VERIFICADA, Q1); "
                    "Best-Kleven 2018, Besley et al. 2014, Collinson-Ganong 2018, Susin 2002, Berger et al. 2020, Gruber et al. 2021 (VERIFICADAS, magnitud no extraída)")
            if i == "I06":
                efecto += ". Los avales relajan la restricción de entrada y no son una ayuda por unidad: la traducción es más incierta (cota superior)"
        if i == "I09":
            efecto = NE + "es una transferencia o aplazamiento de carga a deudores existentes: la rejilla de incidencia de ayudas al acceso no se aplica sin un supuesto adicional"
            signo = NE + "sin simulación; v4 la agrupa con las ayudas por su riesgo de capitalización, no por una estimación propia"
        if i == "I07":
            efecto += "; la deducción por vivienda habitual está suprimida desde 2013 (sin verificar en BOE)"
        if i in ("I17", "I23"):
            continue
        ra = ALIAS.get(i, i)
        if ra in rec.index:
            nf, nc = int(rec.loc[ra, "n_documentos_a_favor"]), int(rec.loc[ra, "n_documentos_en_contra"])
            cota = f"{nf} a favor / {nc} en contra (cota de coincidencias, A5)" + (f"; usa el recuento de {ra}" if ra != i else "")
        else:
            cota = "No evaluable: A5 no codifica este id"
        cd = clase_de.get(i, "sin")
        rows.append(dict(id=i, instrumento=nom, grupo_v4=r.get("id", "—"), mecanismo=mec, evidencia_y_capa=evid, efecto_y_rango=efecto, signo=signo,
                         plazo=r.get("plazo", NE + "sin dato"), coste_fiscal=f"{r.get('coste', 'No evaluable')}; {PRIV}", riesgos=r.get("riesgos", "—"),
                         distribucion=r.get("distribucion", "—"), clase_A4_donde_funciona=clase_txt[cd],
                         documentos_que_lo_proponen_cota_de_coincidencias=cota,
                         capa=("C2 (signo)/C4 (magnitud)" if i in ("I10", "I27", "N7", "I02", "N8", "I06", "I07", "I08", "N9") or r.get("id") == "P1" else "C4"
                               if i != "I01" else "C4 (propio; fuera de C3)")))
    # I16 e I01 conservan su ficha v4; P1 (más construcción) es un instrumento transversal: se añade como fila de referencia
    p1 = base["P1"]
    rows.append(dict(id="P1", instrumento=p1["instrumento"], grupo_v4="P1", mecanismo=p1["mecanismo"], evidencia_y_capa=p1["evidencia"], efecto_y_rango=p1["efecto"],
                     signo=p1["signo"], plazo=p1["plazo"], coste_fiscal=p1["coste"] + "; " + PRIV, riesgos=p1["riesgos"], distribucion=p1["distribucion"],
                     clase_A4_donde_funciona=clase_txt["oferta"], documentos_que_lo_proponen_cota_de_coincidencias="No aplica: resultado de simulación, no instrumento codificado",
                     capa="C2 (signo)/C4 (magnitud)"))
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "matriz_instrumentos.csv", index=False)
    sin_eval = df[df.signo.str.startswith("No evaluable")].id.tolist()
    cols = ["id", "instrumento", "evidencia_y_capa", "efecto_y_rango", "signo", "plazo", "coste_fiscal", "riesgos", "distribucion", "clase_A4_donde_funciona",
            "documentos_que_lo_proponen_cota_de_coincidencias", "capa"]
    md = ("# Matriz completa de instrumentos (D1, v5)\n\nFecha: " + FECHA + ". Rúbrica idéntica para I01-I29 (salvo I17 e I23, sin definición en v4) y N1-N9, más la fila "
          "transversal P1. Se evalúan instrumentos, no actores. «No evaluable: motivo» sustituye a cualquier opinión. Las magnitudes de P-D v3 son C4 y los signos "
          "estables de P-D son C2; las clases territoriales (A4) son C4, así que toda columna de clase es C4 (inferencia de mecanismo, no efecto estimado por clase). "
          "Literatura VERIFICADA = DOI en Crossref y cuartil Scimago; la verificación acredita la existencia, no el resultado, y las magnitudes proceden de resúmenes "
          "secundarios. Sin lenguaje causal por debajo de C3. «Cota de coincidencias» = documentos oficiales de A5 con una medida codificada (cota, no censo).\n\n"
          "## Traslado a precios de las ayudas a la demanda, por clase A4 (C4)\n\n"
          "Parte de una ayuda general por unidad captada por vendedores o arrendadores: |εd|/(εs+|εd|), |εd| en {0,3; 0,6; 1,0; 1,5} (rejilla P-D v3). "
          "Método A: εs = respuesta de oferta provincial de A4 (C4) recortada a ≥ 0, mediana y rango intercuartílico por clase. Método B: la rejilla de oferta de P-D v3 "
          "(0; 0,45; 1,75) asignada a las clases 2, 3 y 1 (supuesto). Si discrepan se dan ambos. Justificación: Eriksen-Ross 2015 (subidas donde la oferta es rígida), "
          "Hilber-Turner 2014 (efecto adverso en mercados restrictivos), Saiz 2010 (elasticidad de oferta limitada por el suelo), Gibbons-Manning 2006 (60-67 % en arrendadores).\n\n"
          "| clase | método | εs (mín-central-máx) | parte al precio mín | centro | máx |\n|---|---|---|---|---|---|\n"
          + "".join(f"| {int(r.clase)} | {r.metodo} | " + (f"{r.es_lo:.2f}-{r.es_central:.2f}-{r.es_hi:.2f} | {pct(r.parte_precio_min)} | {pct(r.parte_precio_central)} | {pct(r.parte_precio_max)} |\n"
                                                      if r.parte_precio_min == r.parte_precio_min else "No evaluable | — | — | — |\n") for r in ic.itertuples())
          + "\n## Matriz\n\n| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
          + "".join("| " + " | ".join(str(r[c]).replace("|", "/") for c in cols) + " |\n" for r in rows))
    (OUT / "matriz_instrumentos.md").write_text(md, encoding="utf-8")

    pa = ic[ic.metodo == "A"].set_index("clase")
    hechos = [dict(id="D1-H01", indicador="Instrumentos evaluados con la rúbrica (I01-I29 sin I17 ni I23, N1-N9)", valor=len(df) - 1, min=None, max=None, unidad="instrumentos",
                   periodo="2026-10", cobertura="matriz D1", fuentes="docs/v4/instrumentos.md; output/v5/A5", capa="C4", fecha_dato=FECHA),
              dict(id="D1-H02", indicador="Instrumentos con 'No evaluable' en el signo", valor=len(sin_eval), min=None, max=None, unidad="instrumentos", periodo="2026-10",
                   cobertura="matriz D1", fuentes="output/v5/D1/matriz_instrumentos.csv", capa="C4", fecha_dato=FECHA)]
    for c in (1, 2, 3):
        x = pa.loc[c]
        hechos.append(dict(id=f"D1-H1{c}", indicador=f"Parte de una ayuda general que se traslada al precio, clase A4 {c} (método A)", valor=round(100 * x.parte_precio_central, 1),
                           min=round(100 * x.parte_precio_min, 1), max=round(100 * x.parte_precio_max, 1), unidad="%", periodo="rejilla εd 0,3-1,5",
                           cobertura=f"{n_clase.get(c, 0)} provincias de clase {c}", fuentes="output/v5/A4; output/v3/PD; literatura verificada", capa="C4", fecha_dato=FECHA))
    (OUT / "hechos.json").write_text(json.dumps(hechos, ensure_ascii=False, indent=1))

    inc1, inc2, inc3 = (f"{pct(pa.loc[c].parte_precio_min)}-{pct(pa.loc[c].parte_precio_max)}" for c in (1, 2, 3))
    fichas = [dict(id="D1-V1", tema="Ayudas a la demanda", enunciado="Las ayudas a los jóvenes para comprar o alquilar abaratan su acceso a la vivienda.", capa="C2",
                   magnitud=(f"Signo por grupo (C2, estable en la rejilla de P-D): el beneficiario paga igual o menos; el no beneficiario paga más. Traslado a precios de una ayuda general por unidad "
                             f"(C4, método A): clase 1 {inc1}; clase 2 {inc2}; clase 3 {inc3}; clase 9 No evaluable. Con el método B: clase 1 {pct(f(1, 'B').parte_precio_min)}-{pct(f(1, 'B').parte_precio_max)}, "
                             f"clase 2 {pct(f(2, 'B').parte_precio_min)}-{pct(f(2, 'B').parte_precio_max)}, clase 3 {pct(f(3, 'B').parte_precio_min)}-{pct(f(3, 'B').parte_precio_max)}."),
                   intervalo=f"clase 1: {inc1}; clase 2: {inc2}; clase 3: {inc3} al precio (C4)", cota="C2 de signo por grupo; magnitud y clase C4",
                   literatura="Eriksen-Ross 2015 (VERIFICADA, Q1); Hilber-Turner 2014 (VERIFICADA); Gibbons-Manning 2006 (VERIFICADA, cuartil no verificado); Carozzi-Hilber-Yu 2024 (VERIFICADA, Q1).",
                   veredicto="PARCIALMENTE",
                   regla=("Regla común con M5-V1: signo estable (C2) para el grupo al que se refiere la afirmación, PARCIALMENTE acotado a ese grupo. Por clase, cuanto más rígida la oferta (clase 2), "
                          "mayor es la parte que se traslada al precio y menor la ventaja neta del beneficiario; en la clase 1 la parte es menor, pero no nula. La capa C2 es solo del signo por grupo; "
                          "la magnitud del traslado y su desglose por clase son C4 (las clases de A4 son C4) y no se promueven."),
                   limites="Sin evaluación verificada de los avales ICO ni de las ayudas españolas; la respuesta de oferta de A4 es C4; una ayuda focalizada tiene una cota superior de traslado.",
                   evidencia=["output/v5/D1/incidencia_ayudas_por_clase.csv", "output/v5/D1/matriz_instrumentos.csv"])]
    (OUT / "fichas_verificador.json").write_text(json.dumps(fichas, ensure_ascii=False, indent=1))
    res = {"rama": "D1", "pregunta": "¿Qué evidencia hay por instrumento, con la misma rúbrica, y cuánto de las ayudas se traslada al precio por clase territorial?",
           "capa": "C4 (signos estables de P-D: C2; clases A4: C4)", "datos": ["output/v4/M5", "output/v3/PD", "output/v5/A4", "output/v5/A5", "output/v5/D1/literatura_instrumentos.csv"],
           "N": {"instrumentos": len(df) - 1, "provincias": int(len(a))}, "metodo": "rúbrica idéntica; incidencia |εd|/(εs+|εd|) con εs por clase (A: respuesta de oferta A4; B: rejilla P-D)",
           "estimacion": {"traslado_precio_clase_A_min_central_max": {int(c): [float(pa.loc[c].parte_precio_min), float(pa.loc[c].parte_precio_central), float(pa.loc[c].parte_precio_max)] for c in (1, 2, 3)},
                          "sin_signo_evaluable": sin_eval},
           "ic95": None, "p_ajustado": None, "nivel_evidencia": "EXPLORATORIO (C4); signos P-D en C2", "diagnosticos": {"metodos_discrepan": "A y B se reportan ambos"},
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
           "notas": "Sin especificaciones econométricas nuevas (determinista; registro.csv vacío por diseño). I17 e I23 sin definición en v4."}
    (OUT / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    pd.DataFrame(columns=["especificacion", "n", "estimacion", "p", "p_ajustado_holm"]).to_csv(OUT / "registro.csv", index=False)
    return res


if __name__ == "__main__":
    print(json.dumps(main()["estimacion"], ensure_ascii=False)[:600])
