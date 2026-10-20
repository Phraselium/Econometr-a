"""V18 · E3-A3 y E3-P-H4 (municipal) · panel municipal de alquiler SERPAVI y shift-share con las cuotas del padrón de 2003.

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. Sin red; SEED 20261010.
Construcción tomada de la réplica H4 de V16 (src/v16/replica/h4.py) en la muestra V18 (sin municipios de v6, V15 ni V16; sellado.filtrar):
- cuotas S_mc = población de la nacionalidad c / población total del municipio en 2003 (padrón municipal);
- crecimiento nacional del stock de c entre 1 de enero de t-1 y t, sin el propio municipio: G_ct = (n1 - n0)/n0 con n = suma de la muestra menos el municipio;
- z_mt = Σ_c S_mc·G_ct; x_mt = 100·(F[t] - F[t-1])/P[t-1] (extranjeros del padrón); y_mt = 100·Δ ln alquiler SERPAVI (vivienda colectiva) del año t;
- efectos provincia-año; sin los municipios de Barcelona y València ciudad (H4); al menos seis años por municipio (H4).
A3 usa los 28 países individuales del padrón, ventana 2014-2022 y pesos de población de 1 de enero de 2013; P-H4 es la réplica (23 orígenes sin Alemania, Francia, Italia,
Portugal y Reino Unido; ventana 2012-2022; sin pesos).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import _e359_comun as K

AGG = ["Extranjera", "Total", "Española", "De Africa", "De América", "De Asia", "Europa (sin España)", "Oceanía y Apátridas", "País de Europa menos UE27_2020",
       "País de Europa menos UE28", "País de la UE27_2020 sin España", "País de la UE28 sin España"]
RES = ["Alemania", "Francia", "Italia", "Portugal", "Reino Unido"]
GRANDES = ("08019", "46250")


class DatosMunicipal:
    def __init__(self, años_stock=range(2003, 2023)):
        ruta = K.RAW / "v9" / "ine_padron_nacionalidad" / "padron_nacionalidad_2003_2022.csv.gz"
        usar = {str(a) for a in años_stock} | {"2003"}
        partes = []
        for ch in pd.read_csv(ruta, dtype=str, usecols=["anio", "cod_municipio", "nacionalidad", "poblacion"], chunksize=1_000_000):
            partes.append(ch[ch["anio"].isin(usar)])
        d = pd.concat(partes, ignore_index=True)
        d["valor"] = pd.to_numeric(d["poblacion"], errors="coerce")
        d = K.filtrar(d.rename(columns={"cod_municipio": "cod", "anio": "periodo"})[["cod", "periodo", "nacionalidad", "valor"]], "cod", "municipio", "periodo",
                      "padron_municipal_nacionalidad", "A")
        d["cod"] = d["cod"].astype(str).str.zfill(5)
        W = d.pivot_table(index=["cod", "periodo"], columns="nacionalidad", values="valor", aggfunc="first")
        self.paises = [c for c in W.columns if c not in AGG]
        self.N = {c: W[c].unstack("periodo") for c in self.paises + ["Extranjera", "Total"]}
        for k in self.N:
            self.N[k].columns = [int(c) for c in self.N[k].columns]
        self.municipios = sorted(self.N["Total"].index)
        s = K.leer_hechos("serpavi_alquiler_m2_mediana", "municipio", "A", desag="tipologia=VC")
        s["cod"] = s["territorio_codigo"].astype(str).str.zfill(5)
        P = s.pivot_table(index="cod", columns="periodo", values="valor", aggfunc="first")
        P.columns = [int(c) for c in P.columns]
        self.P = P.where(P > 0)
        try:
            pt = K.leer_hechos("p_tasado", "municipio", "A")
            pt["cod"] = pt["territorio_codigo"].astype(str).str.zfill(5)
            Q = pt.pivot_table(index="cod", columns="periodo", values="valor", aggfunc="first")
            Q.columns = [int(c) for c in Q.columns]
            self.Q = Q.where(Q > 0)
        except Exception:
            self.Q = None
        self.con_distritos_sellados = K.sellado.municipios_con_distritos_sellados(K.manifiesto())

    def _gcrec(self, orig: list[str], t: int) -> pd.DataFrame:
        """Crecimiento nacional del stock de cada origen entre 1 de enero de t-1 y t sin el propio municipio (H4)."""
        G = {}
        for c in orig:
            a1, a0 = self.N[c][t], self.N[c][t - 1]
            T1, T0 = a1.sum(), a0.sum()
            n1, n0 = T1 - a1, T0 - a0
            G[c] = (n1 - n0) / n0.replace(0, np.nan)
        return pd.DataFrame(G)

    def panel(self, ventana=(2014, 2022), origenes: list[str] | None = None, base: int = 2003, peso_pob0: bool = False, mun_min_pob: int | None = None,
              sin_distritos_sellados: bool = False, resultado: str = "alquiler", min_años: int = 6, con_lag: bool = False, lag: int = 4,
              solo_resultado: bool = False) -> dict:
        orig = [c for c in (origenes or self.paises)]
        tot, ext = self.N["Total"], self.N["Extranjera"]
        S = pd.DataFrame({c: self.N[c][base] / tot[base] for c in orig})
        años = list(range(ventana[0], ventana[1] + 1))
        P = self.P if resultado == "alquiler" else self.Q
        if P is None:
            raise ValueError("sin valor tasado municipal")
        filas, comps = [], []
        for t in años:
            if t not in P.columns or (t - 1) not in P.columns:
                continue
            y = 100 * np.log(P[t] / P[t - 1])
            if solo_resultado:
                df = pd.DataFrame({"y": y}).dropna()
                df["año"], df["cod"] = t, df.index
                filas.append(df)
                continue
            G = self._gcrec(orig, t)
            C = S.mul(G.fillna(0))
            C = C.where(G.notna().any(axis=1), np.nan)
            z = (S * G).sum(axis=1, min_count=1)
            x = 100 * (ext[t] - ext[t - 1]) / tot[t - 1]
            df = pd.DataFrame({"y": y, "x": x, "z": z})
            if con_lag:
                Gl = self._gcrec(orig, t - lag)
                df["zlag"] = (S * Gl).sum(axis=1, min_count=1)
            df = df.dropna()
            df["año"], df["cod"] = t, df.index
            filas.append(df)
            comps.append(C.loc[df.index])
        D = pd.concat(filas, ignore_index=True)
        ZC = pd.concat(comps, ignore_index=True).to_numpy(float) if comps else None
        keep = ~D["cod"].isin(GRANDES)
        if sin_distritos_sellados:
            keep &= ~D["cod"].isin(self.con_distritos_sellados)
        if mun_min_pob:
            ref = 2013 if 2013 in tot.columns else ventana[0] - 1
            keep &= D["cod"].map(tot[ref]).fillna(0) >= mun_min_pob
        D = D[keep]
        if ZC is not None:
            ZC = ZC[keep.to_numpy()]
        cnt = D.groupby("cod")["y"].transform("size")
        k2 = (cnt >= min_años).to_numpy()
        D = D[k2].copy()
        if ZC is not None:
            ZC = ZC[k2]
        D["prov"] = D["cod"].str[:2]
        D["pv"] = D["prov"] + "_" + D["año"].astype(str)
        w = D["cod"].map(tot[ventana[0] - 1]).to_numpy(float) if peso_pob0 else None
        return {"D": D.reset_index(drop=True), "w": w, "origenes": orig, "S": S, "ZC": ZC}
