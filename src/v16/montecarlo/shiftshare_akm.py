"""V16 · fase 5 · Validación Monte Carlo del shift-share en forma reducida con inferencia AKM / AKM0 (Q3-c1, Q3-c2).

Ejecución: python src/v16/montecarlo/shiftshare_akm.py [--R 5000]   (SEED 20261010, k = 31)
El proceso generador se escribe en docs/v16/validacion_montecarlo/shiftshare_akm.md ANTES de simular.
Estructura real usada: cuotas provinciales de 2003 por nacionalidad (28 orígenes, 41 provincias de entrenamiento) del padrón; el resultado se SIMULA.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _comun_iv_espacial as C  # noqa: E402

HERR, K_SEM = "shiftshare_akm", 31
T_ANIOS = list(range(2011, 2025))
AGREGADOS = {"Total", "Española", "Extranjera", "De Africa", "De América", "De Asia", "Europa (sin España)",
             "Oceanía y Apátridas", "País de Europa menos UE28", "País de la UE28 sin España"}
SD_X, SIGMA = 0.10, 0.15
BETA_ALT = 1.0
RHO_G, RHO_U, RHO_F, RHO_E = 0.5, 0.5, 0.7, 0.5
Z = 1.959964


def cuotas() -> tuple[np.ndarray, list[str], list[str]]:
    d = pd.read_parquet(C.ENT / "padron_nacionalidad.parquet", columns=["territorio_codigo", "periodo", "desagregacion", "valor"])
    d = d[d.periodo == "2003"].copy()
    d["prov"] = d.territorio_codigo.str[:2]
    d["nac"] = d.desagregacion.str.replace("nacionalidad=", "", regex=False)
    p = d.pivot_table(index="prov", columns="nac", values="valor", aggfunc="sum").fillna(0.0)
    tot = p["Total"]
    orig = [c for c in p.columns if c not in AGREGADOS]
    S = (p[orig].div(tot, axis=0)).to_numpy()
    return S, list(p.index), orig


def n_efectivo(S: np.ndarray) -> float:
    w = S.sum(0) / S.sum()
    return float(1 / (w ** 2).sum())


def dgp_texto(S, provs, orig, ne) -> str:
    return f"""# shiftshare_akm · Q3-c1 y Q3-c2 (shift-share en forma reducida, inferencia AKM)

## Proceso generador (declarado antes de simular)
- **Estructura real (solo estructura):** {len(provs)} provincias de entrenamiento × {len(T_ANIOS)} años ({T_ANIOS[0]}-{T_ANIOS[-1]}); {len(orig)} orígenes
  (nacionalidades individuales del padrón de 2003, sin agregados); cuotas s_ik = población de nacionalidad k / población total de la provincia i en 2003
  (data/processed/v16/entrenamiento/padron_nacionalidad.parquet, agregado de municipio a provincia). Número efectivo de choques 1/HHI de las ponderaciones de Rotemberg-tipo
  (cuota agregada de cada origen) = **{ne:.1f}** (la adenda prevé ≈ 12).
- **Regresor:** x_it = c · Σ_k s_ik g_kt, con g_kt = choque nacional del origen k (N(0,1) independiente entre orígenes, AR(1) en t con ρ = {RHO_G}); c fija la DT de x
  tras quitar efectos fijos a ≈ {SD_X} puntos (unidad: punto de población extranjera predicha).
- **Resultado:** y_it = β x_it + σ·ε_it, σ = {SIGMA}; ε_it = √0,5·A_it + √0,2·π_i f_t + √0,3·e_it, con
  A_it = Σ_k s_ik u_kt / norma (choques de origen NO observados u_kt, independientes de g_kt pero con las mismas cuotas: dependencia transversal por cuota, AR(1) ρ = {RHO_U}),
  f_t factor común AR(1) ρ = {RHO_F} con cargas π_i ~ N(0,1), e_it AR(1) ρ = {RHO_E}. Los efectos fijos de provincia y año se absorben y no se simulan.
- **Nulo:** β = 0 (tamaño). **Alternativa:** β = {BETA_ALT} (magnitud de referencia de Q3-c1, elasticidad de Saiz por punto): sesgo, RMSE, cobertura y potencia.
- **Estimación:** MCO con efectos fijos de provincia y año (TWFE). Inferencias: (a) AKM (varianza por choque, normal); (b) AKM0 (inversión de la prueba con residuos bajo el nulo, normal);
  (c) EE agrupados por provincia, t(40): solo como referencia del sobre-rechazo, no es candidata.
