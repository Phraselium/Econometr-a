"""V18 · fase 4 · E4 (ayudas), E10 (grandes tenedores), E11 (viviendas vacías) y E12 (vivienda protegida): comprobación de datos y MDE, y estimación de lo que el plan permite.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18 (docs/v18/plan_replicacion.md 1.4, 1.10-1.12 y adenda 1.1-1.3, 1.5, 1.7, 1.12-1.13, Anexos A y B).
Determinista (SEED = 20261010), sin red. Los datos pasan por src/v18/sellado.filtrar (que llama a holdout.excluir_sellados_v6() y excluye los bloques de V15 y V16).
Nunca data/sealed ni evaluate_*.

- E4 y E11: NO ESTIMABLES (falta el dato imprescindible; se comprueba y se documenta con la tarea del autor que lo resolvería). E4-L1: solo literatura.
- E10-A1 (asociación transversal; tope ASOCIACIÓN, fuera de Holm): MCO con efectos de provincia; error agrupado por provincia con wild bootstrap de Webb (WCR, 9.999), Conley a 10 km y Moran de los residuos.
- E12-A1 y E12-A2 (protegida frente a libre, estilo Chapelle; tope SUGESTIVO): IV con efectos de provincia y de año, F efectivo de Montiel Olea-Pflueger, intervalo de Anderson-Rubin
  por cluster (src/v18/herramientas/iv_debil.py, APTO), WCR de Webb del AR en cero y Driscoll-Kraay (NO APTO con T <= 30: solo etiqueta).
El MDE se calcula y se registra antes de estimar (adenda 1.3): sin mirar el coeficiente de interés (solo variación real del instrumento y σ declarada «ya vista»).

Uso: python3 src/v18/estimacion/e4_e10_e12.py [--rapido] [--salida DIR]
"""
from __future__ import annotations

import argparse
import glob
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import f_conjunto as F  # noqa: E402
import f_datos as D  # noqa: E402
import f_nucleo as N  # noqa: E402

RAIZ = N.RAIZ
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "src"))
from econ_utils import Registry, holm  # noqa: E402
from src.v18.herramientas import iv_debil as IV  # noqa: E402

warnings.filterwarnings("ignore")
SEED = 20261010
ROTULO = F.ROTULO
BASE_OUT = RAIZ / "output" / "v18" / "estimacion"
WEBB = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])
REPS_FULL = {"mde": 2000, "webb": 9999, "moran": 999}
REPS_RAPIDO = {"mde": 200, "webb": 499, "moran": 99}
GRID_REL = np.geomspace(0.002, 8.0, 90)      # rejilla de γ en unidades de ||y_res|| / ||z_res||
CHAPELLE = -1.604          # Chapelle (2015): −1,604 (0,219) viviendas privadas por vivienda social (NO VERIFICADA); Anexo B, δ = 0,80
NOTA_UNIDAD_E12 = "viviendas libres iniciadas por 100 viviendas del parque, por cada 100 viviendas protegidas calificadas por 100 viviendas del parque"


def num(x, d=4):
    return F.num(x, d)


class Modulo:
    """Una carpeta de salida (e4, e10, e11, e12) con su registro, sus filas y sus cifras."""

    def __init__(self, nombre: str, out: Path):
        self.nombre, self.out = nombre, out
        out.mkdir(parents=True, exist_ok=True)
        self.reg = Registry(out / "registro.csv")
        self.filas: list[dict] = []
        self.hechos: list[dict] = []
        self.fuentes: list[str] = []

    def hecho(self, id_, indicador, valor, lo, hi, unidad, periodo, cobertura, clase, nota):
        self.hechos.append({"id": id_, "indicador": indicador, "valor": num(valor), "min": num(lo), "max": num(hi), "unidad": unidad, "periodo": periodo, "cobertura": cobertura,
                            "fuentes": self.fuentes, "capa": "C4", "clasificacion_v18": clase, "nota": f"{nota} [{ROTULO}]"})

    def no_estimable(self, id_: str, desc: str, motivo: str, tarea: str, estado: str = "NO ESTIMABLE", clase: str = "NO ESTIMABLE", comprobacion: dict | None = None):
        self.reg.log(f"{self.nombre.upper()}-prereg", id_, desc, "", "", 0, np.nan, np.nan, np.nan, notas=f"{estado}: {motivo}")
        self.filas.append({"id": id_, "familia": self.nombre.upper(), "estado": estado, "estimable": False, "clasificacion_v18": clase, "motivo": motivo, "tarea_autor": tarea,
                           "comprobacion": json.dumps(comprobacion or {}, ensure_ascii=False)})
        if clase == "NO ESTIMABLE":
            self.hecho(f"V18-{id_}", f"{desc}: no estimable con los datos actuales", None, None, None, "—", "", "nacional", "NO ESTIMABLE", f"{motivo} Lo resolvería: {tarea}")


# ---------------------------------------------------------------------------------------------- utilidades de inferencia
def residuos(M: np.ndarray, W: np.ndarray) -> np.ndarray:
    return M - W @ np.linalg.lstsq(W, M, rcond=None)[0]


def codif(c) -> tuple[np.ndarray, int]:
    u, i = np.unique(np.asarray(c).astype(str), return_inverse=True)
    return i, len(u)


def wcr_forma_reducida(y: np.ndarray, z: np.ndarray, W: np.ndarray, cl: np.ndarray, G: int, B: int, rng: np.random.Generator, lote: int = 2000) -> dict:
    """WCR de Webb de H0: π = 0 en y = π z + W γ + ε (forma reducida: es el contraste de Anderson-Rubin en β = 0, y con z = x el MCO). t con CR1 por cluster; p simétrico."""
    Wi = np.linalg.pinv(W.T @ W)
    yr, zr = residuos(y, W), residuos(z, W)
    zz = float(zr @ zr)
    pi = float(zr @ yr / zz)
    e = yr - pi * zr
    sc = np.bincount(cl, weights=zr * e, minlength=G)
    se = float(np.sqrt(G / (G - 1) * (sc ** 2).sum()) / zz)
    t0 = pi / se
    Cg = np.zeros((len(y), G))
    Cg[np.arange(len(y)), cl] = 1.0
    cuenta, hechas = 0, 0
    while hechas < B:
        b = min(lote, B - hechas)
        w = WEBB[rng.integers(0, 6, size=(b, G))]
        ys = w[:, cl] * yr[None, :]
        ys = ys - (ys @ W) @ Wi @ W.T
        ps = ys @ zr / zz
        es = ys - ps[:, None] * zr[None, :]
        s2 = (es * zr[None, :]) @ Cg
        ses = np.sqrt(G / (G - 1) * (s2 ** 2).sum(1)) / zz
        cuenta += int(np.sum(np.abs(ps / ses) >= abs(t0) - 1e-12))
        hechas += b
    return {"pi": pi, "se_cr1": se, "t": t0, "p_webb": cuenta / B, "B": B}


def mde_forma_reducida(zr: np.ndarray, yr: np.ndarray, cl: np.ndarray, G: int, R: int, seed: int = SEED) -> dict:
    """MDE al 80 % (t de Student cluster, 5 % bilateral) de la pendiente de forma reducida γ de y sobre z (ya residualizadas): el ruido es y_res con signos de Rademacher por cluster
    (conserva la estructura intra-cluster y la heterocedasticidad; σ declarada «ya vista»); la variación de z es la real. Devuelve el MDE de γ y su potencia en la rejilla."""
    rng = np.random.default_rng(seed)
    S = rng.choice([-1.0, 1.0], size=(R, G))
    Q = np.bincount(cl, weights=zr * zr, minlength=G)
    Bg = np.bincount(cl, weights=zr * yr, minlength=G)                    # Σ_g z u
    crit = stats.t.ppf(0.975, G - 1)
    escala = float(np.sqrt(yr @ yr) / np.sqrt(zr @ zr))
    GRID = GRID_REL * escala
    pot = []
    for g_ in GRID:
        # y* = γ z + s_g y_res  ->  Σ_g z y* = γ Q_g + s_g B_g ;  residuo e_g = Σ_g z (y* - π z) con π = Σ S_g / Σ Q_g
        Sg = g_ * Q[None, :] + S * Bg[None, :]
        pi = Sg.sum(1) / Q.sum()
        sc = Sg - pi[:, None] * Q[None, :]
        se = np.sqrt(G / (G - 1) * (sc ** 2).sum(1)) / Q.sum()
        pot.append(float(np.mean(np.abs(pi / se) > crit)))
    pot = np.array(pot)
    k = np.where(pot >= 0.8)[0]
    if len(k) == 0:
        return {"mde_gamma": float("inf"), "potencia_max_en_rejilla": float(pot[-1]), "R": R, "G": G}
    j = k[0]
    mde = float(GRID[j]) if j == 0 else float(np.interp(0.8, pot[j - 1:j + 1], GRID[j - 1:j + 1]))
    return {"mde_gamma": mde, "R": R, "G": G, "seed": seed, "escala_rejilla": escala}


