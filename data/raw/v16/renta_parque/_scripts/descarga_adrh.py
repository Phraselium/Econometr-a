"""INE · Atlas de Distribución de Renta de los Hogares (ADRH) · API JSON (servicios.ine.es/wstempus).

1. Lista de tablas: TABLAS_OPERACION/ADRH (540 tablas: renta media y mediana, fuentes de ingresos,
   Gini y P80/P20, umbrales de pobreza por sexo, edad y nacionalidad, indicadores demográficos).
2. Datos: DATOS_TABLA/<Id>?nult=20 (toda la serie disponible, 2015-2023 en la edición vigente).
Salida: _grandes/adrh/<Id>.json.gz (cada tabla pesa ~0,4 MB comprimida; carpeta ignorada en git).
Caché: no rebaja lo que ya existe salvo FORCE=1. Ejecutar: python3 -I descarga_adrh.py
"""
import concurrent.futures as cf
import datetime as dt
import gzip
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import adq_utils as au  # noqa: E402

BASE = "https://servicios.ine.es/wstempus/js/ES"
DEST = os.path.join(au.FAMILIA_DIR, "_grandes", "adrh")
LISTA = os.path.join(au.FAMILIA_DIR, "_grandes", "adrh", "tablas_adrh.json.gz")
FUENTE = "INE ADRH (API wstempus)"
LICENCIA = ("INE: reutilización con cita (Ley 37/2007); aviso legal https://www.ine.es/aviso_legal"
            " (ver también https://www.ine.es/normativa/normativa.htm)")


def fecha_mod(ms):
    try:
        return dt.datetime.fromtimestamp(int(ms) / 1000, dt.timezone.utc).strftime("%Y-%m-%d")
    except Exception:  # noqa: BLE001
        return "desconocida"


def procesa(tabla, hoy):
    tid = tabla["Id"]
    url = f"{BASE}/DATOS_TABLA/{tid}?nult=20"
    destino = os.path.join(DEST, f"{tid}.json.gz")
    estado, nbytes = au.descargar(url, destino)
    with gzip.open(destino, "rb") as f:
        datos = json.loads(f.read().decode("utf-8"))
    anios = [x["Anyo"] for s in datos for x in s.get("Data", [])]
    secretos = sum(1 for s in datos for x in s.get("Data", []) if x.get("Secreto"))
    ruta_rel = os.path.relpath(destino, au.RAIZ)
    return {
        "fuente": FUENTE,
        "fichero": ruta_rel,
        "url": url,
        "fecha_descarga": hoy,
        "edicion": (f"ADRH tabla {tid} ({tabla.get('Codigo')}), '{tabla.get('Nombre')}',"
                    f" última modificación {fecha_mod(tabla.get('Ultima_Modificacion'))}"),
        "periodo": f"{min(anios)}-{max(anios)}" if anios else "vacío",
        "nivel_territorial": "municipio/distrito/sección (series de la tabla; ver notas)",
        "n_filas": len(datos),
        "sha256": au.sha256(destino),
        "licencia": LICENCIA,
        "redistribuible": "sí",
        "notas": (f"Series (no filas de datos): {len(datos)}; valores secretos: {secretos};"
                  f" fichero en _grandes (ignorado en git); descarga {estado}"),
    }


def main():
    os.makedirs(DEST, exist_ok=True)
    hoy = dt.date.today().isoformat()
    if not os.path.exists(LISTA) or au.FORCE:
        au.descargar(f"{BASE}/TABLAS_OPERACION/ADRH", LISTA)
    with gzip.open(LISTA, "rb") as f:
        tablas = json.loads(f.read().decode("utf-8"))
    filas, errores = [], []
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        futuros = {ex.submit(procesa, t, hoy): t["Id"] for t in tablas}
        for fut in cf.as_completed(futuros):
            try:
                filas.append(fut.result())
            except Exception as e:  # noqa: BLE001
                errores.append((futuros[fut], str(e)))
    au.upsert(filas)
    print(f"tablas={len(tablas)} ok={len(filas)} errores={len(errores)}")
    for tid, e in errores[:20]:
        print("ERROR", tid, e[:200])


if __name__ == "__main__":
    main()
