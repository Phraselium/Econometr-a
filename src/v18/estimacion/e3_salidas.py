"""V18 · E3 · Holm por familia, B4, clasificación I1-I8 revisados y escritura de salidas (resultado.json, tabla.csv, informe.md, hechos.json, mde.csv, registro.csv).

Análisis V18; capa C4; pre-registro interno plan-replicacion-v18. I8 (réplica ciega, B6) queda pendiente: toda clase es «provisional, pendiente de I8».
"""
from __future__ import annotations

import time

import numpy as np
import pandas as pd

import _e359_comun as K

DATOS_QUE_FALTAN = (
    "(i) flujos de entrada por nacionalidad (país) y provincia de destino (EVR 1998-2021 y EMCR 2021-2024 por provincia y país: hoy solo por continente en el repositorio) para el choque sin la propia "
    "provincia y con los 16 grupos del original; (ii) el Censo de 2001 por país de nacionalidad y provincia (INE; hoy solo accesible por Eurostat con 8 grupos); (iii) más años de variación del "
    "instrumento dentro de región-año (padrón por provincia anterior a 2002) o unidades más finas (municipios con el padrón por nacionalidad anterior a 2003); (iv) las 11 provincias selladas de v6, "
    "que no se leen")


def ficha(r: dict) -> dict:
    ic = r.get("ic_webb_ar") or {}
    ar = r.get("ar") or {}
    return {"beta": r["beta"], "se": r["se"], "ic_lo": ic.get("lo"), "ic_hi": ic.get("hi"), "ic_acotado": ic.get("acotado"), "ic95_t": r["ic95_t"], "p_t": r["p_t"],
            "p_webb_ar": r["p_webb_ar"], "p_ar": ar.get("p_beta0"), "p_final": max(r["p_webb_ar"], ar.get("p_beta0", 0.0)), "F_eff": r["F_eff"], "pi": r["pi"], "rf": r["rf"],
            "n": r["n"], "G": r["G"], "ar_lo": ar.get("lo"), "ar_hi": ar.get("hi"), "ar_tipo": ar.get("tipo"), "ar_acotado": ar.get("acotado"), "mco": r["mco"]["beta"],
            "ic90": (r.get("ic90_webb_ar") or {})}


def etiqueta_i6(f: dict, ref: dict) -> dict:
    """I6 como etiqueta (adenda 1.2): razón nuestra/referencia en [1/3; 3], o solape de los IC95 si el EE de la referencia < ½|coeficiente| y nuestro IC95 no es más de 3 veces más ancho."""
    razon = f["beta"] / ref["v"]
    coherente = 1 / 3 <= razon <= 3
    via = "razón"
    if not coherente and f["ic_lo"] is not None and np.isfinite(f["ic_lo"]) and np.isfinite(f["ic_hi"]) and ref["se"] < 0.5 * abs(ref["v"]):
        lo, hi = ref["v"] - 1.96 * ref["se"], ref["v"] + 1.96 * ref["se"]
        if (f["ic_hi"] - f["ic_lo"]) <= 3 * (hi - lo) and f["ic_lo"] <= hi and f["ic_hi"] >= lo:
            coherente, via = True, "solape de IC95"
    return {"razon": razon, "coherente": bool(coherente), "via": via, "referencia": ref["nombre"], "estado_ficha": ref["estado"],
            "texto": f"{'coherente' if coherente else 'no coherente'} con {ref['nombre']} ({ref['estado']}), razón {razon:.2f}"}


def tost_ref(f: dict, delta: float) -> dict:
    ic = f.get("ic90") or {}
    if not ic or ic.get("lo") is None or not np.isfinite(ic.get("lo", np.nan)) or not np.isfinite(ic.get("hi", np.nan)):
        return {"equivalente": False, "ic90": None, "delta": delta}
    return {"equivalente": bool(ic["lo"] > -delta and ic["hi"] < delta), "ic90": (ic["lo"], ic["hi"]), "delta": delta}