def moran(e: np.ndarray, coords: np.ndarray, k: int, perms: int, seed: int = SEED) -> dict:
    """I de Moran de los residuos con los k vecinos más próximos (pesos estandarizados por fila); p por permutación."""
    from scipy.spatial import cKDTree
    n = len(e)
    d, ix = cKDTree(coords).query(coords, k=k + 1)
    ix = ix[:, 1:]
    z = e - e.mean()
    den = float(z @ z)
    I = float((z * z[ix].mean(1)).sum() / den)
    rng = np.random.default_rng(seed)
    mayor = 0
    for _ in range(perms):
        zp = rng.permutation(z)
        mayor += int(abs((zp * zp[ix].mean(1)).sum() / den) >= abs(I))
    return {"I": num(I), "p_permutacion": num((mayor + 1) / (perms + 1)), "k_vecinos": k, "esperado_bajo_nulo": num(-1 / (n - 1))}


# ---------------------------------------------------------------------------------------------- E4
def comprobacion_e4() -> dict:
    ficheros = [f for f in glob.glob(str(RAIZ / "data" / "raw" / "**" / "*"), recursive=True)
                if any(s in Path(f).name.lower() for s in ("bono", "beneficiar", "perceptor", "ayuda_alquiler", "ayudas_alquiler"))]
    i = pd.read_csv(RAIZ / "data" / "raw" / "v16" / "intervenciones" / "intervenciones.csv")
    b = i[i.instrumento == "bono_alquiler_joven"]
    return {"ficheros_con_nombre_de_perceptores_o_bono": [str(Path(f).relative_to(RAIZ)) for f in ficheros],
            "n_filas_bono_alquiler_joven_en_intervenciones": int(len(b)), "ambitos_bono": sorted(b.ambito.unique().tolist()),
            "convocatorias_autonomicas_con_fecha": int((b.ambito != "estatal").sum()),
            "ecv_disponible_q7a": (RAIZ / "data" / "raw" / "v9" / "ine_microdatos" / "ecv").exists() or (RAIZ / "data" / "raw" / "v16" / "renta_parque").exists(),
            "nota": "La ECV no asigna el bono por la edad (Q7a, V16): su estimando es un cambio de generosidad, no la incidencia."}


def modulo_e4(out: Path) -> Modulo:
    m = Modulo("e4", out)
    m.fuentes = ["data/raw/v16/intervenciones/intervenciones.csv (calendario estatal del Bono Alquiler Joven)", "docs/v18/bib/ayudas (fichas)", "output/v17/auditoria/regulacion_ayudas_hechos.json (V17-AUD-RA-AYU-TRASLACION-MEDIANA)"]
    comp = comprobacion_e4()
    tarea = ("tareas_autor.md, punto 3: microdatos de beneficiarios del Bono Alquiler Joven y de las ayudas autonómicas (edad, tramo de renta, municipio, fecha de solicitud y concesión, importe, alquiler declarado), "
             "por el Portal de Transparencia o convenio con anonimización")
    m.no_estimable("E4-X1", "Réplica de Fack, Gibbons-Manning y Grislain-Letrémy con perceptores de ayudas al alquiler",
                   "falta el dato imprescindible: no hay microdatos de perceptores ni convocatorias autonómicas con fecha (solo el calendario estatal del bono). Sin tratamiento medido no hay variación que comprobar por MDE.",
                   tarea, comprobacion=comp)
    m.no_estimable("E4-X2", "Discontinuidad por la edad de 35 años en la ECV", "no se repite: Q7a (V16) ya la estimó (−0,120 en el log del alquiler, con placebos del mismo orden) y su estimando es un cambio de generosidad, no la incidencia",
                   "—", estado="no se estima (Q7a)", clase="no se clasifica", comprobacion=comp)
    m.no_estimable("E4-L1", "Magnitud de incidencia de las ayudas al alquiler: solo literatura, sin estimación propia",
                   "la magnitud preferida saldrá solo de la literatura, rotulada «solo literatura, sin estimación propia»; en la fase 5 se combinará en la unidad de la ficha si es comparable",
                   tarea, estado="solo literatura", clase="no se clasifica", comprobacion=comp)
    # E4-L1 no lleva cifra propia: la mediana de V17 (46 %, 41-65 %) ya es una cifra publicada con su id V17-AUD-RA-AYU-TRASLACION-MEDIANA y no se duplica
    m.hecho("V18-E4-L1", "Incidencia de las ayudas al alquiler en el alquiler: solo literatura, sin estimación propia", None, None, None, "—", "", "nacional", "NO ESTIMABLE",
            "Solo literatura, sin estimación propia de V18; la traslación mediana de los estudios con diseño está en V17-AUD-RA-AYU-TRASLACION-MEDIANA (no se duplica). Fichas: Fack (2005, 2006), Gibbons y Manning (2006), "
            "Grislain-Letrémy y Trevien (2022). Lo resolvería: microdatos de beneficiarios (tareas_autor, punto 3).")
    lit = [{"estudio": "Fack (2005, CEPREMAP)", "diseno": "diferencias y triples diferencias con la extensión de las ayudas de los noventa (Francia)", "resultado": "θ = 0,76 (0,26) y 0,39 (0,24) en doble diferencia; 1,42 (0,63) y 1,02 (0,52) en triple", "unidad": "traslación de la ayuda al alquiler (θ)"},
           {"estudio": "Gibbons y Manning (2006)", "diseno": "recorte del Housing Benefit por fecha de mudanza (Reino Unido)", "resultado": "−10,3 % y −16,2 %; con tendencias por antigüedad −3,5 % y −6,8 %", "unidad": "% del alquiler"},
           {"estudio": "Grislain-Letrémy y Trevien (2022, Banque de France WP 886)", "diseno": "discontinuidad geográfica difusa, 60 aglomeraciones (Francia)", "resultado": "+0,052 (0,019) en el log del alquiler por m² por un diferencial de 15-40 €/mes", "unidad": "log del alquiler"}]
    res = {"rama": "v18/estimacion/e4", "pregunta": "¿Se puede estimar con nuestros datos qué parte de una ayuda a la demanda de alquiler acaba en el alquiler (E4 del plan de replicación V18)?", "capa": "C4",
           "datos": "ninguno suficiente: calendario estatal del Bono Alquiler Joven (data/raw/v16/intervenciones); ECV solo para Q7a (V16)", "N": 0,
           "metodo": "comprobación de datos y MDE (adenda 1.3); sin estimación", "estimacion": None, "ic95": None, "p_ajustado": None, "nivel_evidencia": "EXPLORATORIO",
           "clasificacion_v18": "NO ESTIMABLE", "clasificacion_v18_por_especificacion": {r["id"]: r["clasificacion_v18"] for r in m.filas},
           "diagnosticos": {"comprobacion_de_datos": comp, "literatura_sin_combinar": lit, "mde": "no aplica: no hay variación de tratamiento medida", "tarea_del_autor": tarea},
           "fuera_muestra": None, "notas": [ROTULO, "Sin estimación propia: la magnitud preferida saldrá solo de la literatura, rotulada así (E4-L1).", "Si llegan los microdatos se escribirá una adenda antes de mirarlos (plan 1.4, g)."]}
    informe_simple(m, res, "E4 · Ayudas a la demanda", ["No hay microdatos de perceptores del Bono Alquiler Joven ni de las ayudas autonómicas, ni convocatorias autonómicas con fecha: **NO ESTIMABLE**.",
                   "Q7a (V16) ya estimó la discontinuidad por la edad (−0,120) y no se repite: su estimando es un cambio de generosidad, no la incidencia.", f"Datos comprobados: {json.dumps(comp, ensure_ascii=False)}",
                   f"Tarea del autor que lo resolvería: {tarea}.", "La magnitud preferida saldrá solo de la literatura, rotulada «solo literatura, sin estimación propia» (E4-L1)."], lit)
    return m


