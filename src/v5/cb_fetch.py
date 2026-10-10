"""CB descargas (con red, fuera de make): python3 src/v5/cb_fetch.py
Destino: data/raw/v5/cb_*. Fuentes:
  CGPJ  Efecto de la crisis en los organos judiciales (xlsx lanzamientos por TSJ y por PJ; verbales posesorios por ocupacion)
  Interior  Portal Estadistico de Criminalidad, series anuales Allanamiento/Usurpacion (px 11001 hechos conocidos CCAA)
  INE Tempus 9997 (ECV: hogares por regimen de tenencia y CCAA)
  AEAT Sede: Estadistica de los declarantes del IRPF (partidas de bienes inmobiliarios, 2019-2024) y
       Estadistica de viviendas declaradas en el IRPF 2024 (viviendas arrendadas por CCAA, clasificacion por uso)
Los fallos se anotan en docs/v5/fuentes_fallidas.md (seccion CB).
"""
import re
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path

DEST = Path(__file__).resolve().parents[2] / "data" / "raw" / "v5"
CGPJ = "https://www.poderjudicial.es/stfls/ESTADISTICA/FICHEROS/Crisis/"
SEDE = "https://sede.agenciatributaria.gob.es"
IRPF = SEDE + "/AEAT/Contenidos_Comunes/La_Agencia_Tributaria/Estadisticas/Publicaciones/sites/irpf/%s/"
VIV = SEDE + "/AEAT/Contenidos_Comunes/La_Agencia_Tributaria/Estadisticas/Publicaciones/sites/irpfvivienda/2024/"


def get(url):
    with urllib.request.urlopen(url, timeout=120) as r:
        return r.read()


def save(name, url):
    try:
        b = get(url)
        (DEST / name).write_bytes(b)
        print("ok", name, len(b))
        return b
    except Exception as e:  # noqa: BLE001
        print("FALLO", name, url, e)
        return None


def anchors(html):
    return [(m.group(1), re.sub(r"\s+", " ", re.sub(r"<[^>]*>", "", m.group(2))).strip())
            for m in re.finditer(r'<a[^>]*href="([^"#]*)"[^>]*>(.*?)</a>', html, re.S)]


def find_page(base, home, texto, prof=3):
    """BFS por home_parcial/jrubik hasta un ancla cuyo texto coincide."""
    vistos, cola = set(), [(home, 0)]
    while cola:
        p, d = cola.pop(0)
        if p in vistos or d > prof:
            continue
        vistos.add(p)
        try:
            h = get(base + p).decode("utf8", "ignore")
        except Exception:  # noqa: BLE001
            continue
        for href, t in anchors(h):
            if re.search(texto, t) and "jrubik" in href:
                return href
            if "home_parcial" in href and href not in vistos:
                cola.append((href, d + 1))
    return None


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    save("cb_cgpj_lanzamientos_pj_2013_2025.xlsx", CGPJ + urllib.parse.quote("Lanzamientos por PJs_2013_ 2025.xlsx"))
    save("cb_cgpj_series_tsj_1T2026.xlsx", CGPJ + urllib.parse.quote("Series - Efecto de la crisis en los organos judiciales por TSJ 1T-2026_revisado.xlsx"))
    px = "https://estadisticasdecriminalidad.ses.mir.es/sec/jaxiPx/files/_px/es/px/Datos11/l0/%s.px"
    for f in ("11001", "11002"):
        save(f"cb_interior_{f}.px", px % f)
    save("cb_ine_t9997_ecv_tenencia_ccaa.json", "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/9997?nult=12")
    for y in range(2019, 2025):
        base = IRPF % y
        href = find_page(base, "home.html", r"^Bienes inmobiliarios$")
        if href:
            save(f"cb_aeat_irpf_{y}_bienes_inmobiliarios.html", base + href)
        else:
            print("FALLO IRPF", y, "sin pagina de bienes inmobiliarios")
    for nombre, h in (("arrendamiento_ccaa_declarante", "jrubikffbbfc140eeb3061470b400b2fe7de51c1523ce1.html"),
                      ("clasificacion_uso", "jrubik363e5de8f59ea768b6235c20cc2f1c98f2d62663.html"),
                      ("cuenta_resultados_ccaa", "jrubikf6dab530d3943a3876eb332fcaebe8535f33f367.html")):
        save(f"cb_aeat_irpfviv_2024_{nombre}.html", VIV + h)
    try:
        subprocess.run(["sha256sum"] + sorted(str(p) for p in DEST.glob("cb_*")), check=False)
    except OSError:
        pass


if __name__ == "__main__":
    main()