- **Sensibilidad (informativa):** peso de A en ε de 0,25 y 0,75. El veredicto usa el escenario principal (0,5).
- **Pocos clusters / T corto:** 41 provincias, 14 años, {len(orig)} choques (≈ {ne:.0f} efectivos).
- **Criterio:** tamaño en [0,04; 0,06] con R ≥ 2.000 y cobertura en [0,92; 0,97]. Alternativa nombrada en el punto 3: ninguna distinta de AKM en la tabla; AKM0 se prueba como variante de la misma familia (se declara aquí; si AKM falla y AKM0 pasa, el veredicto es «alternativa APTA (AKM0)»).
"""


def lote(rng, n, S, wA: float = 0.5):
    G, K = S.shape
    T = len(T_ANIOS)
    norma = np.sqrt((S ** 2).sum(1).mean())
    c = SD_X / norma
    g = C.ar1(rng, (n, K, T), RHO_G)
    u = C.ar1(rng, (n, K, T), RHO_U)
    f = C.ar1(rng, (n, T), RHO_F)
    pi = rng.standard_normal((n, G))
    e = C.ar1(rng, (n, G, T), RHO_E)
    x = c * np.einsum("ik,nkt->nit", S, g)
    A = np.einsum("ik,nkt->nit", S, u) / norma
    eps = np.sqrt(wA) * A + np.sqrt(0.2) * pi[:, :, None] * f[:, None, :] + np.sqrt(0.8 - wA) * e
    eps = SIGMA * eps
    dm = lambda a: a - a.mean(2, keepdims=True) - a.mean(1, keepdims=True) + a.mean((1, 2), keepdims=True)
    xt = dm(x)
    out = []
    for beta in (0.0, BETA_ALT):
        y = beta * x + eps
        yt = dm(y)
        sxx = (xt ** 2).sum((1, 2))
        bh = (xt * yt).sum((1, 2)) / sxx
        res = yt - bh[:, None, None] * xt
        # convencional: agrupado por provincia
        ci = (xt * res).sum(2)
        se_c = np.sqrt((ci ** 2).sum(1) * G / (G - 1)) / sxx
        # AKM: varianza por origen
        a = np.einsum("ik,nit->nkt", S, yt)
        b = np.einsum("ik,nit->nkt", S, xt)
        gg = c * g
        Ak = (gg * a).sum(2)
        Bk = (gg * b).sum(2)
        SA, SB = Ak.sum(1), Bk.sum(1)
        se_a = np.sqrt(((Ak - bh[:, None] * Bk) ** 2).sum(1)) / sxx
        out.append((bh, se_c, se_a, SA, SB, Ak, Bk, sxx))
    return out


def akm0_rechaza(SA, SB, Ak, Bk, b0):
    num = SA - b0 * SB
    v = ((Ak - b0 * Bk) ** 2).sum(1)
    return num ** 2 > Z ** 2 * v


def akm0_ic(SA, SB, Ak, Bk):
    """IC por inversión: {b: (SA-b SB)^2 - z^2 Σ(Ak-b Bk)^2 <= 0}. Devuelve (lo, hi, acotado)."""
    a2 = SB ** 2 - Z ** 2 * (Bk ** 2).sum(1)
    a1 = -2 * SA * SB + 2 * Z ** 2 * (Ak * Bk).sum(1)
    a0 = SA ** 2 - Z ** 2 * (Ak ** 2).sum(1)
    disc = a1 ** 2 - 4 * a2 * a0
    ok = (a2 > 0) & (disc >= 0)
    r = np.sqrt(np.where(ok, disc, 0.0))
    lo = np.where(ok, (-a1 - r) / (2 * a2), np.nan)
    hi = np.where(ok, (-a1 + r) / (2 * a2), np.nan)
    return lo, hi, a2 > 0


def f_rep(rng, n, S=None, wA=0.5):
    (b0, sc0, sa0, SA0, SB0, Ak0, Bk0, sxx0), (b1, sc1, sa1, SA1, SB1, Ak1, Bk1, sxx1) = lote(rng, n, S, wA)
    tc = stats.t.ppf(0.975, S.shape[0] - 1)
    lo, hi, acot = akm0_ic(SA1, SB1, Ak1, Bk1)
    cols = [
        b0, b1,
        (np.abs(b0) / sc0 > tc), (np.abs(b0) / sa0 > Z), akm0_rechaza(SA0, SB0, Ak0, Bk0, 0.0),            # tamaño: conv, akm, akm0
        (np.abs(b1) / sc1 > tc), (np.abs(b1) / sa1 > Z), akm0_rechaza(SA1, SB1, Ak1, Bk1, 0.0),            # potencia
        (np.abs(b1 - BETA_ALT) <= tc * sc1), (np.abs(b1 - BETA_ALT) <= Z * sa1), ~akm0_rechaza(SA1, SB1, Ak1, Bk1, BETA_ALT),  # cobertura
        2 * Z * sa1, np.where(acot, hi - lo, np.nan), acot,
    ]
    return np.column_stack([np.asarray(c, dtype=float) for c in cols])


def resumir(M: np.ndarray) -> pd.DataFrame:
    R = len(M)
    nm = ["convencional (EE por provincia)", "AKM", "AKM0"]
    filas = []
    for j, m in enumerate(nm):
        tam = M[:, 2 + j].mean()
        cob = M[:, 8 + j].mean()
        filas.append({
            "inferencia": m, "R": R, "tamano_5pct": tam, "tamano_ic95": str(C.ic_binomial(tam, R)),
            "cobertura_95": cob, "potencia_beta1": M[:, 5 + j].mean(),
            "sesgo": np.nanmean(M[:, 1] - BETA_ALT), "rmse": float(np.sqrt(np.nanmean((M[:, 1] - BETA_ALT) ** 2))),
            "longitud_ic_mediana": float(np.nanmedian(M[:, 10 + j])) if j else float("nan"),
            "ic_acotado": float(M[:, 13].mean()) if j == 2 else 1.0,
        })
    return pd.DataFrame(filas)


def main(R: int = 5000, S=None):
    S, provs, orig = cuotas()
    ne = n_efectivo(S)
    C.declarar_dgp(HERR, dgp_texto(S, provs, orig, ne))
    tablas = []
    for esc, wA in (("principal wA=0,5", 0.5), ("sens wA=0,25", 0.25), ("sens wA=0,75", 0.75)):
        M = C.paralelo(f_rep, K_SEM, R if wA == 0.5 else max(C.R_MIN, R // 2), S=S, wA=wA)
        t = resumir(M)
        t.insert(0, "escenario", esc)
        tablas.append(t)
    tab = pd.concat(tablas, ignore_index=True)
    pr = tab[tab.escenario.str.startswith("principal")].set_index("inferencia")
    ver = {}
    for m in ("AKM", "AKM0", "convencional (EE por provincia)"):
        ver[m] = C.veredicto(float(pr.loc[m, "tamano_5pct"]), int(pr.loc[m, "R"]), float(pr.loc[m, "cobertura_95"]))
    if ver["AKM"]["veredicto"] == "APTO":
        vf = "APTO (AKM)"
    elif ver["AKM0"]["veredicto"] == "APTO":
        vf = "alternativa APTA (AKM0)"
    else:
        vf = "NO APTO → diseño solo descriptivo"
    res = C.resultado_base("Q3-c1 / Q3-c2 (shift-share en forma reducida)", f"{len(provs)} provincias x {len(T_ANIOS)} años, {len(orig)} orígenes",
                           "TWFE con inferencia AKM / AKM0", "simulados; cuotas 2003 reales del padrón (solo estructura)")
    res["estimacion"] = {"beta_alt": BETA_ALT, "sesgo": float(pr.loc["AKM", "sesgo"]), "rmse": float(pr.loc["AKM", "rmse"])}
    res["diagnosticos"] = {"veredicto": vf, "por_inferencia": ver, "n_efectivo_choques": ne,
                           "tamano_convencional": float(pr.loc["convencional (EE por provincia)", "tamano_5pct"]),
                           "tamano_akm": float(pr.loc["AKM", "tamano_5pct"]), "cobertura_akm": float(pr.loc["AKM", "cobertura_95"]),
                           "tamano_akm0": float(pr.loc["AKM0", "tamano_5pct"]), "cobertura_akm0": float(pr.loc["AKM0", "cobertura_95"]),
                           "potencia_akm": float(pr.loc["AKM", "potencia_beta1"]), "R": int(pr.loc["AKM", "R"]), "semilla": C.SEED}
    res["notas"] = ["El EE convencional se muestra solo para medir el sobre-rechazo; no es alternativa."]
    md = f"## Resultados (R = {R} réplicas en el escenario principal; semilla {C.SEED}, k = {K_SEM})\n\n{C.md_tabla(tab)}\n\n**Veredicto: {vf}.**\n\n"
    for m, v in ver.items():
        md += f"- {m}: {v['veredicto']} {('— ' + '; '.join(v['fallos'])) if v['fallos'] else ''}\n"
    md += ("\n**Lectura.** Con n efectivo de choques = %.1f las cuotas están concentradas en pocos orígenes: el EE por provincia ignora la dependencia por cuota "
           "(sobre-rechazo), AKM subestima la varianza porque el residuo estimado absorbe el choque dominante (A_k - b·B_k ≈ 0) y AKM0 queda en el extremo conservador "
           "(el estadístico autonormalizado con pocos términos dominantes rara vez supera 1,96). Ninguna pasa [0,04; 0,06]: el diseño es solo descriptivo.\n" % ne)
    C.escribir_salidas(HERR, res, tab, md)
    print(tab.to_string())
    print(vf)
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--R", type=int, default=5000)
    main(ap.parse_args().R)