# ---------------------------------------------------------------------------------------------- E11
def modulo_e11(out: Path) -> Modulo:
    m = Modulo("e11", out)
    m.fuentes = ["data/raw/v16/intervenciones/intervenciones.csv (instrumento ibi_recargo_vacias)", "data/raw/v3/ine_v3_censo2021_municipio_viviendas.csv (vacías 2021 por consumo eléctrico)",
                 "base:censo2011_viviendas", "docs/v18/bib/vacias/segu2020.md"]
    i = pd.read_csv(RAIZ / "data" / "raw" / "v16" / "intervenciones" / "intervenciones.csv")
    q = i[i.instrumento == "ibi_recargo_vacias"]
    comp = {"filas_ibi_recargo_vacias": int(len(q)), "ambitos": sorted(q.ambito.unique().tolist()), "territorios": sorted(q.territorio.unique().tolist()),
            "municipios_con_fecha_de_adopcion": int((q.ambito == "municipio").sum()),
            "cortes_de_vacancia": {"2011": "Censo 2011 (viviendas vacías por municipio: parcial en la base)", "2021": "Censo 2021 (vacías por consumo eléctrico): método distinto"},
            "impuesto_catalan_sobre_vacias": "calendario y bases no localizados en el repositorio", "serie_anual_de_vacancia": "no disponible"}
    tarea = ("tareas_autor.md, punto 12: ordenanzas fiscales con el año de entrada en vigor del recargo del IBI por municipio (Ley 12/2023) y el calendario del impuesto catalán sobre viviendas vacías (Ley 14/2015); "
             "además, las vacías por municipio en 2011 (INE, abierto) y la estadística experimental del INE de vacías por consumo, si existe en serie anual")
    m.no_estimable("E11-X1", "Diferencias en diferencias del recargo del IBI sobre la vacancia y el alquiler", "falta el tratamiento (ningún municipio con fecha de adopción) y la vacancia solo tiene dos cortes con métodos distintos: una diferencia entre cortes confundiría el método con el efecto",
                   tarea, comprobacion=comp)
    m.no_estimable("E11-X2", "Impuesto catalán sobre viviendas vacías", "calendario y bases no localizados", tarea, comprobacion=comp)
    res = {"rama": "v18/estimacion/e11", "pregunta": "¿Se puede estimar el efecto de los recargos e impuestos sobre viviendas vacías en la vacancia y el alquiler (E11 del plan de replicación V18)?", "capa": "C4",
           "datos": "ninguno suficiente", "N": 0, "metodo": "comprobación de datos y MDE (adenda 1.3); sin estimación", "estimacion": None, "ic95": None, "p_ajustado": None,
           "nivel_evidencia": "EXPLORATORIO", "clasificacion_v18": "NO ESTIMABLE", "clasificacion_v18_por_especificacion": {r["id"]: r["clasificacion_v18"] for r in m.filas},
           "diagnosticos": {"comprobacion_de_datos": comp, "mde": "no aplica: no hay tratamiento con fecha", "tarea_del_autor": tarea}, "fuera_muestra": None,
           "notas": [ROTULO, "V17 ya describe las vacías (censo 2021, consumo eléctrico) sin estimar efectos.", "Si llegan los datos se escribirá una adenda antes de mirarlos (plan 1.11, g)."]}
    informe_simple(m, res, "E11 · Viviendas vacías", ["**NO ESTIMABLE.** Falta el tratamiento: no hay adopción municipal del recargo del IBI con fecha ni el calendario del impuesto catalán; la vacancia solo tiene dos cortes con métodos distintos (2011 y 2021, este por consumo eléctrico).",
                   f"Datos comprobados: {json.dumps(comp, ensure_ascii=False)}", f"Tarea del autor que lo resolvería: {tarea}."], None)
    return m