def escribir(E3, dat, mun, specs, mspecs, mde_tab, res, ne, pd4, pq3, reg, B, t0):
    REF = E3.REF
    SAL = E3.SALIDA
    SAL.mkdir(parents=True, exist_ok=True)
    todas = [dict(s, tipo="prov") for s in specs] + [dict(s, tipo="mun", cfg=s["cfgm"]) for s in mspecs]
    por_id = {s["id"]: s for s in todas}
    # ---- familia de Holm: principales y coprincipales estimables (adenda 1.7)
    fam = {}
    for s in todas:
        if s["rol"] in ("principal", "coprincipal") and s["id"] in res:
            fam[s["id"]] = ficha(res[s["id"]])["p_final"]
    fam["E3-P-D4"] = max(pd4["valor tasado"]["p_webb_ar"], pd4["valor tasado"]["p_ar"])
    fam["E3-P-Q3c1"] = pq3["p_webb"]
    ph = K.holm_dict(fam) if hasattr(K, "holm_dict") else K.holm(fam)
    print(f"[{time.time() - t0:5.0f}s] Holm: m = {len(fam)}: " + ", ".join(f"{k}: p {fam[k]:.3f} → {ph[k]:.3f}" for k in fam), flush=True)
    # ---- diagnósticos de las principales estimables
    diag = {}
    for s in todas:
        if s["rol"] != "principal" or s["id"] not in res:
            continue
        r = res[s["id"]]
        if s["tipo"] == "prov":
            diag[s["id"]] = E3.diag_principal(dat, s, r, B)
            if s["id"] == "E3-A5":
                diag[s["id"]]["particion"] = E3.parcial_a5(dat, s, B)
        else:
            cm = E3.cfg_municipal(mun, s["cfgm"])
            diag[s["id"]] = EX_diag(E3, mun, cm, r, REF[s["ref"]]["v"], B)
        print(f"[{time.time() - t0:5.0f}s] diagnósticos {s['id']} listos", flush=True)
    # ---- variantes: BY y robustez
    var_por_padre: dict[str, list[str]] = {}
    for s in todas:
        if s["rol"] == "variante" and s["id"] in res and not s.get("holgura"):
            var_por_padre.setdefault(s["padre"], []).append(s["id"])
    qby = {}
    for padre, vs in var_por_padre.items():
        qby.update(K.by_qvalores({v: ficha(res[v])["p_final"] for v in vs}))
    # ---- clasificación
    clas = {}
    for s in todas:
        if s["rol"] == "variante":
            continue
        sid = s["id"]
        ref = REF[s["ref"]]
        if sid in ne:
            clas[sid] = K.clasificar({"estimable": False, "motivo_no_estimable": ne[sid]})
            continue
        if sid not in res:
            continue
        f = ficha(res[sid])
        if s["rol"] == "coprincipal":
            clas[sid] = K.clasificar({"coprincipal": True})
            continue
        d = diag[sid]
        # robustez I5
        padre_vs = var_por_padre.get(sid, [])
        signo = np.sign(f["beta"])
        misma = [np.sign(ficha(res[v])["beta"]) == signo for v in padre_vs]
        solape = []
        for v in padre_vs:
            fv = ficha(res[v])
            if None in (fv["ic_lo"], fv["ic_hi"], f["ic_lo"], f["ic_hi"]):
                continue
            solape.append(bool(fv["ic_lo"] <= f["ic_hi"] and fv["ic_hi"] >= f["ic_lo"]))
        b4_flip = []
        if d.get("sin_atipicos"):
            b4_flip.append(not d["sin_atipicos"]["mismo_signo"])
        for v in padre_vs:
            if v.endswith("-v8") or v.endswith("-v9") or v.endswith("-v5") and sid == "E3-A1":
                b4_flip.append(np.sign(ficha(res[v])["beta"]) != signo)
        rb = {"n_variantes": len(padre_vs), "frac_mismo_signo": (float(np.mean(misma)) if misma else None), "cambio_signo": bool(any(b4_flip)), "solape_ic": (bool(all(solape)) if solape else None)}
        pr = d["pretendencia"]
        pl = d["placebo_resultado"]
        pres = None if pl is None else min(pl["p_webb_ar"], pl["p_ar_exacto"])
        bal = d["balance"]
        ent = {"estimable": True, "p_holm": ph[sid], "F_eff": f["F_eff"], "ar_acotado": bool(f["ar_acotado"]), "pretend_p": pr["p_webb"], "roth_ok": pr["roth_ok"],
               "placebo_fecha_p": (d["placebo_fecha"] or {}).get("p_webb"), "placebo_fecha_mismo_signo_mitad": (d["placebo_fecha"] or {}).get("mismo_signo_mitad"),
               "placebo_resultado_p": pres, "robustez": rb, "rotemberg_ok": bool(d["rotemberg"]["mismo_signo"] and d["rotemberg"]["dentro_ic"]),
               "jrs_ok": (None if "error" in d.get("jrs", {"error": 1}) else bool(d["jrs"]["dentro_ic"])), "balance_ok": bool(bal["p_holm_min"] > 0.10),
               "tost": tost_ref(f, ref["delta"]), "topes": ([s["tope"]] if s.get("tope") else []), "tope_max": "IDENTIFICADO"}
        ent["debiles_extra"] = []
        if pres is None:
            ent["placebo_resultado_p"] = None
        # el p de Holm no significativo y con pruebas débiles: se rotula NO CONCLUYENTE (D-E359-17)
        c = K.clasificar(ent)
        if c["clase"] == "SUGESTIVO" and ph[sid] >= 0.10 and not ent["tost"]["equivalente"]:
            c = dict(c, clase="NO CONCLUYENTE (sin potencia)", razones=c["razones"] + ["sin significación (p de Holm ≥ 0,10) y sin equivalencia: se rotula NO CONCLUYENTE con las pruebas débiles listadas (D-E359-17)"])
        clas[sid] = dict(c, i6=etiqueta_i6(f, ref), tost=ent["tost"], robustez=rb, p_holm=ph[sid])
    for sid, mm in mde_tab.items():
        pass
    # ---- tabla
    filas = []
    for s in todas:
        sid = s["id"]
        base = {"id": sid, "rol": s["rol"], "padre": s.get("padre") or "", "nota": s["nota"], "ref": s["ref"], "ventana": str(s["cfg"]["ventana"]) if "ventana" in s["cfg"] else ""}
        if sid in ne:
            m = mde_tab.get(sid, {})
            base.update({"estado": "NO ESTIMABLE", "motivo": ne[sid], "mde80": m.get("mde80"), "n": m.get("n"), "G": m.get("G"), "F_eff": m.get("F_eff"), "clase": "NO ESTIMABLE"})
            filas.append(base)
            continue
        if sid not in res:
            continue
        f = ficha(res[sid])
        base.update({"estado": "estimada", "beta": f["beta"], "se": f["se"], "ic95_webb_ar_lo": f["ic_lo"], "ic95_webb_ar_hi": f["ic_hi"], "ic95_t_lo": f["ic95_t"][0], "ic95_t_hi": f["ic95_t"][1],
                     "ar_lo": f["ar_lo"], "ar_hi": f["ar_hi"], "ar_tipo": f["ar_tipo"], "F_eff": f["F_eff"], "p_webb_ar": f["p_webb_ar"], "p_ar": f["p_ar"], "p_final": f["p_final"],
                     "p_holm": ph.get(sid), "q_BY": qby.get(sid), "n": f["n"], "G": f["G"], "mco": f["mco"],
                     "mde80": mde_tab.get(sid, {}).get("mde80"), "clase": (clas.get(sid) or {}).get("clase", "")})
        filas.append(base)
    for nombre, d_ in (("E3-P-D4", pd4["valor tasado"]),):
        filas.append({"id": nombre, "rol": "coprincipal", "padre": "", "nota": "V9-D4 2003-2012, valor tasado (log por punto de población de 2003); publicado V9: −0,0029", "ref": "R1", "ventana": "2003-2012", "estado": "estimada",
                      "beta": d_["beta"], "se": d_["se"], "ic95_webb_ar_lo": d_["ic_webb_ar"]["lo"], "ic95_webb_ar_hi": d_["ic_webb_ar"]["hi"], "F_eff": d_["F_eff"], "p_webb_ar": d_["p_webb_ar"], "p_ar": d_["p_ar"],
                      "p_final": fam[nombre], "p_holm": ph[nombre], "n": d_["n"], "G": d_["G"], "clase": "no se clasifica"})
    filas.append({"id": "E3-P-Q3c1", "rol": "coprincipal", "padre": "", "nota": "V16 Q3-c1: ln valor tasado, TWFE, 2011-2022; publicado V16: 0,0119", "ref": "A1", "ventana": "2011-2022", "estado": "estimada",
                  "beta": pq3["beta"], "se": pq3["se"], "ic95_webb_ar_lo": pq3["ic_webb"][0], "ic95_webb_ar_hi": pq3["ic_webb"][1], "p_final": pq3["p_webb"], "p_webb_ar": pq3["p_webb"], "p_holm": ph["E3-P-Q3c1"],
                  "n": pq3["n"], "G": pq3["G"], "clase": "no se clasifica"})
    tabla = pd.DataFrame(filas)
    tabla.to_csv(SAL / "tabla.csv", index=False)
    pd.DataFrame([{"id": k, **{kk: vv for kk, vv in v.items() if kk not in ("curva", "inv_hhi_origen")}, "inv_hhi_origen": v["inv_hhi_origen"]["por_origen"],
                   "inv_hhi_origen_año": v["inv_hhi_origen"].get("por_origen_año")} for k, v in mde_tab.items()]).to_csv(SAL / "mde.csv", index=False)
    reg.flush()
    from e3_texto import escribir_texto
    escribir_texto(E3, dat, specs, mspecs, mde_tab, res, ne, pd4, pq3, diag, clas, ph, qby, var_por_padre, tabla, B, t0)
    return None


def EX_diag(E3, mun, cm, r, refv, B):
    return E3.EX.diag_municipal(mun, cm, r, refv, B)
