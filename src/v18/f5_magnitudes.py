"""V18 · fase 5 · magnitud preferida por factor (B5; adenda 1.9, que sustituye a «Qué entra» y «Modelo» de la sección 3 del plan).

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. Determinista (SEED 20261010), sin red. Lee solo salidas ya versionadas de
V18 (output/v18/estimacion, output/v18/f1/catalogo.csv); no lee datos de la base ni muestras selladas.

Qué hace
- Una estimación propia por factor, la fijada en la adenda 1.9 (E2-R1 es la única con diseño válido; las demás son NO ESTIMABLE o ASOCIACIÓN:
  no entran). La literatura entra en la unidad del factor, con error típico publicado o reconstruible; el estado de su ficha (VERIFICADA, NO VERIFICADA,
  DISCREPANTE) se toma del catálogo de la fase 1 y se publica por estudio.
- Episodios compartidos (E2: la estimación propia, Jofre-Monseny et al. y Monràs y García-Montalvo, mismo registro y mismo episodio) entran como un
  solo episodio: combinación de mínima varianza con correlación modelada rho = 0,8 (sensibilidad: 0,5 y 1); pesos no negativos.
- Con 3 estudios o más: metaanálisis bayesiano de efectos aleatorios por cuadratura (src/v18/herr18/meta_bayes.py; herramienta con veredicto NO APTO por
  conservadora: los intervalos cubren de más y, con K = 2, el efecto fijo no cubre mu si hay heterogeneidad; se publica con esa advertencia).
  Tres priors de mu: N(0, s^2), N(0, (2s)^2) y N(0, (s/2)^2). Solo se publica magnitud preferida si la decisión coincide en las tres (signo de la
  mediana y si el intervalo de credibilidad al 95 % excluye el cero) y no se da la regla del plan (I^2 > 75 % con intervalo de predicción que cambia de
  signo). Si no, se publica el rango sin magnitud preferida.
- Con menos de 3: media ponderada por la inversa de la varianza (efecto fijo) con IC95, junto a cada estimación.
- Sin error típico en la unidad: no hay metaanálisis; se publica el rango de los estudios (sin intervalo estadístico).
- Unidades no comparables: no se combinan y se dice.

Salidas: output/v18/f5/{magnitudes.csv, magnitudes_estudios.csv, sensibilidad_b5.csv} (las escribe main()); `distribucion(factor)` lo usa f5_contabilidad.py.
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v18"))
from herr18 import meta_bayes as MB  # noqa: E402

ALCANCE_TERRITORIAL = "sin lectura de datos"
SEMILLA = 20261010
OUT = RAIZ / "output" / "v18" / "f5"
EST = RAIZ / "output" / "v18" / "estimacion"
CATALOGO = RAIZ / "output" / "v18" / "f1" / "catalogo.csv"
ROTULO = "análisis V18; capa C4; pre-registro interno plan-replicacion-v18"
RHO = 0.8
RHOS_SENS = (0.5, 1.0)
S_F = {"E1": 0.1, "E2": 0.1, "E3": 3.0, "E4": 1.0, "E5": 2.0, "E6": 0.5, "E7": 10.0, "E8": 5.0, "E9": 5.0}
UNIDAD = {
    "E1": "Δln del alquiler por +1 pp de viviendas turísticas sobre el parque",
    "E2": "ATT en ln de la renta de los contratos regulados",
    "E3": "% de precio por +1 % de población por entrada de inmigrantes",
    "E4": "θ: euros de alquiler por euro de ayuda",
    "E5": "elasticidad precio de la oferta de unidades",
    "E6": "elasticidad del alquiler respecto a la oferta nueva (% por 1 %)",
    "E7": "% del precio por +100 pb del tipo hipotecario, a 8 trimestres",
    "E8": "% de precio por +1 pp del ITP, a 12 meses",
    "E9": "% de precio por +1 pp de cuota de compras de no residentes",
}
# Referencia única de I6 por factor (Anexo B de la adenda): etiqueta, no criterio.
REFERENCIA_I6 = {"E1": ("segu2018", 0.038), "E2": ("jofremonseny2023", -0.045), "E3": ("gonzalez_ortega_2011_chicagofed", 0.959),
                 "E5": ("taltavull_2006_funcas", 0.87), "E6": ("mense_2025_jpemacro", -0.192), "E7": ("sanjuan_2023_bde_be2302art09", -2.0),
                 "E8": ("dolls_etal_2020_vfs", -3.0), "E9": ("sa_2016_lse_cfm2016_39", 2.0)}
# Estimación propia designada (adenda 1.9) y su respaldo; solo E2-R1 tiene diseño válido (I1-I5, I8) y no es NO ESTIMABLE.
PROPIA = {
    "E1": ("E1-A1", "NO ESTIMABLE", "E1-A1 es NO ESTIMABLE por variación (MDE80 0,166 frente al umbral 0,038) y el respaldo E1-R2 también (F efectivo 0,02)"),
    "E2": ("E2-R1", "SUGESTIVO", "diseño válido; clase SUGESTIVO con frase de limitación obligatoria (K9)"),
    "E3": ("E3-R2", "NO ESTIMABLE", "E3-R2 es NO ESTIMABLE por variación (MDE80 2,33 elasticidad) y el respaldo E3-A1 también (MDE80 10,4); E3-R1 (€/m² por punto, NO CONCLUYENTE) está en otra unidad y no se combina"),
    "E4": ("—", "NO ESTIMABLE", "sin datos de beneficiarios ni variación (V18-E4-X1)"),
    "E5": ("E5-R1", "NO ESTIMABLE", "E5-R1 es NO ESTIMABLE (F de la primera etapa 0,03); E5-A1 es ASOCIACIÓN y no entra"),
    "E6": ("E6-R2", "NO ESTIMABLE", "E6-R2 es NO ESTIMABLE por datos (Catastro masivo, tarea del autor); E6-R1 está en otra unidad y no se combina"),
    "E7": ("E7-R1", "NO ESTIMABLE", "E7-R1 es NO ESTIMABLE (primera etapa débil); E7-R2 también; el BVAR E7-R3 es ASOCIACIÓN y no entra"),
    "E8": ("E8-R1", "ASOCIACIÓN", "E8-R1 es ASOCIACIÓN (cambio de signo sin 2012-2013, K7): no entra"),
    "E9": ("E9-R2", "NO ESTIMABLE", "E9-R2 es NO ESTIMABLE por choques efectivos (1/HHI < 10)"),
}


@dataclass
class Estudio:
    factor: str
    clave: str          # nombre de la ficha sin .md
    carpeta: str        # carpeta de docs/v18/bib
    ref: str
    y: float | None
    se: float | None
    pais: str
    espana: bool
    europeo: bool
    unidad_autor: str
    entra: bool
    motivo: str
    se_origen: str = "publicado"
    episodio: str = ""  # estudios del mismo episodio y fuente comparten etiqueta
    nota: str = ""
    propia: bool = False
    en_rango: bool = False   # sin error típico pero en la unidad del factor: entra en el rango
    extra: dict = field(default_factory=dict)


def _lit() -> list[Estudio]:
    E = Estudio
    return [
        # ---------------------------------------------------------------- E1
        E("E1", "segu2018", "turismo", "Segú (2018), Barcelona, 2009-2016", 0.038, 0.012, "España", True, True, "Δln alquiler por punto de densidad de Airbnb", True, "", nota="Bartik con distancia a la playa; 2SLS"),
        E("E1", "garcialopez2020", "turismo", "García-López et al. (2020), Barcelona, 2007-2017", 0.022, 0.011, "España", True, True, "ln por cada 100 anuncios en la BSA (IV, alquileres)", False,
          "unidad no convertible: por 100 anuncios en una BSA; la conversión a pp de viviendas exige las viviendas por BSA, que la ficha no da (plan, sección 3)"),
        E("E1", "chavesfonseca2026", "turismo", "Chaves-Fonseca (2026), Madrid, 2010-2018", 0.020, 0.004, "España", True, True, "ln del precio por 100 anuncios en el barrio", False,
          "unidad no convertible (por 100 anuncios y sobre el precio de compra, no el alquiler)"),
        E("E1", "duso2024", "turismo", "Duso et al. (2024), Berlín, 2014-2019", None, None, "Alemania", False, True, "€/m² por anuncio de alta disponibilidad a 250 m", False,
          "unidad no convertible (€/m² por anuncio a 250 m)"),
        # ---------------------------------------------------------------- E2
        E("E2", "jofremonseny2023", "topes", "Jofre-Monseny et al. (2023), Cataluña, 2020-2022", -0.044, 0.006, "España", True, True, "ln de la renta media, tabla 2", True, "",
          episodio="CAT-2020-22", nota="registro de contratos del Incasòl; 148 municipios"),
        E("E2", "monras2023", "topes", "Monràs y García-Montalvo (2023), Cataluña, 2016-2021", -0.058, 0.014, "España", True, True, "ln del precio del contrato (sin efectos fijos de unidad)", True, "",
          episodio="CAT-2020-22", nota="contratos del Incasòl; con efectos fijos de unidad −0,080"),
        E("E2", "breuille2025", "topes", "Breuille et al. (2025), París y cinco ciudades, 2018-2024", -0.051, 0.007, "Francia", False, True, "ln de la renta por m²", True, ""),
        E("E2", "hahn2021", "topes", "Hahn et al. (2021), Berlín, 2019-2020", -0.113, 0.019, "Alemania", False, True, "ln de la renta anunciada (estrategia A; B: −0,075)", True, "",
          nota="se fija la estrategia A (primera de la ficha) antes de combinar; B en la sensibilidad", extra={"alt": (-0.075, 0.022)}),
        E("E2", "perezgarcia2026", "topes", "Pérez García (2026), zonas tensionadas 2024", -0.0298, 0.0113, "España", True, True, "puntos de crecimiento de la renta", False,
          "otro régimen (zonas tensionadas de 2024) y otra unidad (puntos de crecimiento); sin pretendencias paralelas"),
        E("E2", "abel2024", "topes", "Abel et al. (2024), anuncios de Fotocasa", None, None, "España", True, True, "ln del número de anuncios", False, "otra variable (oferta)"),
        # ---------------------------------------------------------------- E3
        E("E3", "gonzalez_ortega_2009_iza", "inmigracion", "González y Ortega (2009, IZA), 50 provincias, 1998-2008", 3.2, 3.2 * 18.58 / 44.72, "España", True, True,
          "% de precio por 1 % de población (euros/m²: 44,72 con error 18,58)", True, "", se_origen="reconstruido por proporcionalidad con el error de 18,58 €/m² sobre 44,72 €/m²",
          episodio="ES-PROV-1998-2010", nota="las versiones de 2011 (Chicago Fed) y de 2013 (J. Regional Science) son el mismo trabajo: cuentan una vez"),
        E("E3", "gonzalez_ortega_2011_chicagofed", "inmigracion", "González y Ortega (2011, Chicago Fed), provincias, 2001-2010", 0.866, 0.803, "España", True, True,
          "elasticidad respecto a la población en edad de trabajar", False, "versión del mismo trabajo que la de 2009 (mismo episodio y fuente): no cuenta dos veces; entra en la sensibilidad",
          episodio="ES-PROV-1998-2010"),
        E("E3", "sanchis_guarner_2017_lse", "inmigracion", "Sanchis-Guarner (2017), provincias, 2001-2012", 3.046, 1.214, "España", True, True,
          "puntos de crecimiento del precio por punto de tasa de inmigración (semielasticidad ≈ % por 1 %)", True, ""),
        E("E3", "saiz_2007_philly", "inmigracion", "Saiz (2007), áreas metropolitanas de EE. UU., 1983-1998", 1.607, 0.326, "EE. UU.", False, False,
          "Δln precio por 1 % de población en inmigrantes", True, "", nota="validez externa limitada (EE. UU.)"),
        E("E3", "sa_2015_iza", "inmigracion", "Sá (2015), autoridades locales de Inglaterra y Gales, 2004-2010", -1.627, 0.366, "Reino Unido", False, True,
          "% de precio por 1 % de población", True, ""),
        E("E3", "unal_2022_marburg", "inmigracion", "Unal (2022), distritos de Alemania, 2004-2020", 2.689, 0.648, "Alemania", False, True, "% por 1 % de población inicial (pisos)", True, ""),
        E("E3", "accetturo_2012_bdi", "inmigracion", "Accetturo et al. (2012), distritos de 20 ciudades de Italia", 0.160, 0.053, "Italia", False, True, "elasticidad log-log (ciudad)", False,
          "elasticidad log-log respecto a la población extranjera dentro de la ciudad, no a la población total: unidad no convertible"),
        E("E3", "torres_montero_2023_cytet", "inmigracion", "Torres y Montero (2023), 50 provincias, 2001-2019", -0.95, None, "España", True, True, "% de precio por 1 % de población (texto)", False,
          "sin error típico en la ficha"),
        # ---------------------------------------------------------------- E4
        E("E4", "fack_2005_cepremap", "ayudas", "Fack (2005), Francia, 1984-2002", 0.39, 0.24, "Francia", False, True, "θ (DD con controles; sin controles 0,76 con error 0,26)", True, "",
          nota="se fija la especificación con controles antes de combinar"),
        E("E4", "eerola_etal_2026_jpube", "ayudas", "Eerola et al. (2026), Finlandia, reforma de 2015", 0.036, 0.028, "Finlandia", False, True, "θ", True, "", nota="solo resumen"),
        E("E4", "kangasharju_2008_vatt458", "ayudas", "Kangasharju (2008), Finlandia", 0.57, None, "Finlandia", False, True, "θ (IV)", False, "sin error típico en la ficha"),
        E("E4", "hyslop_rea_2018_motu", "ayudas", "Hyslop y Rea (2018), Nueva Zelanda", 0.36, None, "Nueva Zelanda", False, False, "θ", False, "sin error típico en la ficha"),
        # ---------------------------------------------------------------- E5
        E("E5", "taltavull_2006_funcas", "oferta_suelo", "Taltavull (2006), panel de CCAA, 1990-2004", 0.87, 0.125, "España", True, True, "elasticidad precio de los inicios de obra (error desde t = 6,96)", True, "",
          se_origen="reconstruido desde t = 6,96", nota="identificación débil (MC2E con rezagos)"),
        E("E5", "baum_snow_han_2020_nberconf", "oferta_suelo", "Baum-Snow y Han (2020), tractos de EE. UU., 2000-2010", 0.26, 0.11, "EE. UU.", False, False, "elasticidad precio de la oferta de unidades", True, "",
          nota="validez externa limitada (EE. UU.)"),
        E("E5", "paciorek_2012_feds", "oferta_suelo", "Paciorek (2012), EE. UU.", 0.84, 0.10, "EE. UU.", False, False, "elasticidad de permisos al precio (IV)", True, "", nota="validez externa limitada (EE. UU.)"),
        # ---------------------------------------------------------------- E6
        E("E6", "mense_2025_jpemacro", "obra_nueva", "Mense (2025), 94 regiones de Alemania, 2010-2017", -0.192, 0.065, "Alemania", False, True, "elasticidad del alquiler respecto a la oferta nueva", True, ""),
        E("E6", "asquith_mast_reed_2020_philly", "obra_nueva", "Asquith et al. (2020), EE. UU.", -0.062, 0.037, "EE. UU.", False, False, "Δln cerca de un edificio nuevo", False,
          "otra unidad (Δln del alquiler cerca de un edificio, no elasticidad respecto a la oferta): no se combina con Mense (plan, sección 3)"),
        # ---------------------------------------------------------------- E7
        E("E7", "sanjuan_2023_bde_be2302art09", "tipos", "San Juan (2023, Banco de España), BVAR, 2004-2022", -2.0, None, "España", True, True, "% del precio por +100 pb a 8 trimestres", False,
          "intervalos al 68 % solo en un gráfico: sin error típico numérico", nota="solo resumen; BVAR sin identificación externa", en_rango=True),
        E("E7", "bce_eb_2022_6_battistini_gareis_roma", "tipos", "Battistini et al. (2022, BCE), proyecciones locales, área del euro", -5.0, None, "Área del euro", False, True,
          "% del precio por +1 pp del tipo hipotecario a ~2 años", False, "sin error típico (el plan lo deja fuera del metaanálisis y al lado)", en_rango=True),
        # ---------------------------------------------------------------- E8
        E("E8", "dolls_etal_2020_vfs", "fiscalidad", "Dolls et al. (2020), Länder de Alemania, 2005-2018", -3.0, None, "Alemania", False, True, "% de precio por +1 pp del tipo, a 12 meses (publicada −3; WP −3,5)", False,
          "sin error típico recuperado", nota="solo resumen; versión de trabajo −3,5", extra={"alt": (-3.5, None)}, en_rango=True),
        # ---------------------------------------------------------------- E9
        E("E9", "sa_2016_lse_cfm2016_39", "no_residentes", "Sá (2016), Inglaterra y Gales, 1999-2014", 2.0, None, "Reino Unido", False, True, "% de precio por +1 pp de cuota (IV en volumen: 2,0; valor: 1,4; principal 2,1)", False,
          "sin error típico extraído", nota="solo resumen", extra={"alt": (1.4, None), "alt2": (2.1, None)}, en_rango=True),
        E("E9", "alvarez_blanco_garciaposada_2020_bde_be2002art14", "no_residentes", "Álvarez et al. (2020, Banco de España), 50 provincias, 2013T4-2019", 2.55, 2.26, "España", True, True,
          "% de crecimiento acumulado por +1 pp de compras netas sobre el parque", False, "MCO transversal sin instrumento: asociación (el plan no admite asociaciones); se muestra al lado"),
    ]


# ------------------------------------------------------------------------------------------------ catálogo y propia
def estados() -> dict[tuple[str, str], str]:
    c = pd.read_csv(CATALOGO)
    return {(r.factor, str(r.fichero)[:-3]): str(r.estado) for r in c.itertuples()}


def propia_e2() -> Estudio:
    t = pd.read_csv(EST / "e2" / "tabla.csv")
    r = t[t["id"] == "E2-R1"].iloc[0]
    return Estudio("E2", "E2-R1", "", "Estimación propia E2-R1 (Ley 11/2020, Incasòl, 2019T1-2022T1)", float(r["coef"]), float(r["se_cr1"]), "España", True, True,
                   "ATT en ln de la renta de los contratos regulados", True, "", se_origen="error típico CR1 por municipio (el IC95 de Webb es −0,051 a −0,026)",
                   episodio="CAT-2020-22", propia=True, nota="clase SUGESTIVO; 49 municipios regulados y 94 controles")


def frase_limitacion_e2() -> str:
    h = json.loads((EST / "e2" / "hechos.json").read_text(encoding="utf-8"))
    nota = next(x["nota"] for x in h if x["id"] == "V18-E2-R1")
    m = re.search(r"«(Entre 2020T4.*?)»", nota, flags=re.S)
    return m.group(1) if m else ""


# ------------------------------------------------------------------------------------------------ combinación y metaanálisis
def combinar_episodio(y: np.ndarray, se: np.ndarray, rho: float) -> tuple[float, float, np.ndarray]:
    """Combinación de mínima varianza con correlación rho entre todas las estimaciones; pesos no negativos (se descarta iterativamente la de peso negativo).
    Con rho = 1 se queda con la más precisa."""
    n = len(y)
    activo = list(range(n))
    while True:
        s = se[activo]
        S = rho * np.outer(s, s)
        np.fill_diagonal(S, s ** 2)
        if rho >= 0.999999:
            w_a = np.zeros(len(activo))
            w_a[int(np.argmin(s))] = 1.0
        else:
            w_a = np.linalg.solve(S, np.ones(len(activo)))
            w_a = w_a / w_a.sum()
        if (w_a >= -1e-12).all():
            break
        activo.pop(int(np.argmin(w_a)))
    w = np.zeros(n)
    w[activo] = np.maximum(w_a, 0)
    S_full = rho * np.outer(se, se)
    np.fill_diagonal(S_full, se ** 2)
    return float(w @ y), float(np.sqrt(w @ S_full @ w)), w


def efecto_fijo(y: np.ndarray, se: np.ndarray) -> dict:
    w = 1 / se ** 2
    m = float((w * y).sum() / w.sum())
    s = float(1 / np.sqrt(w.sum()))
    q = float((w * (y - m) ** 2).sum())
    k = len(y)
    i2 = max(0.0, (q - (k - 1)) / q) if (k > 1 and q > 0) else float("nan")
    return {"mu": m, "lo": m - 1.959964 * s, "hi": m + 1.959964 * s, "se": s, "Q": q, "I2": i2}


def _posterior_interno(Y, SE, s, mult, tipo):
    tau, dt = MB.rejilla_tau(s)
    w = 1.0 / (SE[:, None] ** 2 + tau[None, :] ** 2)
    S1, Sy, Syy = w.sum(0), (w * Y[:, None]).sum(0), (w * Y[:, None] ** 2).sum(0)
    P = S1 + 1.0 / (mult * s) ** 2
    logL = 0.5 * np.log(w).sum(0) - 0.5 * np.log(P) - 0.5 * (Syy - Sy ** 2 / P)
    logw = logL + np.log(MB.densidad_prior_tau(tau, s, tipo) * dt)
    om = np.exp(logw - logw.max())
    om /= om.sum()
    return tau, om, Sy / P, 1.0 / np.sqrt(P)


def muestras_re(Y, SE, s, mult, tipo, n, rng) -> dict:
    tau, om, m, sd = _posterior_interno(np.asarray(Y, float), np.asarray(SE, float), s, mult, tipo)
    j = rng.choice(len(tau), size=n, p=om)
    mu = rng.normal(m[j], sd[j])
    t = tau[j]
    nuevo = rng.normal(mu, t)
    K = len(Y)
    W = 1 / np.asarray(SE) ** 2
    s2 = (K - 1) * W.sum() / (W.sum() ** 2 - (W ** 2).sum())
    i2 = t ** 2 / (t ** 2 + s2)
    return {"mu": mu, "tau": t, "nuevo": nuevo, "i2": i2}


def meta(Y: np.ndarray, SE: np.ndarray, s: float, n: int = 40000, semilla: int = SEMILLA) -> dict:
    """Metaanálisis bayesiano con las tres priors de mu (principal N(0,s^2)) y semi-Cauchy para tau como sensibilidad."""
    Y, SE = np.asarray(Y, float), np.asarray(SE, float)
    out = {"priors": {}}
    for nombre, mult, tipo in (("s", 1.0, "seminormal"), ("2s", 2.0, "seminormal"), ("s/2", 0.5, "seminormal"), ("s_semicauchy", 1.0, "semicauchy")):
        p = MB.posterior(Y[None, :], SE[None, :], s=s, mult=mult, tipo_tau=tipo)
        lo, med, hi = float(p["mu_lo"][0]), float(p["mu_med"][0]), float(p["mu_hi"][0])
        out["priors"][nombre] = {"mu_med": med, "mu_lo": lo, "mu_hi": hi, "tau_med": float(p["tau_med"][0]), "tau_lo": float(p["tau_lo"][0]), "tau_hi": float(p["tau_hi"][0]),
                                 "signo": int(np.sign(med)), "excluye0": bool(lo > 0 or hi < 0)}
    rng = np.random.default_rng(semilla)
    m = muestras_re(Y, SE, s, 1.0, "seminormal", n, rng)
    out["pi"] = (float(np.quantile(m["nuevo"], 0.025)), float(np.quantile(m["nuevo"], 0.975)))
    out["i2_med"] = float(np.median(m["i2"]))
    out["i2_ic"] = (float(np.quantile(m["i2"], 0.025)), float(np.quantile(m["i2"], 0.975)))
    dec = {(v["signo"], v["excluye0"]) for k, v in out["priors"].items() if k != "s_semicauchy"}
    out["decision_coincide"] = len(dec) == 1
    p0 = out["priors"]["s"]
    out["pi_cambia_signo"] = out["pi"][0] < 0 < out["pi"][1]
    out["regla_i2"] = bool(out["i2_med"] > 0.75 and out["pi_cambia_signo"])
    out["rango_priors"] = (min(v["mu_lo"] for k, v in out["priors"].items() if k != "s_semicauchy"), max(v["mu_hi"] for k, v in out["priors"].items() if k != "s_semicauchy"))
    out["mu_principal"] = (p0["mu_med"], p0["mu_lo"], p0["mu_hi"])
    return out


# ------------------------------------------------------------------------------------------------ construcción de un factor
def _entradas(factor: str, est: list[Estudio], rho: float, sin_i6: bool, ref: float | None, alt_hahn: bool = False,
              contar_go_2011: bool = False) -> tuple[list[dict], list[str]]:
    """Unidades de análisis (estudios o episodios) que entran en el metaanálisis."""
    notas: list[str] = []
    ent = [e for e in est if e.factor == factor and e.entra and e.y is not None and e.se is not None]
    if factor == "E3" and contar_go_2011:
        ent = [e for e in ent if e.clave != "gonzalez_ortega_2009_iza"] + [e for e in est if e.clave == "gonzalez_ortega_2011_chicagofed"]
    if alt_hahn:
        h = next(e for e in ent if e.clave == "hahn2021")
        y2, s2 = h.extra["alt"]
        ent = [Estudio(**{**h.__dict__, "y": y2, "se": s2}) if e.clave == "hahn2021" else e for e in ent]
    if sin_i6 and ref is not None:
        mant = []
        for e in ent:
            r = e.y / ref if ref else np.nan
            if (r >= 1 / 3) and (r <= 3):
                mant.append(e)
            else:
                notas.append(f"{e.clave} fuera de I6 (razón {r:.2f})")
        ent = mant
    unidades: list[dict] = []
    por_ep: dict[str, list[Estudio]] = {}
    for e in ent:
        if e.episodio:
            por_ep.setdefault(e.episodio, []).append(e)
        else:
            unidades.append({"nombre": e.clave, "y": e.y, "se": e.se, "miembros": [e.clave], "propia": e.propia, "pais": e.pais, "espana": e.espana, "europeo": e.europeo})
    for ep, lst in por_ep.items():
        if len(lst) == 1:
            e = lst[0]
            unidades.append({"nombre": e.clave, "y": e.y, "se": e.se, "miembros": [e.clave], "propia": e.propia, "pais": e.pais, "espana": e.espana, "europeo": e.europeo})
        else:
            y = np.array([e.y for e in lst])
            se = np.array([e.se for e in lst])
            m, s, w = combinar_episodio(y, se, rho)
            unidades.append({"nombre": f"episodio {ep}", "y": m, "se": s, "miembros": [e.clave for e in lst], "propia": any(e.propia for e in lst), "pais": lst[0].pais,
                             "espana": True, "europeo": True, "pesos": {e.clave: round(float(x), 3) for e, x in zip(lst, w)}})
    return unidades, notas


def resolver(factor: str, unidades: list[dict]) -> dict:
    """Aplica la regla del plan: >= 3 unidades, metaanálisis; < 3, efecto fijo; sin unidades con error, rango sin intervalo."""
    s = S_F[factor]
    k = len(unidades)
    if k == 0:
        return {"metodo": "sin estudios con error típico en la unidad", "k": 0}
    y = np.array([u["y"] for u in unidades])
    se = np.array([u["se"] for u in unidades])
    if k >= 3:
        m = meta(y, se, s)
        r = {"metodo": "metaanálisis bayesiano de efectos aleatorios (3 priors)", "k": k, "meta": m, "y": y, "se": se}
        if not m["decision_coincide"]:
            r["estado"] = "rango sin magnitud preferida (la decisión no coincide en las tres priors)"
        elif m["regla_i2"]:
            r["estado"] = "rango sin magnitud preferida (I² > 75 % y el intervalo de predicción cambia de signo)"
        else:
            r["estado"] = "magnitud preferida"
        return r
    f = efecto_fijo(y, se)
    return {"metodo": "media ponderada por la inversa de la varianza (efecto fijo)" if k == 2 else "un solo estudio en la unidad", "k": k, "fijo": f, "y": y, "se": se,
            "estado": "magnitud preferida" if k >= 1 else "sin magnitud"}


def construir(factor: str, est: list[Estudio], rho: float = RHO, sin_i6: bool = False, **kw) -> dict:
    ref = REFERENCIA_I6.get(factor, (None, None))[1]
    unidades, notas = _entradas(factor, est, rho, sin_i6, ref, **kw)
    r = resolver(factor, unidades)
    r["unidades"] = unidades
    r["notas_i6"] = notas
    return r


def rango_estudios(factor: str, est: list[Estudio]) -> tuple[float, float, list[str]]:
    """Rango de los valores centrales de los estudios en la unidad del factor (con o sin error típico), con las variantes declaradas de la misma ficha."""
    vals, nombres = [], []
    for e in est:
        if e.factor != factor or e.y is None or not (e.entra or e.en_rango):
            continue
        vals.append(e.y)
        nombres.append(e.clave)
        for k in ("alt", "alt2"):
            if k in e.extra:
                vals.append(e.extra[k][0])
    return (min(vals), max(vals), nombres) if vals else (float("nan"), float("nan"), [])


# ------------------------------------------------------------------------------------------------ distribución para la contabilidad
def estudios_todos() -> list[Estudio]:
    return _lit() + [propia_e2()]


def distribucion(factor: str, n: int = 10000, semilla: int = SEMILLA) -> dict | None:
    """Extracciones de la magnitud preferida del factor (para la propagación de la contabilidad).
    tipo: 'posterior' (mu del metaanálisis, prior principal), 'fijo' (normal), 'rango' (uniforme entre los estudios, sin magnitud preferida o sin error típico)."""
    est = estudios_todos()
    idx = sorted(S_F).index(factor)
    rng = np.random.default_rng(semilla + 1000 + idx)
    r = construir(factor, est)
    if r["k"] >= 3 and r["estado"] == "magnitud preferida":
        m = muestras_re(r["y"], r["se"], S_F[factor], 1.0, "seminormal", n, rng)
        return {"tipo": "posterior", "x": m["mu"], "centro": float(np.median(m["mu"])), "ref": "metaanálisis bayesiano"}
    if r["k"] in (1, 2):
        f = r["fijo"]
        return {"tipo": "fijo", "x": rng.normal(f["mu"], f["se"], n), "centro": f["mu"], "ref": "estudio único" if r["k"] == 1 else "efecto fijo"}
    lo, hi, nombres = rango_estudios(factor, est)
    if np.isfinite(lo) and hi > lo:
        return {"tipo": "rango", "x": rng.uniform(lo, hi, n), "centro": (lo + hi) / 2, "ref": "rango de los estudios, uniforme (sin intervalo estadístico)", "lo": lo, "hi": hi}
    if np.isfinite(lo):
        return {"tipo": "puntual", "x": np.full(n, lo), "centro": lo, "ref": "valor único sin error", "lo": lo, "hi": hi}
    return None


# ------------------------------------------------------------------------------------------------ salidas
def _fmt(x, d=4):
    return "" if x is None or (isinstance(x, float) and not np.isfinite(x)) else round(float(x), d)


def fila_factor(factor: str, est: list[Estudio], est_fichas: dict) -> tuple[dict, list[dict]]:
    r = construir(factor, est)
    propia_def = PROPIA.get(factor)
    entra_propia = any(u["propia"] for u in r["unidades"])
    origen = "propia + literatura" if entra_propia else "magnitud solo de la literatura"
    if r["k"] == 0:
        origen = "sin magnitud (ni propia ni literatura comparable)"
    clase = propia_def[1] if propia_def else ""
    base = {"factor": factor, "unidad": UNIDAD[factor], "origen": origen, "estimacion_propia": propia_def[0] if propia_def else "", "clase_estimacion_propia": clase if entra_propia else f"no entra ({clase})",
            "motivo_propia": propia_def[2] if propia_def else "", "n_estudios": sum(1 for e in est if e.factor == factor and e.entra and e.y is not None and e.se is not None),
            "n_unidades_meta": r["k"], "metodo": r["metodo"], "s_f": S_F[factor]}
    lim = []
    if r["k"] >= 3:
        m = r["meta"]
        mu, lo, hi = m["mu_principal"]
        base.update({"estado_b5": r["estado"], "magnitud": _fmt(mu) if r["estado"] == "magnitud preferida" else "", "ic_lo": _fmt(lo) if r["estado"] == "magnitud preferida" else "",
                     "ic_hi": _fmt(hi) if r["estado"] == "magnitud preferida" else "", "rango_lo": _fmt(m["rango_priors"][0]), "rango_hi": _fmt(m["rango_priors"][1]),
                     "tau": _fmt(m["priors"]["s"]["tau_med"]), "I2": _fmt(m["i2_med"], 2), "pi_lo": _fmt(m["pi"][0]), "pi_hi": _fmt(m["pi"][1]),
                     "decision_coincide_3_priors": m["decision_coincide"]})
        lim.append("herramienta meta_bayes NO APTO por conservadora (intervalos que cubren de más; el prior s/2 queda corto en calibración)")
    elif r["k"] in (1, 2):
        f = r["fijo"]
        base.update({"estado_b5": "magnitud preferida" if r["k"] == 2 else "magnitud de un solo estudio", "magnitud": _fmt(f["mu"]), "ic_lo": _fmt(f["lo"]), "ic_hi": _fmt(f["hi"]),
                     "I2": _fmt(f["I2"], 2) if r["k"] == 2 else "", "tau": "", "decision_coincide_3_priors": ""})
        if r["k"] == 2:
            lim.append("con K = 2 el efecto fijo no cubre mu si hay heterogeneidad (cobertura 0,50-0,56 en el Monte Carlo)")
        else:
            lim.append("un solo estudio en la unidad: sin heterogeneidad estimable")
    else:
        lo, hi, nombres = rango_estudios(factor, est)
        base.update({"estado_b5": "rango de la literatura, sin error típico (no hay metaanálisis ni intervalo estadístico)" if np.isfinite(lo) else "sin magnitud",
                     "magnitud": "", "ic_lo": "", "ic_hi": "", "rango_lo": _fmt(lo), "rango_hi": _fmt(hi), "tau": "", "I2": "", "decision_coincide_3_priors": ""})
    if entra_propia:
        lim.append("episodio compartido con el original: cuenta una vez (rho = 0,8)")
    base["limitacion"] = "; ".join(lim)
    # sensibilidades
    sens = []
    for nombre, kw in (("rho_0.5", dict(rho=0.5)), ("rho_1", dict(rho=1.0)), ("sin_I6", dict(sin_i6=True))):
        if factor == "E2" or nombre == "sin_I6":
            rr = construir(factor, est, **kw)
            sens.append((nombre, rr))
    if factor == "E2":
        sens.append(("hahn_estrategia_B", construir(factor, est, alt_hahn=True)))
        sens.append(("sin_estimacion_propia", construir(factor, [e for e in est if not e.propia])))
    if factor == "E3":
        sens.append(("version_2011_en_lugar_de_2009", construir(factor, est, contar_go_2011=True)))
        sens.append(("solo_europeos", construir(factor, [e for e in est if (e.europeo or e.factor != "E3")])))
        sens.append(("solo_espana", construir(factor, [e for e in est if (e.espana or e.factor != "E3")])))
    if factor == "E2":
        sens.append(("solo_europeos", construir(factor, [e for e in est if (e.europeo or e.factor != "E2")])))
    filas_s = []
    for nombre, rr in sens:
        d = {"factor": factor, "variante": nombre, "k": rr["k"], "unidades": "; ".join(u["nombre"] for u in rr["unidades"]), "notas": "; ".join(rr.get("notas_i6", []))}
        if rr["k"] >= 3:
            m = rr["meta"]
            d.update({"estado": rr["estado"], "mu": _fmt(m["mu_principal"][0]), "lo": _fmt(m["mu_principal"][1]), "hi": _fmt(m["mu_principal"][2]),
                      "I2": _fmt(m["i2_med"], 2), "decision_coincide": m["decision_coincide"],
                      "mu_semicauchy": _fmt(m["priors"]["s_semicauchy"]["mu_med"])})
        elif rr["k"] in (1, 2):
            f = rr["fijo"]
            d.update({"estado": rr["estado"], "mu": _fmt(f["mu"]), "lo": _fmt(f["lo"]), "hi": _fmt(f["hi"]), "I2": _fmt(f["I2"], 2)})
        else:
            d.update({"estado": "sin estudios"})
        filas_s.append(d)
    base["_sens"] = filas_s
    base["_resultado"] = r
    return base, filas_s


def filas_estudios(est: list[Estudio], est_fichas: dict, base: dict[str, dict]) -> list[dict]:
    filas = []
    for e in est:
        ref_clave, ref_val = REFERENCIA_I6.get(e.factor, (None, None))
        if e.propia:
            estado = "estimación propia V18 (SUGESTIVO)"
        else:
            estado = est_fichas.get((e.carpeta, e.clave), "NO VERIFICADA (sin registro en el catálogo)")
        if e.y is not None and ref_val and ref_val != 0 and e.clave != ref_clave:
            r = e.y / ref_val
            i6 = ("coherente" if 1 / 3 <= r <= 3 else "no coherente") + f" con {ref_clave}, razón {r:.2f}"
        elif e.clave == ref_clave:
            i6 = "referencia de I6"
        else:
            i6 = "no aplicable"
        filas.append({"factor": e.factor, "estudio": e.clave, "referencia": e.ref, "estado_ficha": estado, "valor": _fmt(e.y), "error_tipico": _fmt(e.se),
                      "origen_error": e.se_origen if e.se is not None else "sin error típico", "unidad_del_autor": e.unidad_autor, "pais": e.pais,
                      "entra_en_B5": "sí" if (e.entra and e.y is not None and e.se is not None) else "no", "motivo_si_no_entra": e.motivo if not (e.entra and e.y is not None and e.se is not None) else (e.motivo or ""),
                      "episodio_compartido": e.episodio, "etiqueta_I6": i6, "nota": e.nota})
    return filas


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    est = estudios_todos()
    fichas = estados()
    filas, sens_todas = [], []
    for f in sorted(S_F):
        b, s = fila_factor(f, est, fichas)
        sens_todas += b.pop("_sens")
        b.pop("_resultado")
        filas.append(b)
    pd.DataFrame(filas).to_csv(OUT / "magnitudes.csv", index=False, encoding="utf-8")
    pd.DataFrame(filas_estudios(est, fichas, {})).to_csv(OUT / "magnitudes_estudios.csv", index=False, encoding="utf-8")
    pd.DataFrame(sens_todas).to_csv(OUT / "sensibilidad_b5.csv", index=False, encoding="utf-8")
    print(pd.DataFrame(filas)[["factor", "origen", "n_estudios", "estado_b5", "magnitud", "ic_lo", "ic_hi", "rango_lo", "rango_hi", "I2", "tau"]].to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
