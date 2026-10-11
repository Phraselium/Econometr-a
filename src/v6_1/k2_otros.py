"""K2 (v6.1): otras conclusiones que cambiaron de signo o de mercado entre versiones (empleo, renta, iniciadas, turisticos).

Cadenas ligeras de 4-6 pasos, una dimension cada vez, con el paso anterior estimado en la MISMA muestra. Se llama desde
k2_inmigracion.main(). Todo C4; sin lenguaje causal.
"""
from __future__ import annotations

import numpy as np

import k2_datos as kd
import k2_lib as kl

B = "otros"


def _chain(U, name, pasos, registrar, fila, estimar, comunes, mercados=("alquiler", "compra")):
    prev = None
    for pid, desc, s, dim in pasos:
        for mk in mercados:
            y = s["ya"] if mk == "alquiler" else s["yc"]
            if y is None:
                continue
            mask, sp = None, None
            if prev is not None:
                sp = dict(prev)
                if dim != "periodo":
                    sp["a0"], sp["a1"] = s["a0"], s["a1"]
                    mask = comunes(U, sp, s, mk) if (sp["ya" if mk == "alquiler" else "yc"] is not None) else None
            r = estimar(U, s, mk, mask)
            f = fila(r, s, mk)
            if sp is not None and (sp["ya" if mk == "alquiler" else "yc"] is not None):
                fp = fila(estimar(U, sp, mk, mask), sp, mk)
                f.update(coef_anterior_misma_muestra=fp["coef"], ic_anterior=f"[{fp['lo']:.2f}; {fp['hi']:.2f}]",
                         N_anterior=fp["N"])
            registrar(f, B, name, pid, desc, "anterior en la misma muestra" if dim != "periodo" else "el periodo cambia")
        prev = s


