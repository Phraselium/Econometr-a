"""V18 · E3 (inmigración, González y Ortega) · construcción de los paneles provinciales y del instrumento de asentamiento histórico.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. Sin red; SEED 20261010. Lectura con sellado (ver _e359_datos).
Definiciones (docs/v18/desviaciones_e3_e5_e9.md, D-E359-3 a D-E359-10):
- x_pt = 100·(F[t+1] − F[t]) / P[t] (stock de extranjeros del padrón a 1 de enero; entre t y t+1 entran los del año t); R2: Δ ln población de 15 a 64 años.
- z_pt = 100·Σ_c s_pc·M_ct / P[t] con s_pc = stock del grupo c en p / stock nacional del grupo (Censo de 2001) y M_ct las entradas nacionales del grupo en el año t.
- Controles: efectos región-año (5 NUTS 1 sin sellar), cuota de empleo en construcción de 2001 × año, costa × año (17 provincias).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

import _e359_comun as K
import _e359_datos as D

GRUPOS = D.GRUPOS
# Padrón de 2003 por nacionalidad (variante v2): correspondencia aproximada entre los 6 bloques del padrón y los 8 grupos (D-E359-14)
PADRON_BLOQUES = ["UE15_aprox", "Europa_resto_AELC", "Africa", "America", "Asia", "Oceania_apatridas"]
SEXTETO = {  # bloque -> columnas de grupo cuyas entradas se suman
    "UE15_aprox": ["G1_UE15"], "Europa_resto_AELC": ["G2_AELC", "G3_Europa_resto"], "Africa": ["G4_Africa_norte", "G5_Africa_resto"],
    "America": ["G6_America_latina_Caribe"], "Asia": ["G7_Asia"], "Oceania_apatridas": ["G8_resto_mundo"]}


@dataclass
class Panel:
    cfg: dict
    y: np.ndarray
    x: np.ndarray
    z: np.ndarray
    zc: np.ndarray                 # componentes del instrumento por origen (n, K); z = zc.sum(1)
    prov: np.ndarray
    año: np.ndarray
    w: np.ndarray | None
    C: np.ndarray
    cols_C: list[str] = field(default_factory=list)
    origenes: list[str] = field(default_factory=list)
    expo: np.ndarray | None = None  # exposición e_pc,t (n, K) = 100·s_pc/P[t]: cuotas BHJ (z = Σ e·g)
    g: np.ndarray | None = None     # choques g_ct (n, K) = M_ct
    z_lag: np.ndarray | None = None


class DatosE3:
    def __init__(self):
        self.P = list(K.PROVINCIAS_ENTRENAMIENTO)
        self.fl = D.flujos_por_grupo()
        self.stock = D.censo2001_grupos()
        self.S = D.shares_localizacion(self.stock, self.P)[GRUPOS]
        self.vt = D.valor_tasado_anual(self.P)
        self.ini = D.iniciadas_anual(self.P)
        self.ter = D.terminadas_anual(self.P)
        self.pt = D.pob_prov("pob_total", self.P)
        self.pe = D.pob_prov("pob_extranj", self.P)
        pop = D.poblacion_edad(self.P)
        self.pop = pop
        self.tot = pop.xs("TOTAL", level="age")
        self.wap = pop.xs("Y15-64", level="age")
        self.p65 = pop.xs("Y_GE65", level="age")
        emp = D.empleo_entrenamiento(self.P)
        self.emp = emp
        tot01 = emp.xs("TOTAL", level="nace_r2")[2001]
        self.cuota_constr = (emp.xs("F", level="nace_r2")[2001] / tot01).reindex(self.P)
        self.cuota_indus = (emp.xs("B-E", level="nace_r2")[2001] / tot01).reindex(self.P)
        ext = self.stock["total_extranjeros"].reindex(self.P)
        noue = (self.stock["total_extranjeros"] - self.stock[GRUPOS[0]] - self.stock[GRUPOS[1]]).reindex(self.P)
        self.cuota_noue = noue / self.stock["pob_total"].reindex(self.P)
        self.cuota_ext01 = ext / self.stock["pob_total"].reindex(self.P)
        self.pib = None
        self.sp = D.serpavi_prov("tipologia=VC")
        self.ipva = D.ipva_prov()
        self.ipc = D.ipc_alquiler_prov()
        self.macro = pd.Series({p: K.MACRO[p] for p in self.P})
        self.costa = pd.Series({p: float(p in K.COSTA) for p in self.P})
        self.fl_interp = self._interpolar_2003()
        self.S_padron = None
        self._padron2003()

    # ---- flujos con 2003 interpolado (solo variante marcada)
    def _interpolar_2003(self) -> pd.DataFrame:
        fl = self.fl.copy()
        comp = fl[GRUPOS].div(fl[GRUPOS].sum(axis=1), axis=0)
        d = pd.read_csv(K.RAW / "eurostat_inmigracion_anual.csv", keep_default_na=False)
        d["valor"] = pd.to_numeric(d["valor"], errors="coerce")
        d["periodo"] = d["periodo"].astype(str)
        d["territorio_codigo"] = "00"
        d = K.filtrar(d, "territorio_codigo", "nacional", "periodo", "ine_migraciones_nacionalidad", "A")
        w = d.pivot_table(index="citizen", columns="periodo", values="valor", aggfunc="first")
        tot03 = float(w.loc["TOTAL", "2003"])
        nat = (w.loc["NAT", "2002"] / w.loc["TOTAL", "2002"] + w.loc["NAT", "2004"] / w.loc["TOTAL", "2004"]) / 2
        ext03 = tot03 * (1 - nat)
        c03 = (comp.loc[2002] + comp.loc[2004]) / 2
        fl.loc[2003, GRUPOS] = c03 * ext03
        fl.loc[2003, "total_extranjeros"] = ext03
        return fl

    # ---- cuotas del padrón de 2003 (variante v2): 6 bloques continentales
    def _padron2003(self):
        """Cuotas de localización del padrón de 2003 en los 6 bloques de nacionalidad que el padrón provincial permite (D-E359-14). El padrón de las
        provincias selladas no se lee: la cuota se normaliza dentro de la muestra y se escala por la fracción de la muestra en el stock nacional del
        bloque en el Censo de 2001, para que la escala de z sea la de la principal."""
        p = K.leer_hechos("padron_pob_nacionalidad", "provincia", "A")
        p = p[p["periodo"] == "2003"].copy()
        p["nac"] = p["desagregacion"].str.replace("nacionalidad=", "", regex=False)
        W = p.pivot_table(index="territorio_codigo", columns="nac", values="valor", aggfunc="first")
        W = W.loc[[q for q in W.index if q in self.P]]
        bloques = pd.DataFrame({
            "UE15_aprox": W["País de la UE28 sin España"] - W["Rumanía"] - W["Bulgaria"] - W["Polonia"],
            "Europa_resto_AELC": W["País de Europa menos UE28"] + W["Rumanía"] + W["Bulgaria"] + W["Polonia"],
            "Africa": W["De Africa"], "America": W["De América"], "Asia": W["De Asia"], "Oceania_apatridas": W["Oceanía y Apátridas"]}).reindex(self.P)
        dentro = bloques.div(bloques.sum(axis=0), axis=1)
        cen = self.stock
        frac = {}
        for b_, grp in SEXTETO.items():
            tot = cen[grp].sum(axis=1)
            frac[b_] = float(tot.reindex(self.P).sum() / tot.sum())
        self.S_padron = dentro.mul(pd.Series(frac))

    # ---- piezas
    def flujos(self, interp: bool = False) -> pd.DataFrame:
        return self.fl_interp if interp else self.fl

    def _dummies(self, claves: list, nombre: str) -> tuple[np.ndarray, list[str]]:
        d = pd.get_dummies(pd.Series(claves), dtype=float)
        return d.to_numpy(), [f"{nombre}:{c}" for c in d.columns]

    # ---- panel principal
    def panel(self, cfg: dict) -> Panel:
        t0, t1 = cfg["ventana"]
        sin = set(cfg.get("sin_anios", [] if cfg.get("interpolar_2003") else [2003]))
        años = [t for t in range(t0, t1 + 1) if t not in sin]
        FL = self.flujos(cfg.get("interpolar_2003", False))
        tipo_x = cfg["x"]
        gx = set(cfg.get("grupos_excl", []))
        if cfg.get("shares") == "padron2003":
            S, orig = self.S_padron, PADRON_BLOQUES
            FLg = pd.DataFrame({b: FL[SEXTETO[b]].sum(axis=1) for b in PADRON_BLOQUES})
            if gx:
                orig = [o for o in orig if not (o == "UE15_aprox" and {"G1_UE15", "G2_AELC"} & gx)]
                if "G2_AELC" in gx and "G1_UE15" not in gx:
                    pass
        else:
            S, orig, FLg = self.S, GRUPOS, FL[GRUPOS]
            orig = [o for o in orig if o not in gx]
        excl = set(cfg.get("excl_prov", []))
        provs = [p for p in self.P if p not in excl]
        filas = []
        for p in provs:
            for t in años:
                pt_t = self.pt.at[p, t] if t in self.pt.columns else np.nan
                if tipo_x == "pp_ext":
                    if (t + 1) not in self.pe.columns or t not in self.pe.columns:
                        continue
                    base, x = pt_t, 100.0 * (self.pe.at[p, t + 1] - self.pe.at[p, t]) / pt_t
                elif tipo_x in ("dln_wap", "dln_pob"):
                    ser = self.wap if tipo_x == "dln_wap" else self.tot
                    if (t + 1) not in ser.columns or t not in ser.columns:
                        continue
                    base, x = ser.at[p, t], float(np.log(ser.at[p, t + 1] / ser.at[p, t]))
                else:
                    raise ValueError(tipo_x)
                if base is None or not np.isfinite(base) or not np.isfinite(x):
                    continue
                esc = 100.0 if tipo_x == "pp_ext" else 1.0
                if t not in FLg.index or FLg.loc[t, orig].isna().any():
                    continue
                e = esc * S.loc[p, orig].to_numpy(float) / base
                g = FLg.loc[t, orig].to_numpy(float)
                y = self._y(cfg, p, t)
                if y is None or not np.isfinite(y):
                    continue
                zlag = np.nan
                if cfg.get("con_lag"):
                    tl = t - cfg.get("lag", 4)
                    if tl in FLg.index and not FLg.loc[tl, orig].isna().any():
                        zlag = float(e @ FLg.loc[tl, orig].to_numpy(float))
                filas.append((p, t, y, x, e, g, zlag))
        if not filas:
            raise ValueError(f"panel vacío en {cfg.get('id')}")
        prov = np.array([f[0] for f in filas])
        año = np.array([f[1] for f in filas])
        y = np.array([f[2] for f in filas])
        x = np.array([f[3] for f in filas])
        E = np.vstack([f[4] for f in filas])
        G = np.vstack([f[5] for f in filas])
        zl = np.array([f[6] for f in filas])
        zc = E * G
        z = zc.sum(axis=1)
        if cfg.get("con_lag"):
            ok = np.isfinite(zl)
            prov, año, y, x, E, G, zc, z, zl = (a[ok] for a in (prov, año, y, x, E, G, zc, z, zl))
        w = self._peso(cfg, prov, año)
        C, cols = self._controles(cfg, prov, año, zl if cfg.get("con_lag") else None)
        return Panel(cfg, y, x, z, zc, prov, año, w, C, cols, list(orig), E, G, zl if cfg.get("con_lag") else None)

    # ---- resultado
    def _y(self, cfg: dict, p: str, t: int):
        ty = cfg["y"]
        try:
            if ty == "dprecio":
                return float(self.vt.at[p, t] - self.vt.at[p, t - 1])
            if ty == "dlnp":
                return float(np.log(self.vt.at[p, t] / self.vt.at[p, t - 1]))
            if ty == "dlnp100":
                return 100.0 * float(np.log(self.vt.at[p, t] / self.vt.at[p, t - 1]))
            if ty in ("ini_pc", "ter_pc"):
                s = self.ini if ty == "ini_pc" else self.ter
                return 100.0 * float(s.at[p, t]) / float(self.tot.at[p, t])
            if ty in ("dlnini", "dlnter"):
                s = self.ini if ty == "dlnini" else self.ter
                a, b = float(s.at[p, t]), float(s.at[p, t - 1])
                return float(np.log(a / b)) if a > 0 and b > 0 else None
            if ty == "dlnrent100":
                return 100.0 * float(np.log(self.sp.at[p, t] / self.sp.at[p, t - 1]))
            if ty == "dlnipva100":
                return 100.0 * float(np.log(self.ipva.at[p, t] / self.ipva.at[p, t - 1]))
            if ty == "dlnipc100":
                return 100.0 * float(np.log(self.ipc.at[p, t] / self.ipc.at[p, t - 1]))
            if ty == "dln65":
                return float(np.log(self.p65.at[p, t + 1] / self.p65.at[p, t]))
        except (KeyError, ValueError, ZeroDivisionError):
            return None
        raise ValueError(ty)

    def _peso(self, cfg: dict, prov, año):
        pw = cfg.get("peso")
        if pw is None:
            return None
        if pw == "pob_ini":
            t0 = cfg["ventana"][0]
            base = self.pt[t0]
        else:
            base = self.tot[int(pw.replace("pob", ""))]
        return base.reindex(prov).to_numpy(float)

    def _controles(self, cfg: dict, prov, año, zlag=None):
        cols, bloques = [], []
        ry = [f"{self.macro[p]}_{t}" for p, t in zip(prov, año)]
        A, n = self._dummies(ry, "regionaño")
        bloques.append(A)
        cols += n
        ct = cfg.get("controles", {})
        ys = sorted(set(año))
        if ct.get("construccion", True):
            for t in ys:
                bloques.append(((año == t) * self.cuota_constr.reindex(prov).to_numpy())[:, None])
                cols.append(f"constr2001×{t}")
        if ct.get("costa", True):
            for t in ys:
                bloques.append(((año == t) * self.costa.reindex(prov).to_numpy())[:, None])
                cols.append(f"costa×{t}")
        if ct.get("ficticias"):
            for t in (2005, 2006):
                bloques.append(((año == t) * self.cuota_noue.reindex(prov).to_numpy())[:, None])
                cols.append(f"noUE2001×{t}")
        if cfg.get("fe_prov"):
            B, n = self._dummies(list(prov), "prov")
            bloques.append(B)
            cols += n
        if zlag is not None:
            bloques.append(np.asarray(zlag, float)[:, None])
            cols.append("z_rezagado")
        return np.hstack(bloques), cols

    # ---- preperiodo
    def pre_panel(self, cfg: dict, años_pre: list[int], desfase: int | None = None) -> Panel:
        """Panel del preperiodo con el mismo resultado; si desfase = d, el instrumento es el de t + d (placebo de fecha)."""
        c = dict(cfg)
        c["ventana"] = (min(años_pre), max(años_pre))
        c["sin_anios"] = [t for t in range(min(años_pre), max(años_pre) + 1) if t not in años_pre]
        # el resultado se toma del año t; x y z no se usan aquí salvo z (instrumento falso): se construyen aparte
        filas = []
        prov, año, y = [], [], []
        for p in self.P:
            if p in set(cfg.get("excl_prov", [])):
                continue
            for t in años_pre:
                yy = self._y(c, p, t)
                if yy is None or not np.isfinite(yy):
                    continue
                prov.append(p)
                año.append(t)
                y.append(yy)
        prov, año, y = np.array(prov), np.array(año), np.array(y)
        w = None
        if cfg.get("peso") is not None:
            w = self._peso(cfg, prov, año)
        C, cols = self._controles(cfg, prov, año)
        return Panel(c, y, np.full(len(y), np.nan), np.full(len(y), np.nan), np.zeros((len(y), 0)), prov, año, w, C, cols)

    def z_en(self, cfg: dict, prov, año, desfase: int = 0):
        """Instrumento z (misma definición que en el panel) para (p, t + desfase): flujos de t+desfase, población de t+desfase."""
        FL = self.flujos(cfg.get("interpolar_2003", False))
        gx = set(cfg.get("grupos_excl", []))
        orig = [o for o in GRUPOS if o not in gx]
        out = np.full(len(prov), np.nan)
        for i, (p, t) in enumerate(zip(prov, año)):
            tt = int(t) + desfase
            if tt not in FL.index or FL.loc[tt, orig].isna().any() or tt not in self.pt.columns:
                continue
            esc = 100.0 if cfg["x"] == "pp_ext" else 1.0
            base = self.pt.at[p, tt] if cfg["x"] == "pp_ext" else (self.wap.at[p, tt] if cfg["x"] == "dln_wap" else self.tot.at[p, tt])
            out[i] = esc * float(self.S.loc[p, orig].to_numpy(float) @ FL.loc[tt, orig].to_numpy(float)) / base
        return out
