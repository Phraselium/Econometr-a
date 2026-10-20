"""V18 · errores estándar de Conley (1999) con núcleo de Bartlett en MCO (con efectos fijos de grupo opcionales) y geometría sintética.

Sin lectura de datos. La geometría es sintética, con la densidad de secciones censales de Barcelona (unos 10,6 secciones/km2 en la ciudad
una vez descontados los distritos sellados, 800 secciones; resto del área metropolitana con densidad decreciente) y 311 municipios de la
provincia. Coordenadas planas en km.
"""
from __future__ import annotations

import numpy as np

SEED = 20261010
ALCANCE_TERRITORIAL = "sin lectura de datos"
CIUDAD = (10.8, 7.0)        # km (75,6 km2: Barcelona sin los tres distritos sellados)
N_CIUDAD, N_BARRIOS = 800, 48
N_CORONA, N_MUN_CORONA = 3200, 310


def distancias(c1, c2=None):
    c2 = c1 if c2 is None else c2
    d2 = (c1 ** 2).sum(1)[:, None] + (c2 ** 2).sum(1)[None, :] - 2 * c1 @ c2.T
    d = np.sqrt(np.maximum(d2, 0.0))
    if c2 is c1:
        np.fill_diagonal(d, 0.0)
    return d


def nucleo_bartlett(coords, corte_km):
    """Matriz N x N de pesos de Bartlett max(0, 1 - d/corte), con diagonal 1 (cada observación una sola vez)."""
    return np.maximum(0.0, 1.0 - distancias(coords) / corte_km)


def wendland(d, soporte_km):
    """Correlación de Wendland (1 - r)^4_+ (4 r + 1), r = d/soporte: definida positiva en R^2, soporte compacto."""
    r = d / soporte_km
    return np.where(r < 1.0, (1.0 - r) ** 4 * (4.0 * r + 1.0), 0.0)


def geometria_secciones(rng):
    """800 secciones en 48 barrios de la ciudad y 3.200 secciones en 310 municipios de la corona; grupos = barrio o municipio.

    Devuelve (coords (N, 2), grupo (N,) ordenado y contiguo, es_ciudad (N,) bool).
    """
    ax, ay = CIUDAD
    gx, gy = np.meshgrid((np.arange(8) + 0.5) / 8 * ax - ax / 2, (np.arange(6) + 0.5) / 6 * ay - ay / 2)
    cb = np.column_stack([gx.ravel(), gy.ravel()]) + rng.uniform(-0.25, 0.25, (N_BARRIOS, 2))
    barrio = np.sort(np.arange(N_CIUDAD) % N_BARRIOS)
    p = cb[barrio] + 0.45 * rng.standard_normal((N_CIUDAD, 2))
    p[:, 0] = np.clip(p[:, 0], -ax / 2, ax / 2)
    p[:, 1] = np.clip(p[:, 1], -ay / 2, ay / 2)
    # corona: centros municipales con densidad radial decreciente (escala 18 km) en la ventana de la provincia
    ang = rng.uniform(0, 2 * np.pi, N_MUN_CORONA)
    rad = 8.0 + rng.gamma(2.0, 9.0, N_MUN_CORONA)
    cm = np.column_stack([rad * np.cos(ang) * 1.15, rad * np.sin(ang) * 0.9])
    cm[:, 0] = np.clip(cm[:, 0], -50, 50)
    cm[:, 1] = np.clip(cm[:, 1], -38, 38)
    pesos = rng.pareto(1.6, N_MUN_CORONA) + 1.0
    n_m = 1 + rng.multinomial(N_CORONA - N_MUN_CORONA, pesos / pesos.sum())
    mun = np.repeat(np.arange(N_MUN_CORONA), n_m)
    sg = 0.3 + 0.12 * np.sqrt(n_m)[mun]
    pc = cm[mun] + sg[:, None] * rng.standard_normal((N_CORONA, 2))
    coords = np.vstack([p, pc])
    grupo = np.concatenate([barrio, N_BARRIOS + mun])
    return coords, grupo, np.arange(len(coords)) < N_CIUDAD


def geometria_municipios(rng):
    """311 municipios: Barcelona en el origen y 310 en la corona con la misma ley radial (sin grupos)."""
    ang = rng.uniform(0, 2 * np.pi, N_MUN_CORONA)
    rad = 8.0 + rng.gamma(2.0, 9.0, N_MUN_CORONA)
    c = np.column_stack([rad * np.cos(ang) * 1.15, rad * np.sin(ang) * 0.9])
    c[:, 0] = np.clip(c[:, 0], -50, 50)
    c[:, 1] = np.clip(c[:, 1], -38, 38)
    return np.vstack([[0.0, 0.0], c])


def conley_ols(y, x, coords, corte_km, grupo=None):
    """MCO de y sobre x (+ constante o efectos fijos de grupo) con varianza de Conley (Bartlett). Devuelve (beta, se_conley, var_positiva)."""
    y = np.asarray(y, float)
    x = np.asarray(x, float)
    if grupo is None:
        xt, yt = x - x.mean(), y - y.mean()
    else:
        g = np.asarray(grupo)
        cnt = np.bincount(g).astype(float)
        mx = np.bincount(g, weights=x) / cnt
        my = np.bincount(g, weights=y) / cnt
        xt, yt = x - mx[g], y - my[g]
    sxx = float(xt @ xt)
    b = float(xt @ yt / sxx)
    s = xt * (yt - b * xt)
    K = nucleo_bartlett(coords, corte_km)
    v = float(s @ (K @ s))
    return b, float(np.sqrt(max(v, 0.0)) / sxx), v > 0
