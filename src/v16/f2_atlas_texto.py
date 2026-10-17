"""V16-F2.3 · Atlas: índice atlas.md, hechos.json (V16-ATL-*) y resultado.json. Solo descriptivo (C4)."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

import f2_atlas_datos as D

ORDEN = ["nacional", "ccaa", "provincia", "partido_judicial", "municipio", "distrito", "seccion"]
CLAVE = [  # (id, indicador, nivel, descripción)
    ("RENTA-HOGAR", "renta_media_hogar", "municipio", "Renta neta media del hogar (ADRH)"),
    ("RENTA-UC-SECCION", "renta_mediana_uc", "seccion", "Renta mediana por unidad de consumo (ADRH), entre secciones"),
    ("ALQUILER-M2", "alquiler_m2_mediana", "municipio", "Alquiler mediano €/m² y mes (SERPAVI)"),
    ("ESFUERZO", "esfuerzo_alquiler_renta_hogar", "municipio", "Ratio alquiler anual de 80 m² / renta neta media del hogar"),
    ("ESFUERZO-SECCION", "esfuerzo_alquiler_renta_hogar", "seccion", "Ratio alquiler anual de 80 m² / renta neta media del hogar, entre secciones"),
    ("VT-PCT", "viviendas_turisticas_pct_ine", "municipio", "Viviendas turísticas, % de las viviendas (INE VTE)"),
    ("VACIAS", "viviendas_vacias_pct", "municipio", "Viviendas vacías por consumo eléctrico, % (Censo 2021)"),
    ("NO-PRINCIPALES", "viviendas_no_principales_pct", "municipio", "Viviendas no principales, % (Censo 2021)"),
    ("EXTRANJERA", "poblacion_extranjera_pct", "municipio", "Población de nacionalidad extranjera, % (censo anual)"),
    ("PRECIO-PROV", "valor_tasado_m2", "provincia", "Valor tasado €/m², entre provincias"),
    ("LANZ-PJ", "lanzamientos_total_por_10000_viviendas_acum_2013_2024", "partido_judicial",
     "Lanzamientos por 10.000 viviendas, suma 2013-2024, entre partidos judiciales"),
    ("ECV40-CCAA", "ecv_sobreesfuerzo_40_ccaa", "ccaa", "Sobreesfuerzo del 40 % (ECV), entre CCAA"),
]


def _ultimo(a: pd.DataFrame, ind: str, nivel: str) -> tuple[pd.DataFrame, str]:
    s = a[(a.indicador == ind) & (a.nivel == nivel) & ~a.suprimida & a.valor.notna()]
    if s.empty:
        return s, ""
    per = sorted(s.periodo.unique())[-1]
    return s[s.periodo == per], per


def _posibles() -> dict[str, int]:
    t = pd.read_parquet(D.RAIZ / "data" / "base" / "territorios.parquet", columns=["territorio_codigo", "nivel"])
    return t.groupby("nivel").size().to_dict()


def _selladas() -> dict[str, tuple[int, int]]:
    """(unidades selladas, universo) por nivel, solo recuentos."""
    t = pd.read_parquet(D.RAIZ / "data" / "base" / "territorios.parquet", columns=["territorio_codigo", "nivel"])
    res = {}
    for nivel in ("provincia", "municipio", "distrito", "seccion"):
        c = t[t.nivel == nivel].territorio_codigo
        res[nivel] = (int(D.es_sellada(c, nivel).sum()), int(len(c)))
    pm = pd.read_parquet(D.P16 / "tension_social_partidos_municipios_terceros.parquet", columns=["territorio_codigo", "estado"])
    pj = pm[pm.estado == "partido_con_serie_cgpj"].territorio_codigo.drop_duplicates()
    res["partido_judicial"] = (int(D.es_sellada(pj, "partido_judicial").sum()), int(len(pj)))
    return res


def cifras(a: pd.DataFrame) -> list[dict]:
    h = []
    for id_, ind, nivel, desc in CLAVE:
        s, per = _ultimo(a, ind, nivel)
        if s.empty:
            continue
        v = s.valor.astype(float)
        p10, p90 = np.percentile(v, 10), np.percentile(v, 90)
        tot = int(((a.indicador == ind) & (a.nivel == nivel) & (a.periodo == per)).sum())
        h.append({"id": f"V16-ATL-DISP-{id_}", "indicador": f"Cociente P90/P10 de «{desc}» entre {nivel.replace('_', ' ')}s no sellados",
                  "valor": round(float(p90 / p10), 3) if p10 > 0 else None, "min": round(float(v.min()), 3), "max": round(float(v.max()), 3),
                  "unidad": "cociente P90/P10 (min y max en la unidad del indicador: " + str(s.unidad.iloc[0]) + ")", "periodo": per,
                  "cobertura": f"{len(v)} unidades con dato de {tot} filas del periodo (el resto, suprimidas)", "fuentes": str(s.fuente.iloc[0]),
                  "capa": "C4", "fecha_dato": per, "ficha": "output/v16/f2_atlas/atlas.md#dispersion"})
    sup = int(a.suprimida.sum())
    h.append({"id": "V16-ATL-COB-FILAS", "indicador": "Filas del atlas (formato largo)", "valor": int(len(a)), "min": None, "max": None,
              "unidad": "filas", "periodo": "varios", "cobertura": f"{a.indicador.nunique()} indicadores, {a.nivel.nunique()} escalas",
              "fuentes": "varias (véase atlas.md)", "capa": "C4", "fecha_dato": D.FECHA, "ficha": "output/v16/f2_atlas/atlas.md#cobertura"})
    h.append({"id": "V16-ATL-COB-SUPRIMIDAS", "indicador": "Porcentaje de filas suprimidas (base < 10 o CV > 30 % o sustituto)",
              "valor": round(100.0 * sup / len(a), 2), "min": None, "max": None, "unidad": "%", "periodo": "varios",
              "cobertura": f"{sup} de {len(a)} filas", "fuentes": "varias", "capa": "C4", "fecha_dato": D.FECHA,
              "ficha": "output/v16/f2_atlas/atlas.md#supresion"})
    for nivel in ("municipio", "seccion"):
        s = a[(a.nivel == nivel) & ~a.suprimida]
        n = s.territorio_codigo.nunique()
        h.append({"id": f"V16-ATL-COB-{nivel.upper()}", "indicador": f"Unidades de escala {nivel} con al menos un indicador publicado",
                  "valor": int(n), "min": None, "max": None, "unidad": "unidades", "periodo": "varios",
                  "cobertura": f"de {_posibles().get(nivel, 0)} del nomenclátor; las selladas V16 no figuran", "fuentes": "varias", "capa": "C4",
                  "fecha_dato": D.FECHA, "ficha": "output/v16/f2_atlas/atlas.md#cobertura"})
    s, per = _ultimo(a, "alquiler_m2_mediana", "municipio")
    if len(s):
        h.append({"id": "V16-ATL-COB-ALQ-MUN", "indicador": "Municipios con alquiler SERPAVI publicable (n >= 10 contratos y CV <= 30 %)",
                  "valor": int(len(s)), "min": None, "max": None, "unidad": "municipios", "periodo": per, "cobertura": "municipios no sellados",
                  "fuentes": "MIVAU SERPAVI", "capa": "C4", "fecha_dato": per, "ficha": "output/v16/f2_atlas/atlas.md#cobertura"})
    s, per = _ultimo(a, "esfuerzo_alquiler_renta_hogar", "seccion")
    if len(s):
        h.append({"id": "V16-ATL-COB-ESF-SECCION", "indicador": "Secciones con la ratio de esfuerzo descriptiva publicable",
                  "valor": int(len(s)), "min": None, "max": None, "unidad": "secciones", "periodo": per, "cobertura": "secciones no selladas",
                  "fuentes": "MIVAU SERPAVI; INE ADRH", "capa": "C4", "fecha_dato": per, "ficha": "output/v16/f2_atlas/atlas.md#esfuerzo"})
    return h[:25]


def _indice(a: pd.DataFrame) -> list[str]:
    filas = ["| indicador | escalas (unidades con valor en el último periodo) | periodos | filas | suprimidas | fuente |", "|---|---|---|---|---|---|"]
    for ind, g in a.groupby("indicador"):
        esc = []
        for nivel in ORDEN:
            gn = g[g.nivel == nivel]
            if gn.empty:
                continue
            ok = gn[~gn.suprimida]
            per = ok.periodo.max() if len(ok) else gn.periodo.max()
            n = ok.territorio_codigo.nunique() if len(str(per)) == 10 else int((ok.periodo == per).sum())  # instantáneas con fecha distinta por unidad
            esc.append(f"{nivel} {n}")
        per = sorted(g.periodo.unique())
        rango = per[0] if len(per) == 1 else f"{per[0]}..{per[-1]}"
        filas.append(f"| {ind} | {'; '.join(esc)} | {rango} | {len(g)} | {int(g.suprimida.sum())} | {g.fuente.iloc[0][:60]} |")
    return filas


def escribir(a: pd.DataFrame, out: Path, smoke: bool) -> list[dict]:
    h = cifras(a)
    (out / "hechos.json").write_text(json.dumps(h, ensure_ascii=False, indent=1), encoding="utf-8")
    sel = _selladas()
    mot = a[a.suprimida].calidad.str.extract(r"(suprimida: [^;]+|valor sustituto[^;]*|renta sustituto[^;]*)")[0].fillna("otro").value_counts()
    L = ["# Atlas multiescala V16 (fase 2.3): capa C4, descriptivo", "",
         f"Generado por `src/v16/f2_atlas.py` (SEED {D.SEED}); no editar a mano. Fecha del dato: cada fila lleva su periodo; construcción {D.FECHA}. "
         "Ninguna frase atribuye causas: son coincidencias territoriales. Amplía el atlas de V10 (`output/v10/atlas_descriptivo.md`: coste por grupo "
         "social, València, Comunitat Valenciana y provincias) con renta ADRH 2015-2023 completa, turismo, parque, lanzamientos e intervenciones, "
         "a todas las escalas disponibles; no repite sus tablas.", "",
         '<a id="cobertura"></a>', "## Cobertura y unidades en blanco por validación sellada", "",
         "Salida: `atlas.parquet` (formato largo: territorio_codigo, nivel, periodo, indicador, valor, ic_inf, ic_sup, calidad, suprimida, fuente; "
         "más unidad, n_base y cv). Escalas: España, CCAA, provincia, partido judicial, municipio, distrito y sección censal. "
         "**Área urbana funcional: sin correspondencia en `data/base/geo` ni en territorios; no se produce** (los mapas usan el municipio y la sección).", "",
         "Las unidades de la muestra sellada (v6, V15 y V16, `holdout.unidad_sellada_v16`) **están en blanco por validación sellada, no por falta de "
         "dato**: no figuran en el fichero ni en los mapas con valor. Las ocho CCAA de la decisión K8 (Aragón, Asturias, Baleares, Canarias, Madrid, "
         "Murcia, Navarra y La Rioja) aparecen solo a escala de CCAA y nación; nunca como provincia ni por debajo. Unidades selladas (recuento): " +
         "; ".join(f"{k} {v[0]} de {v[1]}" for k, v in sel.items()) + ".", "",
         '<a id="supresion"></a>', "## Incertidumbre y supresión", "",
         "- **Supresión**: base < 10 unidades (contratos, anuncios, hogares, viviendas, personas o recuento) o CV > 30 % => valor en blanco y "
         "`suprimida = True`; el motivo queda en `calidad`. "
         f"Filas suprimidas: {int(a.suprimida.sum()):,} de {len(a):,}. Motivos: " + "; ".join(f"{k} ({v})" for k, v in mot.items()) + ".",
         "- **Intervalos al 95 %** solo donde hay error de estimación: (i) alquiler SERPAVI municipal y provincial, aproximación normal a la mediana "
         "con SE = 1,2533·(P75−P25)/1,349/√n; (ii) esfuerzo municipal y provincial, que propaga solo el intervalo del alquiler (la renta ADRH es un "
         "registro); (iii) sobreesfuerzo ECV por CCAA, bootstrap de `f2_esfuerzo`. Sección y distrito: sin n ni intervalo por celda; el n de base "
         "se acota con el del municipio (si el municipio tiene n < 10, la celda se suprime).",
         "- **Registros administrativos** (ADRH, padrón, Censo 2021, CGPJ, SERPAVI en niveles finos): sin intervalo, con marca de calidad "
         "(cota inferior/superior por secreto estadístico, estimación experimental INE-VTE, rastreo de plataforma no validado). "
         "Los **valores sustitutos de provincia o comarca del ADRH no se muestran como municipales** (suprimidos, con su marca). "
         "No hay interpolaciones. Inside Airbnb es un rastreo no validado y no exhaustivo: solo descriptivo.", "",
         '<a id="esfuerzo"></a>', "## Construcción de la ratio de esfuerzo",
         "", f"`esfuerzo = 100 · (mediana SERPAVI de €/m² y mes, tipología colectiva) · 12 · {D.SUPERFICIE_M2:.0f} m² / renta neta media del hogar (ADRH)`, "
         "mismo año (2015-2023), por provincia, municipio, distrito y sección. La superficie de 80 m² es un supuesto de vivienda tipo (como en V10), no la "
         "superficie observada. SERPAVI mide el stock de contratos declarados, no los contratos nuevos; la renta es la de todos los hogares de la unidad, "
         "no solo la de los inquilinos. **No es la tasa de sobreesfuerzo de la ECV** (que se muestra aparte por CCAA, `ecv_sobreesfuerzo_30/40_ccaa`, con "
         "otro universo y otra definición) y no debe compararse con ella.", "",
         "## Límites de cobertura",
         "- Valor tasado MIVAU: provincia, CCAA y nación; a escala municipal solo València (el MIVAU publica los municipios con nombre, no con código INE).",
         "- Vacías y esporádicas (Censo 2021, tabla 59531): municipios que el INE publica; en la tabla del Censo el «vacío» por consumo eléctrico y las "
         "no principales son la misma fuente, no dos (C4).",
         "- Viviendas turísticas: INE VTE (agosto de 2020, 2022 y 2024, mayo de 2026) e Inside Airbnb (última instantánea por unidad). Los registros "
         "autonómicos de Madrid, Canarias y Baleares no se usan (K8).",
         "- Lanzamientos: CGPJ. Provincia: suma anual 2013-2025 de trimestres completos (Cádiz incluye Ceuta y Málaga incluye Melilla). Partido judicial: "
         "agregado propio 2013-2024 (suma de 12 años); tasa con las viviendas del Censo 2021 de sus municipios. CCAA: series por TSJ. Solo agregados; "
         "ningún fichero de microdatos del CGPJ sale de este módulo.",
         "- Intervenciones: `output/v16/f1/intervenciones.csv`, vigentes a la fecha del dato; la ausencia de fila no equivale a ausencia de regulación.",
         "- Distrito y sección: todos los años disponibles de cada fuente (ADRH 2015-2023, SERPAVI 2015-2024).", "",
         "## Índice por escala e indicador", ""] + _indice(a) + [
         "", '<a id="dispersion"></a>', "## Dispersión territorial (resumen)", "",
         "| id | magnitud | P90/P10 | mínimo | máximo | periodo |", "|---|---|---|---|---|---|"]
    for c in h:
        if c["id"].startswith("V16-ATL-DISP"):
            L.append(f"| {c['id']} | {c['indicador'].replace('Cociente P90/P10 de ', '')[:95]} | {c['valor']} | {c['min']} | {c['max']} | {c['periodo']} |")
    L += ["", "## Mapas", "",
          "`mapas/<área>_municipio.png` (municipios de la provincia) y `mapas/<área>_seccion.png` (secciones del municipio) para Barcelona, València "
          "y Sevilla (ninguna está sellada a escala de municipio; algunos distritos y secciones sí lo están y salen en gris hachurado). Seis paneles: "
          "renta mediana por unidad de consumo 2023, alquiler €/m² 2024, esfuerzo 2023, viviendas turísticas (INE VTE % por municipio; anuncios de "
          "Inside Airbnb por 100 viviendas por sección), población extranjera (censo anual 2025 por municipio; padrón 2022 por sección) y viviendas "
          "no principales (Censo 2021). Gris claro: sin dato o suprimida; gris hachurado: validación sellada.", "",
          "## Summary (English)", "",
          "Descriptive multiscale atlas (layer C4) of income (ADRH), rents (SERPAVI), appraised prices, rent-to-income ratio, tourist dwellings, foreign "
          "population, housing stock and vacancies, evictions and tenancy-related interventions, with 95 % intervals where there is estimation error "
          "and suppression of cells with fewer than 10 base units or CV above 30 %. Sealed-validation units are blank by design, not for lack of data. "
          "No causal claims."]
    (out / "atlas.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    res = {"rama": "f2_atlas", "pregunta": "¿Cómo se distribuyen territorialmente renta, alquiler, precio, esfuerzo, turismo, población extranjera, "
           "parque, lanzamientos e intervenciones, con qué incertidumbre y dónde no se puede publicar?",
           "capa": "C4", "datos": "INE ADRH, MIVAU SERPAVI y valor tasado, INE VTE, Inside Airbnb, padrón y EMCR, Censo 2021, CGPJ (agregados), ECV (f2_esfuerzo), "
           "intervenciones F1", "N": int(len(a)), "metodo": "Inventario descriptivo en formato largo; IC normal aproximado (alquiler), propagado (esfuerzo) y bootstrap (ECV); "
           "supresión base < 10 o CV > 30 %; exclusión de unidades selladas V16",
           "estimacion": {"filas": int(len(a)), "indicadores": int(a.indicador.nunique()), "suprimidas": int(a.suprimida.sum())},
           "ic95": None, "p_ajustado": None, "nivel_evidencia": "DESCRIPTIVO",
           "diagnosticos": {"unidades_selladas_en_salida": 0, "selladas_por_nivel": {k: v[0] for k, v in sel.items()},
                            "smoke": smoke, "fdr": "no aplica (sin contrastes)", "auf": "sin correspondencia en la base"},
           "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
           "notas": "Capa C4. Sin lenguaje causal. Unidades selladas en blanco por validación sellada (K8). No sustituye a las cifras de cifras_clave."}
    (out / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    return h
