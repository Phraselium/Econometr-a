"""V11-DATOS (histórico, A3): AEAT, «Estadística de los declarantes del IRPF por municipios» (municipios de más de 1.000
hab.), ejercicios 2013-2024: https://sede.agenciatributaria.gob.es/AEAT/Contenidos_Comunes/La_Agencia_Tributaria/
Estadisticas/Publicaciones/sites/irpfmunicipios/<año>/home.html.
Desagregación REAL: un informe HTML («jrubik») por municipio y ejercicio, con 61 filas (número de declaraciones y de
titulares, renta bruta y disponible y sus componentes: trabajo, capital mobiliario, «rentas de bienes inmuebles no
afectos a actividades económicas» = capital inmobiliario, actividades económicas, ganancias patrimoniales…; medias por
declarante con cada renta). No hay ficheros descargables; no publica el NÚMERO de declarantes con rentas
inmobiliarias (solo importe y media: n ≈ importe / media, cálculo que se deja para el análisis). Por código postal
(irpfCodPostal) solo en grandes municipios: no se descarga en esta tarea (documentado).
Se recorre home → «Datos municipales por ámbito territorial» → comunidad → provincia → municipio (el código INE va en
el texto del enlace «Nombre-PPMMM»). Ámbito por coste (≈ 1 petición por municipio y año): provincias 03, 12 y 46.
Caché por año y municipio en tmp/ (no versionada). Licencia AEAT: reutilización con cita.
"""
from __future__ import annotations

import html
import io
import re
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import CABECERAS, GZ_PANDAS, RAW11, registrar, verificar_manifiesto  # noqa: E402

FUENTE = "aeat_irpf_municipios"
DIR = RAW11 / FUENTE
B = "https://sede.agenciatributaria.gob.es/AEAT/Contenidos_Comunes/La_Agencia_Tributaria/Estadisticas/Publicaciones/sites/irpfmunicipios/{a}/"
LIC = "Agencia Tributaria: reutilización con cita (Ley 37/2007)"
ANIOS = range(2013, 2025)
PROVINCIAS = {"03": "Alicante", "12": "Castell", "46": "Valencia/Val"}
S = requests.Session()


def pagina(url: str) -> str:
    for _ in range(3):
        try:
            r = S.get(url, headers=CABECERAS, timeout=120)
            if r.status_code == 200:
                return r.content.decode("utf-8", "replace")
        except Exception:  # noqa: BLE001
            pass
    return ""


def enlaces(t: str) -> list[tuple[str, str]]:
    return [(a, html.unescape(re.sub(r"<[^>]+>|\s+", " ", b)).strip())
            for a, b in re.findall(r'href="((?:jrubik|home_parcial)[^"]+)"[^>]*>(.*?)</a>', t, re.S)]


def tabla(t: str) -> pd.DataFrame | None:
    try:
        T = max(pd.read_html(io.StringIO(t), thousands=".", decimal=",", flavor="lxml"), key=len)
    except (ValueError, ImportError):
        return None
    return pd.DataFrame({"variable": T.iloc[:, 0].astype(str).str.strip(), "valor": pd.to_numeric(T.iloc[:, 1], errors="coerce")})


def main(verificar: bool = False) -> int:
    DIR.mkdir(parents=True, exist_ok=True)
    if verificar:
        return verificar_manifiesto(FUENTE)
    cache = DIR / "tmp"
    cache.mkdir(parents=True, exist_ok=True)
    partes, sin = [], []
    for a in ANIOS:
        base = B.format(a=a)
        home = pagina(base + "home.html")
        if not home:
            sin.append(f"{a}: sin home")
            continue
        # home → página con «Datos municipales por ámbito territorial» (puede estar en un home_parcial)
        cand = [u for u, x in enlaces(home)]
        amb = None
        for u in cand:
            t = pagina(base + u)
            amb = next((v for v, x in enlaces(t) if x.startswith("Datos municipales por ámbito")), None)
            if amb:
                break
        if not amb:
            sin.append(f"{a}: sin página de ámbito")
            continue
        t_amb = pagina(base + amb)
        cv = next((v for v, x in enlaces(t_amb) if "Valenciana" in x), None)   # «Comunitat» o «Comunidad» según el año
        t_cv = pagina(base + cv) if cv else ""
        for pp, nom in PROVINCIAS.items():
            pv = next((v for v, x in enlaces(t_cv) if x.startswith(nom)), None)
            t_pv = pagina(base + pv) if pv else ""
            muns = [(v, x) for v, x in enlaces(t_pv) if re.search(r"-\d{5}$", x)]
            if not muns:
                sin.append(f"{a}-{pp}: sin municipios")
            for v, x in muns:
                cod = x[-5:]
                c = cache / f"{a}_{cod}.csv"
                if c.exists():
                    d = pd.read_csv(c)
                else:
                    tm = pagina(base + v)
                    if not tm:
                        sin.append(f"{a}-{cod}")
                        continue
                    d = tabla(tm)
                    if d is None:
                        sin.append(f"{a}-{cod}: sin tabla")
                        continue
                    d.to_csv(c, index=False)
                d.insert(0, "cod_municipio", cod)
                d.insert(0, "ejercicio", a)
                partes.append(d)
        print(a, len(partes), flush=True)
    D = pd.concat(partes, ignore_index=True)
    D["cod_municipio"] = D.cod_municipio.astype(str).str.zfill(5)
    r = DIR / "irpf_municipios_cv.csv.gz"
    D.to_csv(r, index=False, compression=GZ_PANDAS)
    registrar(FUENTE, r, B.format(a="<año>") + "home.html", edicion="AEAT, estadística de declarantes del IRPF por municipios",
              periodo=f"{D.ejercicio.min()}-{D.ejercicio.max()}", nivel_territorial="municipio > 1.000 hab. (Comunitat Valenciana)",
              licencia=LIC, redistribuible=True, notas=f"61 conceptos por municipio y ejercicio (formato largo); incidencias: {sin[:20]}")
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