def run(U, meta, CTX, FILAS, registrar, fila, estimar, spec, comunes, REG, OUT):
    nuc = kd.NUCLEO
    # --- cadenas de v2 a v6 para empleo, renta e iniciadas
    defs = [
        ("empleo", "g_ocup", "l1_ln_ocupados_miles", "ocupados (EPA)", "l1_ln_ocupados_miles"),
        ("renta", "g_pib_pc", "l1_ln_pib_pc", "PIB por habitante", "l1_ln_pib_pc"),
        ("iniciadas", "g_inic", "l1_ln_iniciadas_libres", "viviendas libres iniciadas", "l1_ln_iniciadas_libres"),
    ]
    for nom, gx, lx, txt, propio in defs:
        ctrl = [c for c in nuc if c != propio]
        fd = spec(xs=[gx], a0=2004, a1=2023, ya="y_alq", yc="y_pre", metodo="primeras diferencias, EF prov+anio",
                  k=10.0, unidad_x=f"+10 pp de crecimiento anual ({txt})", medida_alq="IPC alquiler (stock)",
                  medida_precio="valor tasado MIVAU (real)")
        pasos = [
            (f"{nom}-0", "base v2: variacion anual, 2004-2023", fd, None),
            (f"{nom}-1", "periodo: 2016-2023", {**fd, "a0": 2016, "a1": 2023}, "periodo"),
            (f"{nom}-2", "metodo: niveles ln con EF dobles (v6)",
             {**fd, "a0": 2016, "a1": 2023, "xs": [lx], "ya": "lv_ipc6", "yc": "lv_tas6", "k": 0.1,
              "metodo": "MCO niveles ln, EF prov+anio", "unidad_x": f"+10 % ({txt}, t-1)",
              "medida_precio": "valor tasado MIVAU"}, "metodo"),
            (f"{nom}-3", "medida de alquiler: IPC -> SERPAVI",
             {**fd, "a0": 2016, "a1": 2023, "xs": [lx], "ya": "lv_alq6", "yc": "lv_tas6", "k": 0.1,
              "medida_alq": "SERPAVI VC (stock)", "metodo": "MCO niveles ln, EF prov+anio",
              "unidad_x": f"+10 % ({txt}, t-1)", "medida_precio": "valor tasado MIVAU"}, "medida"),
            (f"{nom}-4", "controles: + nucleo de M2",
             {**fd, "a0": 2016, "a1": 2023, "xs": [lx], "ya": "lv_alq6", "yc": "lv_tas6", "k": 0.1, "ctrl": ctrl,
              "medida_alq": "SERPAVI VC (stock)", "metodo": "MCO niveles ln, EF prov+anio + nucleo M2",
              "unidad_x": f"+10 % ({txt}, t-1)", "medida_precio": "valor tasado MIVAU"}, "controles"),
        ]
        if nom == "iniciadas":
            pasos.append((f"{nom}-5", "periodo: 2021-2023 (ventana de M1a S0), sin controles",
                          {**pasos[3][2], "a0": 2021, "a1": 2023, "ctrl": []}, "periodo"))
            pasos.append((f"{nom}-6", "controles: + turisticos (ln_vut, solo desde 2020)",
                          {**pasos[3][2], "a0": 2021, "a1": 2023, "ctrl": ["l1_ln_vut"]}, "controles"))
        _chain(U, nom, pasos, registrar, fila, estimar, comunes)
    # --- BMA aproximado (BIC) del nucleo: PIP de empleo, renta, iniciadas en alquiler y compra
    bma_otros = {}
    for mk, y, a0, a1 in [("compra", "lv_tas6", 2016, 2024), ("alquiler", "lv_alq6", 2016, 2023)]:
        m = U[U["anio"].between(a0, a1)].dropna(subset=["l1_share_ext_pob"] + nuc + [y])
        r, n, nm = kl.bma_bic(m, y, ["l1_share_ext_pob"] + nuc)
        bma_otros[mk] = dict(res=r, N=n)
        for v, d in r.items():
            REG.log("K2", f"BMA_BIC_otros|{mk}|{v}", f"{y}~nucleo (BMA con BIC, EF prov+anio)", a0, a1, n, np.nan, np.nan,
                    np.nan, np.nan, d["media"], np.nan, f"PIP={d['pip']:.3f}; C4")
    CTX["bma_otros"] = bma_otros
    # --- turisticos (VUT): solo desde 2020
    tur = spec(xs=["l1_ln_vut"], k=0.1, a0=2021, a1=2023, ya="lv_alq6", yc="lv_tas6", medida_alq="SERPAVI VC (stock)",
               medida_precio="valor tasado MIVAU", metodo="MCO niveles ln, EF prov+anio",
               unidad_x="+10 % de viviendas turisticas (t-1)")
    pasos = [
        ("turisticos-0", "base v6 (M1a S0): provincia, SERPAVI, 2021-2023", tur, None),
        ("turisticos-1", "medida de alquiler: SERPAVI -> IPC", {**tur, "ya": "lv_ipc6", "medida_alq": "IPC alquiler (stock)"},
         "medida"),
        ("turisticos-2", "metodo: primeras diferencias", {**tur, "xs": ["dl1_ln_vut"], "ya": "y_alq6", "yc": "y_pre_t6",
                                                         "a0": 2022, "a1": 2023, "metodo": "primeras diferencias, EF prov+anio",
                                                         "unidad_x": "+10 % de variacion de viviendas turisticas (t-1)"},
         "metodo"),
        ("turisticos-3", "controles: + poblacion", {**tur, "xs": ["dl1_ln_vut"], "ya": "y_alq6", "yc": "y_pre_t6",
                                                    "a0": 2022, "a1": 2023, "ctrl": ["dl1_ln_pob"],
                                                    "metodo": "primeras diferencias, EF prov+anio + poblacion",
                                                    "unidad_x": "+10 % de variacion de viviendas turisticas (t-1)"}, "controles"),
    ]
    _chain(U, "turisticos", pasos, registrar, fila, estimar, comunes)
    # nivel municipal (v2): ln viviendas turisticas municipales t-1 -> SERPAVI municipal
    mun = kd.municipal(meta["codes"])
    mun["cod"] = mun["cod_muni"]
    mun["cod_prov_cl"] = mun["cod_prov"]
    if CTX.get("smoke"):
        mun = mun[mun["cod_muni"].astype(str).str[:3].isin(mun["cod_muni"].astype(str).str[:3].unique()[:30])]
    for y, mk, med, a1 in [("lv_ser", "alquiler", "SERPAVI VC (stock)", 2023), ("lv_tas", "compra", "valor tasado municipal", 2023)]:
        s = spec(xs=["l1_ln_vut_m"], k=0.1, a0=2021, a1=a1, ya=(y if mk == "alquiler" else None),
                 yc=(y if mk == "compra" else None), nivel="municipio (v2, 41 prov. de entrenamiento)", cl="cod_prov_cl",
                 medida_alq=med, medida_precio=med, metodo="MCO niveles ln, EF municipio+anio, cluster provincia",
                 unidad_x="+10 % de viviendas turisticas municipales (t-1)")
        r = estimar(mun, s, mk, None)
        registrar(fila(r, s, mk), B, "turisticos", "turisticos-4", "nivel: municipio", "municipal; cluster provincia")