def informe_simple(m: Modulo, res: dict, titulo: str, lineas: list[str], lit: list[dict] | None) -> None:
    t = pd.DataFrame(m.filas)
    t.to_csv(m.out / "tabla.csv", index=False)
    (m.out / "hechos.json").write_text(json.dumps(m.hechos, ensure_ascii=False, indent=1), encoding="utf-8")
    (m.out / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    L_ = [f"# {titulo}\n\n*{ROTULO}.*\n", "## Lectura\n"] + [f"- {x}" for x in lineas]
    if lit:
        L_.append("\n## Literatura (sin combinar: unidades distintas)\n")
        L_.append(F.md_tabla(pd.DataFrame(lit), ["estudio", "diseno", "resultado", "unidad"]))
    L_.append("\n## Especificaciones\n")
    L_.append(F.md_tabla(t, ["id", "estado", "clasificacion_v18", "motivo"]))
    (m.out / "informe.md").write_text("\n".join(L_), encoding="utf-8")
    m.reg.flush()


# ---------------------------------------------------------------------------------------------- E12
def _protegida_prov() -> pd.DataFrame:
    d = pd.read_csv(D.RAW / "mivau_v2_protegida.csv")
    d = d[(d.tabla_codigo == 31306000) & (((d.nivel == "provincia") & d.serie.str.startswith("prot_definitiva_anual_provincia"))
                                           | ((d.nivel == "ccaa") & (d.territorio == "Cantabria")))].copy()
    d["territorio_codigo"] = d["territorio"].map(D.codigo_provincia)         # Cantabria, uniprovincial, se trata como la provincia 39 (como en F3)
    d = d.dropna(subset=["territorio_codigo"])
    d["periodo"] = d["periodo"].astype(str)
    d["nivel"] = "provincia"
    return D.sellado.filtrar(d[["territorio_codigo", "nivel", "periodo", "valor"]], "territorio_codigo", "provincia", "periodo", "mivau_calificaciones_protegida", "A")


def e12_panel() -> dict:
    """Panel provincial balanceado 2002-2024: libre iniciada / protegida (calificaciones definitivas) por 100 viviendas del parque del año anterior."""
    par = D.parque_provincial().pivot(index="territorio_codigo", columns="periodo", values="valor")
    lib = D.iniciadas_libres_provincial().pivot(index="territorio_codigo", columns="periodo", values="valor")
    pro = _protegida_prov().pivot(index="territorio_codigo", columns="periodo", values="valor")
    anios = [str(a) for a in range(2002, 2025)]
    ok = [p for p in par.index if p in lib.index and p in pro.index
          and par.loc[p, [str(a - 1) for a in range(2002, 2025)]].notna().all() and lib.loc[p, anios].notna().all() and pro.loc[p, anios].notna().all()
          and lib.loc[p, [str(a) for a in range(1991, 1996)]].notna().all() and pro.loc[p, [str(a) for a in range(1991, 1996)]].notna().all() and pd.notna(par.loc[p, "2001"])]
    ok = sorted(ok)
    par, lib, pro = par.loc[ok], lib.loc[ok], pro.loc[ok]
    s95 = pro[[str(a) for a in range(1991, 1996)]].sum(1)
    cuota = s95 / s95.sum()
    L0 = lib[[str(a) for a in range(1991, 1996)]].mean(1) / par["2001"] * 100        # obra libre 1991-1995 por 100 viviendas del parque de 2001 (control de persistencia, AD-E12-A1)
    return {"provincias": ok, "par": par, "lib": lib, "pro": pro, "cuota": cuota, "L0": L0, "anios": anios}


def e12_arrays(P: dict, anios: list[str], excluir: list[str] | None = None, outcome: str = "libre", precio: pd.DataFrame | None = None) -> dict:
    prov = [p for p in P["provincias"] if p not in set(excluir or [])]
    A = [str(a) for a in anios]
    par_prev = np.stack([P["par"].loc[prov, str(int(a) - 1)].to_numpy() for a in A], axis=1)               # (N, T)
    x = np.stack([P["pro"].loc[prov, a].to_numpy() for a in A], axis=1) / par_prev * 100
    if outcome == "libre":
        y = np.stack([P["lib"].loc[prov, a].to_numpy() for a in A], axis=1) / par_prev * 100
    else:
        y = np.stack([precio.loc[prov, a].to_numpy() for a in A], axis=1)
    # el total «nacional sin la propia provincia» se restringe a las provincias no selladas (nunca se leen las selladas)
    nac = np.stack([P["pro"].loc[:, a].to_numpy().sum() - P["pro"].loc[prov, a].to_numpy() for a in A], axis=1)
    cuota = P["cuota"].loc[prov].to_numpy()
    z = cuota[:, None] * nac / par_prev * 100
    L0 = P["L0"].loc[prov].to_numpy()
    return {"prov": prov, "y": y, "x": x, "z": z, "L0": L0, "anios": A}


def e12_efectos(a: dict, con_L0: bool = True) -> np.ndarray:
    n, T = a["y"].shape
    prov = np.kron(np.eye(n), np.ones((T, 1)))
    anio = np.kron(np.ones((n, 1)), np.eye(T)[:, 1:])
    cols = [prov, anio]
    if con_L0:
        cols.append(np.kron(a["L0"][:, None], np.eye(T)[:, 1:]))          # obra libre 1991-1995 × año
    return np.hstack(cols)


def iv_cluster(y: np.ndarray, x: np.ndarray, z: np.ndarray, W: np.ndarray, cl: np.ndarray, G: int) -> dict:
    yr, xr, zr = residuos(y, W), residuos(x, W), residuos(z, W)
    yy, XX, ZZ, cc, G_ = IV.preparar(yr, xr, zr, cl)
    F_ = float(IV.f_efectivo(XX, ZZ, cc, G_)[0])
    b, V = IV.dos_sls(yy, XX, ZZ, cc, G_)
    A, C = IV.sumas_ar(yy, XX, ZZ, cc, G_)
    ic = IV.ar_ic_1(A, C, G_)
    se = float(np.sqrt(V[0, 0]))
    pi = float(zr @ xr / (zr @ zr))
    return {"beta": float(b[0]), "se_cr1": se, "t_ic95": [float(b[0] - stats.t.ppf(0.975, G - 1) * se), float(b[0] + stats.t.ppf(0.975, G - 1) * se)], "F_efectivo": F_, "ar": ic,
            "p_ar0": IV.ar_p(A, C, np.array([0.0]), G_), "pi": pi, "yr": yr, "xr": xr, "zr": zr, "n": len(y)}


def dk_iv(res: dict, n: int, T: int, m: int | None = None) -> dict:
    """Driscoll-Kraay (Bartlett) para el IV simple de un instrumento: la varianza de las sumas transversales de z·e por periodo. NO APTO con T <= 30 (V18 montecarlo/driscoll_kraay)."""
    zr, xr, yr = res["zr"].reshape(n, T), res["xr"].reshape(n, T), res["yr"].reshape(n, T)
    b = res["beta"]
    s = (zr * (yr - b * xr)).sum(0)
    m = m if m is not None else int(np.floor(4 * (T / 100) ** (2 / 9)))
    S = float(s @ s)
    for l in range(1, m + 1):
        S += 2 * (1 - l / (m + 1)) * float(s[l:] @ s[:-l])
    zx = float((zr * xr).sum())
    se = float(np.sqrt(max(S, 0)) / abs(zx))
    return {"se_dk": se, "t": b / se, "p_t": float(2 * stats.t.sf(abs(b / se), T - 1)), "bandwidth": m, "etiqueta": "NO APTO con T <= 30 (V18 montecarlo/driscoll_kraay)"}


def ar_texto(ic) -> str:
    t, lo, hi = ic
    if t == "intervalo":
        return f"[{lo:.2f}; {hi:.2f}]"
    if t == "complemento":
        return f"toda la recta salvo ({lo:.2f}; {hi:.2f}): no acotado"
    return {"recta": "toda la recta (no acotado)", "vacio": "vacío"}.get(t, t)


def spec_e12(m: Modulo, id_: str, estado: str, desc: str, a: dict, con_L0: bool, reps: dict, ref: float | None, repite: str = "no", delta: float | None = None, prereg: bool = True,
             seed_off: int = 0) -> dict:
    n, T = a["y"].shape
    W = e12_efectos(a, con_L0)
    cl = np.repeat(np.arange(n), T)
    y, x, z = a["y"].reshape(-1), a["x"].reshape(-1), a["z"].reshape(-1)
    yr, zr, xr = residuos(y, W), residuos(z, W), residuos(x, W)
    pi = float(zr @ xr / (zr @ zr))
    mde_g = mde_forma_reducida(zr, yr, cl, n, reps["mde"], SEED + seed_off)
    mde_b = mde_g["mde_gamma"] / abs(pi) if np.isfinite(mde_g["mde_gamma"]) and abs(pi) > 1e-12 else float("inf")
    umbral = abs(ref) if ref is not None else None
    estimable = True if umbral is None else bool(mde_b <= umbral)
    if prereg:
        m.reg.log("E12-prereg", id_, f"IV: y = β x + FE provincia + FE año{' + L0×año' if con_L0 else ''}; z = cuota 1991-95 × protegida de las demás provincias; cluster provincia", a["anios"][0], a["anios"][-1], 0, np.nan, np.nan, np.nan,
                  notas=f"{estado}; repite_visto={repite}; MDE(β)={mde_b:.3f} frente a {umbral}; π={pi:.4f}; σ de y tras efectos (ya visto); estimable={estimable}")
    r = iv_cluster(y, x, z, W, cl, n)
    rng = np.random.default_rng(SEED + 17 + seed_off)
    w = wcr_forma_reducida(y, z, W, cl, n, reps["webb"], rng)
    dk = dk_iv(r, n, T)
    m.reg.log("E12", id_, "IV provincial", a["anios"][0], a["anios"][-1], n * T, np.nan, np.nan, np.nan, coef_interes=r["beta"], p_interes=w["p_webb"],
              notas=f"G={n}; F={r['F_efectivo']:.2f}; AR={ar_texto(r['ar'])}; Webb B={w['B']}")
    return {"id": id_, "estado": estado, "desc": desc, "G": n, "T": T, "muestra": f"{a['anios'][0]}-{a['anios'][-1]}", "r": r, "w": w, "dk": dk, "mde": mde_g, "mde_beta": mde_b, "umbral": umbral,
            "estimable": estimable, "ref": ref, "repite": repite, "con_L0": con_L0, "delta": delta, "prov": a["prov"]}


def clase_e12(s: dict, p_holm: float | None, pretend: dict, signos_ok: float | None) -> tuple[str, list[str]]:
    """Reglas de la adenda 1.2 con tope SUGESTIVO (el estimando es la protegida, no la pública; la exclusión del instrumento de tendencia es discutible)."""
    if not s["estimable"]:
        return "NO ESTIMABLE", [f"NO ESTIMABLE por variación: MDE {s['mde_beta']:.2f} > {s['umbral']:.3f}"]
    r = s["r"]
    mot = ["tope SUGESTIVO: la vivienda protegida no es la pública y la exclusión del instrumento de tendencia es discutible (Chapelle, 2015)"]
    ar_ac = r["ar"][0] == "intervalo"
    if r["F_efectivo"] < 5 and not ar_ac:
        return "ASOCIACIÓN", mot + ["F efectivo < 5 con AR no acotado: fallo decisivo (I2)"]
    if r["F_efectivo"] < 10:
        mot.append("F efectivo < 10: tope SUGESTIVO (adenda 1.2)")
    for k, v in pretend.items():
        if v.get("p") is not None and v["p"] < 0.01:
            return "ASOCIACIÓN", mot + [f"{k}: p = {v['p']:.3f} < 0,01: fallo decisivo"]
        if v.get("p") is not None and v["p"] < 0.10:
            mot.append(f"{k}: p = {v['p']:.3f} < 0,10: prueba débil")
    if signos_ok is not None and signos_ok < 0.8:
        mot.append("menos del 80 % de las variantes con el mismo signo (I5)")
    i7 = p_holm is not None and p_holm < 0.05
    if i7:
        return "SUGESTIVO", mot
    return "NO CONCLUYENTE", mot + ["I7 no superado (p Holm >= 0,05) con el diseño válido: NO CONCLUYENTE (sin potencia)"]


def pretendencias_e12(P: dict) -> dict:
    """Pretendencia (adenda E12): el instrumento de 2002-2007 no predice la variación de la obra libre de 1996-2001 (MCO transversal, HC1) y exclusión: la cuota 1991-95 no predice el crecimiento
    del PIB provincial de 1995-2001 (el PIB provincial empieza en 2000: no verificable)."""
    prov = P["provincias"]
    a = e12_arrays(P, [str(x) for x in range(2002, 2008)])
    zbar = a["z"].mean(1)
    par01 = P["par"].loc[prov, "2001"].to_numpy()
    pre = (P["lib"].loc[prov, [str(a_) for a_ in range(1996, 2002)]].mean(1).to_numpy() - P["lib"].loc[prov, [str(a_) for a_ in range(1991, 1996)]].mean(1).to_numpy()) / par01 * 100
    X = np.column_stack([np.ones(len(prov)), zbar])
    b = np.linalg.lstsq(X, pre, rcond=None)[0]
    e = pre - X @ b
    Xi = np.linalg.inv(X.T @ X)
    V = Xi @ (X.T * e ** 2 @ X) @ Xi * len(prov) / (len(prov) - 2)
    t = b[1] / np.sqrt(V[1, 1])
    out = {"pretendencia_instrumento_2002_2007_sobre_variacion_libre_1996_2001": {"coef": num(b[1]), "se_hc1": num(np.sqrt(V[1, 1])), "p": num(float(2 * stats.t.sf(abs(t), len(prov) - 2))), "N": len(prov),
                                                                               "unidad": "variación de la obra libre iniciada 1996-2001 frente a 1991-95 por 100 viviendas del parque de 2001, por unidad del instrumento medio"},
           "exclusion_cuota_sobre_pib_1995_2001": {"p": None, "nota": "NO VERIFICABLE: el PIB provincial (data/raw/ine_v2_cre.csv) empieza en 2000; solo habría el crecimiento 2000-2001. Tope SUGESTIVO (ya es el tope de la especificación)."}}
    return out


def e12_precio(P: dict) -> pd.DataFrame:
    """100 Δ ln del valor tasado provincial anual real (media de años completos; valor tasado provincial desde 2002: primera diferencia en 2003)."""
    v = D.anual_de_t("valor_tasado", "provincia").pivot(index="territorio_codigo", columns="periodo", values="valor")
    d = D.anual_de_t("deflactor", "nacional").set_index("periodo").valor
    real = np.log(v.div(d.reindex(v.columns), axis=1) * 100)
    out = 100 * real.diff(axis=1)
    return out


def modulo_e12(out: Path, reps: dict) -> Modulo:
    m = Modulo("e12", out)
    m.fuentes = ["data/raw/mivau_v2_protegida.csv (calificaciones definitivas anuales de vivienda protegida, tabla 1.6, MIVAU)", "data/raw/mivau_v2_iniciadas_terminadas_prov.csv (viviendas libres iniciadas)",
                 "data/raw/mivau_parque.csv (parque de viviendas)", "base:valor_tasado provincial y base:deflactor (E12-A2)"]
    tarea = ("tareas_autor.md, punto 11: promociones de vivienda pública por municipio y año con número de viviendas, régimen y fechas de inicio y entrega (MIVAU, CASA 47 y empresas públicas autonómicas)")
    comp_x1 = {"promociones_publicas_por_municipio_y_ano": "no hay", "intervenciones_vivienda_publica": "3 filas estatales (anuncios y entrega), sin municipio", "parque_social": "solo agregados nacionales y por CCAA en PDF (data/raw/v17/parque_social)"}
    m.no_estimable("E12-X1", "Promociones públicas por municipio y año: efecto sobre la obra privada y los precios del entorno", "falta el dato imprescindible: no hay promociones públicas por municipio y año", tarea, comprobacion=comp_x1)
    P = e12_panel()
    prov = P["provincias"]
    todos = e12_arrays(P, P["anios"])
    n13 = e12_arrays(P, [str(a) for a in range(2002, 2014)])
    sin_bcn = e12_arrays(P, P["anios"], excluir=["08"])
    # sin atípicos: la provincia de mayor cuota 1991-95 y la de mayor |media de y − mediana| (1 % extremo con N ≈ 38: una unidad)
    atip = [prov[int(np.argmax(todos["z"].mean(1)))], prov[int(np.argmax(np.abs(todos["y"].mean(1) - np.median(todos["y"].mean(1)))))]]
    sin_at = e12_arrays(P, P["anios"], excluir=sorted(set(atip)))
    S: dict[str, dict] = {}
    S["E12-A1"] = spec_e12(m, "E12-A1", "principal", "IV: libre iniciada frente a protegida, con obra libre 1991-1995 × año", todos, True, reps, CHAPELLE, delta=0.80, seed_off=0)
    S["E12-A1-v1"] = spec_e12(m, "E12-A1-v1", "variante", "A1 sin el control de obra libre 1991-1995 × año", todos, False, reps, CHAPELLE, seed_off=1)
    S["E12-A1-v2"] = spec_e12(m, "E12-A1-v2", "variante", "A1 sin Barcelona", sin_bcn, True, reps, CHAPELLE, seed_off=2)
    S["E12-A1-v4"] = spec_e12(m, "E12-A1-v4", "variante", "A1 con la ventana 2002-2013", n13, True, reps, CHAPELLE, seed_off=3)
    S["E12-A1-sin-atipicos"] = spec_e12(m, "E12-A1-sin-atipicos", "diagnóstico", f"A1 sin atípicos ({', '.join(sorted(set(atip)))})", sin_at, True, reps, CHAPELLE, seed_off=4)
    m.no_estimable("E12-A1-v3", "A1 con las viviendas libres terminadas como resultado", "falta la clave de sellado: la serie de viviendas libres terminadas por provincia no figura en sellado_v18.json (solo existe la de iniciadas y la de terminadas totales, que incluye la protegida); "
                   "no se sustituye por otra (adenda 1.8)", "añadir la clave de las libres terminadas (sustituto por la regla f de la adenda 1.4) al manifiesto y regenerarlo con src/v18/f3_sellado.py (orden del orquestador, no del autor)", estado="variante", clase="no se clasifica")
    pre = e12_precio(P)
    anios_p = [str(a) for a in range(2003, 2025)]
    prov_p = [p for p in prov if pre.loc[p, anios_p].notna().all()] if all(p in pre.index for p in prov) else [p for p in prov if p in pre.index and pre.loc[p, anios_p].notna().all()]
    P2 = {**P, "provincias": prov_p}
    ap2 = lambda anios, ex=None: e12_arrays(P2, anios, excluir=ex, outcome="precio", precio=pre)       # noqa: E731
    S["E12-A2"] = spec_e12(m, "E12-A2", "principal", "IV: Δ ln valor tasado real frente a protegida", ap2(anios_p), True, reps, None, seed_off=10)
    S["E12-A2-v1"] = spec_e12(m, "E12-A2-v1", "variante", "A2 sin Barcelona", ap2(anios_p, ["08"]), True, reps, None, seed_off=11)
    S["E12-A2-v2"] = spec_e12(m, "E12-A2-v2", "variante", "A2 con la ventana 2003-2013", ap2([str(a) for a in range(2003, 2014)]), True, reps, None, seed_off=12)
    return m, S, P


def finalizar_e12(m: Modulo, S: dict, P: dict, reps: dict) -> dict:
    pre = pretendencias_e12(P)
    # I5 y BY de las variantes
    s0 = np.sign(S["E12-A1"]["r"]["beta"])
    var_a1 = ["E12-A1-v1", "E12-A1-v2", "E12-A1-v4"]
    signo_a1 = float(np.mean([np.sign(S[k]["r"]["beta"]) == s0 for k in var_a1]))
    diag_sin_at = bool(np.sign(S["E12-A1-sin-atipicos"]["r"]["beta"]) == s0)
    s2 = np.sign(S["E12-A2"]["r"]["beta"])
    signo_a2 = float(np.mean([np.sign(S[k]["r"]["beta"]) == s2 for k in ("E12-A2-v1", "E12-A2-v2")]))
    fam = {k: S[k]["w"]["p_webb"] for k in ("E12-A1", "E12-A2") if S[k]["estimable"] or S[k]["umbral"] is None}
    hp = holm(fam) if fam else {}
    by1 = F.by_adjust([S[k]["w"]["p_webb"] for k in var_a1])
    by2 = F.by_adjust([S[k]["w"]["p_webb"] for k in ("E12-A2-v1", "E12-A2-v2")])
    qby = dict(zip(var_a1, by1))
    qby.update(dict(zip(("E12-A2-v1", "E12-A2-v2"), by2)))
    clases = {}
    for k in ("E12-A1", "E12-A2"):
        s = S[k]
        clases[k], mot = clase_e12(s, hp.get(k), pre if k == "E12-A1" else {"pretendencia": pre["pretendencia_instrumento_2002_2007_sobre_variacion_libre_1996_2001"]}, signo_a1 if k == "E12-A1" else signo_a2)
        s["motivos"] = mot
    for k, s in S.items():
        r, w, dk = s["r"], s["w"], s["dk"]
        es_var = s["estado"] in ("variante", "diagnóstico")
        clase = clases.get(k) if not es_var else (clases["E12-A1"] if k.startswith("E12-A1") else clases["E12-A2"])
        if es_var and s["estado"] == "diagnóstico":
            clase = clases["E12-A1"]
        unidad = ("viviendas libres iniciadas por 100 viviendas del parque, por vivienda protegida calificada (por 100 del parque): viviendas privadas por vivienda protegida"
                  if k.startswith("E12-A1") else "% del valor tasado real (variación anual) por cada 100 viviendas protegidas calificadas por 100 del parque")
        ref = f"I6 (etiqueta, no decide): {'coherente' if S[k]['ref'] and 1 / 3 <= r['beta'] / S[k]['ref'] <= 3 else 'no coherente'} con Chapelle (2015) ({CHAPELLE} (0,219), ficha NO VERIFICADA; estimando distinto: protegida, no pública), razón {r['beta'] / CHAPELLE:.2f}. " \
              if k.startswith("E12-A1") else "Sin referencia en la misma unidad (Anexo B): I6 no aplicable. "
        nota = (f"{s['desc']}. {s['G']} provincias no selladas × {s['T']} años ({s['muestra']}); mide la vivienda PROTEGIDA, no la pública (rótulo). 2SLS {r['beta']:.3f} (error típico agrupado por provincia {r['se_cr1']:.3f}; IC95 t[{s['G'] - 1}] "
                f"[{r['t_ic95'][0]:.2f}; {r['t_ic95'][1]:.2f}]); F efectivo (MOP) {r['F_efectivo']:.2f} (primera etapa π = {r['pi']:.3f}); conjunto AR 95 % por cluster {ar_texto(r['ar'])}; p AR en 0 = {r['p_ar0']:.3f}; "
                f"p del WCR de Webb (B = {w['B']}) del AR en 0 = {w['p_webb']:.3f}; Driscoll-Kraay: error típico {dk['se_dk']:.3f}, p = {dk['p_t']:.3f} ({dk['etiqueta']}). "
                f"MDE(β) {s['mde_beta']:.2f} frente al umbral {s['umbral'] if s['umbral'] is not None else 'sin referencia (δ no definido)'} (σ de y tras efectos, ya vista). {ref}{'; '.join(s.get('motivos', []))} "
                f"Inferencia: AR por cluster APTO (V18 montecarlo/iv_debil); Webb con G = {s['G']} (WCR de panel APTO con 30-39 clusters; V18 montecarlo/webb_twfe). Respuesta relativa entre provincias, sin el componente común (efectos de año).")
        m.hecho(f"V18-{k}", f"Viviendas {'libres iniciadas' if k.startswith('E12-A1') else 'valor tasado'}: respuesta a la vivienda protegida calificada, IV provincial ({k})", r["beta"],
                r["ar"][1] if r["ar"][0] == "intervalo" else None, r["ar"][2] if r["ar"][0] == "intervalo" else None, unidad, s["muestra"], f"{s['G']} provincias", clase, nota)
        m.filas.append({"id": k, "familia": "E12", "estado": s["estado"], "repite_visto": "no", "muestra": s["muestra"], "N": s["G"] * s["T"], "G": s["G"], "beta_2sls": num(r["beta"]), "se_cr1": num(r["se_cr1"]),
                        "ic95_t_lo": num(r["t_ic95"][0]), "ic95_t_hi": num(r["t_ic95"][1]), "F_efectivo": num(r["F_efectivo"]), "ar_tipo": r["ar"][0], "ar_lo": num(r["ar"][1]), "ar_hi": num(r["ar"][2]),
                        "p_ar0": num(r["p_ar0"]), "p_webb": num(w["p_webb"]), "p_holm": num(hp.get(k)), "q_BY_variantes": num(qby.get(k)), "p_dk": num(dk["p_t"]), "mde_beta": num(s["mde_beta"], 3),
                        "umbral_mde": num(s["umbral"]) if s["umbral"] is not None else None, "estimable": s["estimable"], "clasificacion_v18": clase if s["estado"] != "diagnóstico" else "no se clasifica", "nota": nota})
    diag = {"pretendencias_y_exclusion": pre, "I5_signo": {"A1": signo_a1, "A1_sin_atipicos_mismo_signo": diag_sin_at, "A2": signo_a2}, "atipicos_excluidos": S["E12-A1-sin-atipicos"]["desc"],
            "holm": {"m": len(hp), "valores": hp}, "BY_variantes": {k: num(v) for k, v in qby.items()},
            "cd_pesaran_A1": F.cd_pesaran((S["E12-A1"]["r"]["yr"] - S["E12-A1"]["r"]["beta"] * S["E12-A1"]["r"]["xr"]).reshape(S["E12-A1"]["G"], S["E12-A1"]["T"])),
            "mde": {k: {"mde_beta": num(s["mde_beta"], 3), "umbral": s["umbral"], "estimable": s["estimable"], "R": s["mde"]["R"]} for k, s in S.items()},
            "driscoll_kraay": "NO APTO con T <= 30 (V18 montecarlo/driscoll_kraay): solo etiqueta", "instrumento": "cuota de protegida 1991-95 × calificaciones de las demás provincias no selladas; 1/HHI no aplica (un solo choque nacional)"}
    clase_a1 = clases["E12-A1"]
    res = {"rama": "v18/estimacion/e12", "pregunta": "¿Desplaza la vivienda protegida calificada a la obra libre iniciada (y cómo se mueve el valor tasado), en las provincias no selladas 2002-2024? Estilo Chapelle (2015), con vivienda protegida, no pública (E12-A1 y E12-A2)",
           "capa": "C4", "datos": "calificaciones definitivas de vivienda protegida, viviendas libres iniciadas, parque y valor tasado provinciales vía src/v18/sellado.filtrar",
           "N": {k: s["G"] * s["T"] for k, s in S.items()}, "metodo": "IV con efectos de provincia y de año y obra libre 1991-95 × año; F efectivo MOP; AR por cluster; WCR de Webb (9.999); Driscoll-Kraay (etiqueta); MDE por Monte Carlo; Holm sobre {A1, A2}; BY en variantes",
           "estimacion": {k: {"beta": num(s["r"]["beta"]), "ar95": [num(s["r"]["ar"][1]), num(s["r"]["ar"][2])], "ar_tipo": s["r"]["ar"][0], "F": num(s["r"]["F_efectivo"]), "p_webb": num(s["w"]["p_webb"]), "p_holm": num(hp.get(k))} for k, s in S.items()},
           "ic95": {k: [num(s["r"]["t_ic95"][0]), num(s["r"]["t_ic95"][1])] for k, s in S.items()}, "p_ajustado": {"metodo": "Holm sobre las estimables de E12 (p del WCR de Webb del AR en 0); BY en variantes", "m": len(hp), "valores": hp},
           "nivel_evidencia": "EXPLORATORIO", "clasificacion_v18": clase_a1, "clasificacion_v18_por_especificacion": {r["id"]: r["clasificacion_v18"] for r in m.filas}, "diagnosticos": diag, "fuera_muestra": None,
           "notas": [ROTULO, "Clase provisional hasta I8 (réplica ciega, B6). Tope SUGESTIVO.", "fuera_muestra: no aplica (diseño de identificación; la predicción frente a AR(4) y ECM v1 se hace en F1).",
                     "Mide la vivienda protegida (calificaciones definitivas), no la pública: se rotula así en cada cifra.", "Desviaciones y motivos: docs/v18/desviaciones_e4_e7b_e10_e12.md."]}
    return res


# ---------------------------------------------------------------------------------------------- E10
def e10_datos() -> pd.DataFrame:
    cols = ["variable", "nivel", "frecuencia", "periodo", "territorio_codigo", "desagregacion", "valor", "edicion", "metodo_dato", "muestra_sellada_v6"]
    vs = ["serpavi_alquiler_m2_mediana", "v12_titularidad_pct_mas10", "v12_titularidad_pct_pj", "adrh_renta_neta_persona", "pob_censo_anual"]
    h = pd.read_parquet(D.HECHOS, columns=cols, filters=[("variable", "in", vs)])
    f = D.sellado.filtrar
    sp = h[(h.variable == "serpavi_alquiler_m2_mediana") & (h.nivel == "municipio") & (h.desagregacion == "tipologia=VC")]
    sp = f(sp, "territorio_codigo", "municipio", "periodo", "serpavi_alquiler_m2_mediana", "A").pivot(index="territorio_codigo", columns="periodo", values="valor")
    t10 = f(h[(h.variable == "v12_titularidad_pct_mas10") & (h.nivel == "municipio")], "territorio_codigo", "municipio", "periodo", "v12_titularidad_pct_mas10", "A")
    tpj = f(h[(h.variable == "v12_titularidad_pct_pj") & (h.nivel == "municipio")], "territorio_codigo", "municipio", "periodo", "v12_titularidad_pct_pj", "A")
    ad = f(h[(h.variable == "adrh_renta_neta_persona") & (h.nivel == "seccion")], "territorio_codigo", "seccion", "periodo", "adrh_renta_neta_persona", "A")
    ad = ad[ad.periodo == "2023"].assign(mun=lambda d: d.territorio_codigo.str.zfill(10).str[:5]).groupby("mun").valor.mean()
    # población municipal: el total de pob_censo_anual hereda la clave pob_total|municipio|A (regla f: misma magnitud, mismo nivel; pob_total municipal de la base solo trae una unidad)
    pc = h[(h.variable == "pob_censo_anual") & (h.nivel == "municipio") & (h.desagregacion == "nacionalidad=Total")]
    pc = f(pc.assign(variable="pob_total"), "territorio_codigo", "municipio", "periodo", "pob_total", "A")
    pc = pc[pc.periodo == "2024"].set_index("territorio_codigo").valor
    d = pd.DataFrame({"ln_alq_2024": np.log(sp["2024"]), "d_ln_alq": np.log(sp["2024"]) - np.log(sp["2019"]),
                      "pct10": t10[t10.periodo == "2024"].set_index("territorio_codigo").valor, "pctpj": tpj[tpj.periodo == "2024"].set_index("territorio_codigo").valor})
    d["ln_renta"] = np.log(ad.reindex(d.index))
    d["ln_pob"] = np.log(pc.reindex(d.index))
    d["prov"] = d.index.str[:2]
    d = d.dropna(subset=["pct10", "ln_renta", "ln_pob", "prov"])
    import geopandas as gpd
    g = gpd.read_parquet(D.RAIZ / "data" / "base" / "geo" / "municipios.parquet").set_index("cod_municipio")
    c = g.geometry.to_crs(25830).centroid
    d["x_km"] = c.x.reindex(d.index) / 1000
    d["y_km"] = c.y.reindex(d.index) / 1000
    return d.dropna(subset=["x_km", "y_km"])


def conley_fwl(xr: np.ndarray, yr: np.ndarray, coords: np.ndarray, corte: float) -> dict:
    from scipy.spatial import cKDTree
    b = float(xr @ yr / (xr @ xr))
    e = yr - b * xr
    s = xr * e
    tree = cKDTree(coords)
    pares = tree.sparse_distance_matrix(tree, corte, output_type="coo_matrix")
    w = 1.0 - pares.data / corte
    v = float((s[pares.row] * s[pares.col] * w).sum())            # incluye la diagonal (d = 0, peso 1)
    se = float(np.sqrt(max(v, 0)) / (xr @ xr))
    vec = float(np.mean(np.bincount(pares.row, minlength=len(xr)) - 1))
    return {"se_conley": se, "t": b / se if se > 0 else float("nan"), "vecinos_medios_en_el_corte": vec, "var_positiva": v > 0}


def spec_e10(m: Modulo, d: pd.DataFrame, id_: str, estado: str, desc: str, y: str, x: str, ctrl: list[str], reps: dict, seed_off: int = 0, prereg: bool = True) -> dict:
    d = d.dropna(subset=[y, x] + ctrl)
    prov, G = codif(d["prov"])
    n = len(d)
    Wc = np.column_stack([np.ones(n)] + [d[c].to_numpy() for c in ctrl]) if ctrl else np.ones((n, 1))
    Wp = np.eye(G)[prov][:, 1:]
    W = np.column_stack([Wc, Wp])
    yv, xv = d[y].to_numpy(), d[x].to_numpy()
    yr, xr = residuos(yv, W), residuos(xv, W)
    mde_g = mde_forma_reducida(xr, yr, prov, G, reps["mde"], SEED + 100 + seed_off)
    if prereg:
        m.reg.log("E10-prereg", id_, f"MCO: {y} ~ {x} + {'+'.join(ctrl) or '—'} + FE provincia; cluster provincia (Webb), Conley 10 km", "2019", "2024", 0, np.nan, np.nan, np.nan,
                  notas=f"{estado}; sin referencia ni δ (Anexo B): el MDE se publica como diagnóstico, sin umbral; MDE={mde_g['mde_gamma']:.3f}; σ de y tras efectos (ya visto); N={n}; G={G}")
    b = float(xr @ yr / (xr @ xr))
    rng = np.random.default_rng(SEED + 200 + seed_off)
    w = wcr_forma_reducida(yv, xv, W, prov, G, reps["webb"], rng)
    cf = conley_fwl(xr, yr, d[["x_km", "y_km"]].to_numpy(), 10.0)
    e = yr - b * xr
    mor = moran(e, d[["x_km", "y_km"]].to_numpy(), 8, reps["moran"], SEED + 300 + seed_off)
    se = w["se_cr1"]
    lo, hi = b - stats.t.ppf(0.975, G - 1) * se, b + stats.t.ppf(0.975, G - 1) * se
    m.reg.log("E10", id_, f"{y} ~ {x}", "2019", "2024", n, np.nan, np.nan, np.nan, coef_interes=b, p_interes=w["p_webb"], notas=f"G={G}; Webb B={w['B']}; Conley 10 km se={cf['se_conley']:.4f}")
    return {"id": id_, "estado": estado, "desc": desc, "y": y, "x": x, "ctrl": ctrl, "N": n, "G": G, "beta": b, "se_cr1": se, "ic95": [lo, hi], "w": w, "conley": cf, "moran": mor, "mde": mde_g,
            "sd_x": float(np.std(xv)), "provincias": int(G)}


def modulo_e10(out: Path, reps: dict) -> Modulo:
    m = Modulo("e10", out)
    m.fuentes = ["base:serpavi_alquiler_m2_mediana municipal, vivienda colectiva (MIVAU/SERPAVI) 2019 y 2024", "base:v12_titularidad_pct_mas10 y base:v12_titularidad_pct_pj municipales 2024 (Catastro; tramo contado dentro del municipio: cota inferior)",
                 "base:adrh_renta_neta_persona por sección 2023 (promedio municipal)", "base:pob_censo_anual municipal 2024 (total)", "data/base/geo/municipios.parquet (centroides)", "output/v17/auditoria/oferta_titularidad_hechos.json (V17-AUD-OT-CAT-GT-PARQUE-2026)"]
    tarea = ("tareas_autor.md, puntos 9, 10, 7 y 6: serie homogénea de titularidad por tramo 2012-2026 (Catastro, transparencia), Panel de Hogares AEAT-IEF, compras de personas jurídicas por provincia (Notariado) y EFF; "
             "con ellas, un diseño escalonado de entrada de grandes tenedores por zona frente a la renta de contratos")
    m.no_estimable("E10-X1", "Réplica de McCarthy (Irlanda) con entrada de grandes tenedores por zona y año", "falta la variación temporal: la titularidad por tramo solo tiene tres cortes (2024-2026) y la serie 2012-2023 tiene otra definición; SERPAVI termina en 2024", tarea,
                   comprobacion={"cortes_de_titularidad_por_tramo": ["2024", "2025", "2026"], "serie_2012_2023": "otra definición (data/raw/v11/catastro_titularidad)", "alquiler": "SERPAVI hasta 2024"})
    d = e10_datos()
    ctr = ["ln_renta", "ln_pob"]
    dn = d.dropna(subset=["ln_alq_2024"])
    dd = d.dropna(subset=["d_ln_alq"])
    S: dict[str, dict] = {}
    S["E10-A1"] = spec_e10(m, dn, "E10-A1", "principal", "ln SERPAVI 2024 frente al % de viviendas de titulares con más de 10 inmuebles (2024), efectos de provincia, renta ADRH 2023 y población 2024", "ln_alq_2024", "pct10", ctr, reps, 0)
    S["E10-A1-d"] = spec_e10(m, dd, "E10-A1-d", "principal", "Δ ln SERPAVI 2019-2024 frente al % de titulares con más de 10 inmuebles (2024), mismos controles", "d_ln_alq", "pct10", ctr, reps, 1)
    for suf, base in (("", dn), ("-d", dd)):
        yv = "ln_alq_2024" if suf == "" else "d_ln_alq"
        k = f"E10-A1{suf}"
        S[k + "-v1"] = spec_e10(m, base, k + "-v1", "variante", f"{k} con el % de personas jurídicas", yv, "pctpj", ctr, reps, 10 + len(S))
        S[k + "-v2"] = spec_e10(m, base[base.index != "08019"], k + "-v2", "variante", f"{k} sin Barcelona (municipio 08019)", yv, "pct10", ctr, reps, 10 + len(S))
        S[k + "-v3"] = spec_e10(m, base, k + "-v3", "variante", f"{k} sin controles", yv, "pct10", [], reps, 10 + len(S))
        gran = base[base.ln_pob >= np.log(10000)]
        S[k + "-v4"] = spec_e10(m, gran, k + "-v4", "variante", f"{k} con municipios de más de 10.000 habitantes", yv, "pct10", ctr, reps, 10 + len(S))
        fuga = D.sellado.municipios_con_distritos_sellados()
        S[k + "-vF"] = spec_e10(m, base[~base.index.isin(fuga)], k + "-vF", "holgura", f"{k} sin los municipios con distritos sellados (fuga declarada, adenda 1.5; holgura nº 1)", yv, "pct10", ctr, reps, 10 + len(S))
    return m, S, d


def finalizar_e10(m: Modulo, S: dict, d: pd.DataFrame) -> dict:
    ps = {k: s["w"]["p_webb"] for k, s in S.items()}
    bh = {}
    for suf in ("", "-d"):
        ks = [f"E10-A1{suf}"] + [f"E10-A1{suf}-v{i}" for i in (1, 2, 3, 4)]
        q = F.by_adjust([ps[k] for k in ks])
        bh.update(dict(zip(ks, q)))
    ref_titulares = "V17: titulares de más de 10 viviendas con el 4,2 % del parque (Catastro 2026; V17-AUD-OT-CAT-GT-PARQUE-2026) y entre el 2 y el 12 % del alquiler habitual con supuestos; no se duplica"
    for k, s in S.items():
        unidad = "% de variación del alquiler por m² (log × 100) por punto porcentual de viviendas de grandes tenedores en el municipio" if k.startswith("E10-A1") else ""
        y_txt = "ln del alquiler por m² (SERPAVI vivienda colectiva) 2024" if s["y"] == "ln_alq_2024" else "Δ ln del alquiler por m² 2019-2024"
        cf, mo = s["conley"], s["moran"]
        nota = (f"{s['desc']}. Asociación transversal (el orden temporal está invertido y no hay variación exógena): no se interpreta como efecto. {s['N']} municipios no sellados en {s['provincias']} provincias, "
                f"resultado {y_txt}. MCO con efectos de provincia: coeficiente {s['beta']:.4f} (error típico agrupado por provincia {s['se_cr1']:.4f}; IC95 t[{s['G'] - 1}] [{s['ic95'][0]:.4f}; {s['ic95'][1]:.4f}]); "
                f"p del WCR de Webb (B = {s['w']['B']}) = {s['w']['p_webb']:.3f}; error típico de Conley a 10 km {cf['se_conley']:.4f} ({cf['vecinos_medios_en_el_corte']:.1f} vecinos medios; APTO si el alcance de la dependencia no supera el corte, V18 montecarlo/conley); "
                f"Moran de los residuos (8 vecinos) I = {mo['I']} (p = {mo['p_permutacion']}). MDE {s['mde']['mde_gamma']:.4f} (sin referencia: diagnóstico, sin umbral). "
                f"El % de grandes tenedores es una cota inferior (tramo contado dentro del municipio); fuga declarada: los totales municipales de las ciudades con distritos sellados están en entrenamiento. "
                f"Webb en sección cruzada con efectos de provincia sin validar por Monte Carlo (etiqueta). Q BY de las variantes: {num(bh.get(k))}. {ref_titulares}.")
        clase = "ASOCIACIÓN"
        m.hecho(f"V18-{k}", f"Alquiler municipal por m² y % de viviendas de grandes tenedores: asociación transversal ({k})", 100 * s["beta"], 100 * s["ic95"][0], 100 * s["ic95"][1], unidad, "2019-2024", f"{s['N']} municipios", clase, nota)
        m.filas.append({"id": k, "familia": "E10", "estado": s["estado"], "repite_visto": "no", "N": s["N"], "G": s["G"], "resultado": s["y"], "regresor": s["x"], "coef": num(s["beta"]), "se_cr1": num(s["se_cr1"]),
                        "ic95_lo": num(s["ic95"][0]), "ic95_hi": num(s["ic95"][1]), "p_webb": num(s["w"]["p_webb"]), "se_conley_10km": num(cf["se_conley"]), "moran_I": mo["I"], "moran_p": mo["p_permutacion"],
                        "q_BY": num(bh.get(k)), "mde": num(s["mde"]["mde_gamma"]), "sd_regresor": num(s["sd_x"]), "estimable": True, "clasificacion_v18": clase if s["estado"] == "principal" else "no se clasifica", "nota": nota})
    pr = {k: S[k] for k in ("E10-A1", "E10-A1-d")}
    n_vars = [S[f"E10-A1{suf}-v{i}"]["beta"] for suf in ("", "-d") for i in (1, 2, 3, 4)]
    signo = {suf: float(np.mean([np.sign(S[f"E10-A1{suf}-v{i}"]["beta"]) == np.sign(S[f"E10-A1{suf}"]["beta"]) for i in (1, 2, 3, 4)])) for suf in ("", "-d")}
    res = {"rama": "v18/estimacion/e10", "pregunta": "¿Se asocia el peso de los grandes tenedores (titulares de más de 10 inmuebles) con el alquiler municipal por m² (nivel 2024 y variación 2019-2024)? Asociación transversal, sin variación exógena (E10-A1)",
           "capa": "C4", "datos": "SERPAVI municipal (vivienda colectiva), titularidad del Catastro 2024 (cota inferior), ADRH 2023 y población 2024 vía src/v18/sellado.filtrar; municipios no sellados",
           "N": {k: s["N"] for k, s in S.items()}, "metodo": "MCO con efectos de provincia; error agrupado por provincia con WCR de Webb (9.999); Conley a 10 km; Moran de los residuos; BY en variantes; MDE como diagnóstico",
           "estimacion": {k: {"coef": num(s["beta"]), "ic95_t": [num(s["ic95"][0]), num(s["ic95"][1])], "p_webb": num(s["w"]["p_webb"]), "q_BY": num(bh.get(k))} for k, s in S.items()},
           "ic95": {k: [num(s["ic95"][0]), num(s["ic95"][1])] for k, s in S.items()}, "p_ajustado": {"metodo": "fuera de la familia de Holm (tope ASOCIACIÓN, adenda 1.7); BY (10 %) en las variantes de cada resultado", "valores": {k: num(v) for k, v in bh.items()}},
           "nivel_evidencia": "EXPLORATORIO", "clasificacion_v18": "ASOCIACIÓN", "clasificacion_v18_por_especificacion": {r["id"]: r["clasificacion_v18"] for r in m.filas},
           "diagnosticos": {"I5_mismo_signo_variantes": signo, "mde": {k: {"mde": num(s["mde"]["mde_gamma"]), "sd_regresor": num(s["sd_x"])} for k, s in S.items()}, "moran": {k: s["moran"] for k, s in pr.items()},
                            "conley_10km": {k: s["conley"] for k, s in pr.items()}, "dato_titularidad": "cota inferior: el tramo se cuenta dentro del municipio (la mediana municipal es 0)", "datos_parciales_v17": ref_titulares},
           "fuera_muestra": None, "notas": [ROTULO, "Tope ASOCIACIÓN: sin variación exógena y con el orden temporal invertido.", "Webb en sección cruzada con efectos de provincia y Moran no tienen Monte Carlo propio: se publican con esa etiqueta.",
                                            "Desviaciones y motivos: docs/v18/desviaciones_e4_e7b_e10_e12.md."]}
    return res


# ---------------------------------------------------------------------------------------------- informes
def informe_modelo(m: Modulo, res: dict, titulo: str, lecturas: list[str], cols: list[str]) -> None:
    t = pd.DataFrame(m.filas)
    t.to_csv(m.out / "tabla.csv", index=False)
    (m.out / "hechos.json").write_text(json.dumps(m.hechos, ensure_ascii=False, indent=1), encoding="utf-8")
    (m.out / "resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    L_ = [f"# {titulo}\n\n*{ROTULO}.*\n", "## Lectura\n"] + [f"- {x}" for x in lecturas]
    L_.append("\n## Tabla de especificaciones\n")
    L_.append(F.md_tabla(t, cols))
    L_.append("\n## Diagnósticos del pre-registro\n")
    L_.append("```json\n" + json.dumps(res["diagnosticos"], ensure_ascii=False, indent=1, default=str) + "\n```\n")
    (m.out / "informe.md").write_text("\n".join(L_), encoding="utf-8")
    m.reg.flush()


def main(rapido: bool = False, salida: Path | None = None) -> dict:
    reps = REPS_RAPIDO if rapido else REPS_FULL
    base = salida or BASE_OUT
    m4 = modulo_e4(base / "e4")
    m11 = modulo_e11(base / "e11")
    m12, S12, P12 = modulo_e12(base / "e12", reps)
    r12 = finalizar_e12(m12, S12, P12, reps)
    a1, a2 = S12["E12-A1"], S12["E12-A2"]
    c1, c2 = r12["clasificacion_v18_por_especificacion"].get("E12-A1"), r12["clasificacion_v18_por_especificacion"].get("E12-A2")
    informe_modelo(m12, r12, "E12 · Vivienda protegida y obra libre (estilo Chapelle)",
                   [f"**E12-A1** ({a1['G']} provincias × {a1['T']} años): 2SLS {a1['r']['beta']:.3f} viviendas libres iniciadas por vivienda protegida calificada; F efectivo {a1['r']['F_efectivo']:.2f}; AR 95 % {ar_texto(a1['r']['ar'])}; "
                    f"p Webb del AR en 0 = {a1['w']['p_webb']:.3f}; MDE(β) {a1['mde_beta']:.2f} frente a |Chapelle| = {abs(CHAPELLE)}. Clase provisional **{c1}**{' (estimación informativa, fuera de clasificación y de la familia de Holm: el MDE supera el umbral de la adenda 1.3)' if not a1['estimable'] else ''}.",
                    f"**E12-A2** (valor tasado real): 2SLS {a2['r']['beta']:.3f} % por 100 protegidas por 100 del parque; F efectivo {a2['r']['F_efectivo']:.2f}; AR {ar_texto(a2['r']['ar'])}; p Webb {a2['w']['p_webb']:.3f}. Clase provisional **{c2}**.",
                    "Mide la vivienda **protegida** (calificaciones definitivas), no la pública (E12-X1 NO ESTIMABLE por falta de promociones públicas por municipio y año: tarea del autor, punto 11).",
                    "Tope SUGESTIVO. Las variantes heredan la clase de su principal; E12-A1-v3 (libres terminadas) no se estima por falta de la clave de sellado."],
                   ["id", "estado", "muestra", "N", "G", "beta_2sls", "se_cr1", "F_efectivo", "ar_tipo", "ar_lo", "ar_hi", "p_webb", "p_holm", "q_BY_variantes", "mde_beta", "umbral_mde", "estimable", "clasificacion_v18"])
    m10, S10, d10 = modulo_e10(base / "e10", reps)
    r10 = finalizar_e10(m10, S10, d10)
    s = S10["E10-A1"]
    sd_ = S10["E10-A1-d"]
    informe_modelo(m10, r10, "E10 · Grandes tenedores y alquiler municipal (asociación transversal)",
                   [f"**E10-X1** NO ESTIMABLE (tres cortes de titularidad; tarea del autor: puntos 9, 10, 7 y 6).",
                    f"**E10-A1** ({s['N']} municipios no sellados, {s['G']} provincias): coeficiente {100 * s['beta']:.3f} % del alquiler por m² por punto de viviendas de grandes tenedores (IC95 t [{100 * s['ic95'][0]:.3f}; {100 * s['ic95'][1]:.3f}]; p Webb {s['w']['p_webb']:.3f}; Conley 10 km {100 * s['conley']['se_conley']:.3f}).",
                    f"**E10-A1-d** (variación 2019-2024, {sd_['N']} municipios): {100 * sd_['beta']:.3f} (IC95 t [{100 * sd_['ic95'][0]:.3f}; {100 * sd_['ic95'][1]:.3f}]; p Webb {sd_['w']['p_webb']:.3f}).",
                    "**ASOCIACIÓN** (tope): sin variación exógena y con el orden temporal invertido. El % de grandes tenedores es una cota inferior (tramo contado dentro del municipio). " + r10["diagnosticos"]["datos_parciales_v17"] + "."],
                   ["id", "estado", "N", "G", "resultado", "regresor", "coef", "se_cr1", "ic95_lo", "ic95_hi", "p_webb", "se_conley_10km", "moran_I", "moran_p", "q_BY", "mde", "clasificacion_v18"])
    return {"e4": m4, "e11": m11, "e12": r12, "e10": r10, "n_hechos": {"e4": len(m4.hechos), "e11": len(m11.hechos), "e12": len(m12.hechos), "e10": len(m10.hechos)}}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--salida", default=None)
    a = ap.parse_args()
    r = main(a.rapido, Path(a.salida) if a.salida else None)
    print("e4_e10_e12:", r["n_hechos"])
