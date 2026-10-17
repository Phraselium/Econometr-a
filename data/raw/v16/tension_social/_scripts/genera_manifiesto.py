"""Genera _manifest.csv de la familia tension_social. Uso: python3 -I genera_manifiesto.py <raiz_repo>"""
import csv, glob, gzip, hashlib, os, sys
R = sys.argv[1]
F = "data/raw/v16/tension_social/"
FECHA = "2026-10-17"
def sha(p):
    h = hashlib.sha256()
    with open(os.path.join(R, p), "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()
def nl(p):
    with gzip.open(os.path.join(R, p), "rb") as f:
        return sum(1 for _ in f) - 1
rows = []
CG_LIC = ("CGPJ: Aviso Legal (https://www.poderjudicial.es/cgpj/es/Poder-Judicial/Aviso-Legal/) sin texto disponible el 2026-10-17 "
          "('No hay información disponible'); pie 'Copyright © Consejo General del Poder Judicial'; sin licencia de reutilización declarada")
base = "https://www.poderjudicial.es/stfls/ESTADISTICA/FICHEROS/Crisis/"
cg = [
 ("cgpj_lanzamientos_partidos_judiciales_2013_2025.xlsx", "Lanzamientos%20por%20PJs_2013_%202025.xlsx", "Lanzamientos practicados 2013-2025 (anual)", "2013-2025 anual", "partido judicial (nombre; sin código INE)", "hoja única; total y por causa (ej. hipotecaria, LAU, otros). Idéntico (sha256) a data/raw/v5/cb_cgpj_lanzamientos_pj_2013_2025.xlsx"),
 ("cgpj_series_tsj_2T2026.xlsx", "Series%20-%20Efecto%20de%20la%20crisis%20en%20los%20organos%20judiciales%20por%20TSJ%202T-2026.xlsx", "Series por TSJ 2T-2026", "trimestral 2013T1-2026T2", "TSJ/CCAA", "amplía v5 (1T-2026): añade 2T-2026; lanzamientos por causa, ejecuciones hipotecarias, concursos, monitorios"),
 ("cgpj_series_provincias_2T2026.xlsx", "Series%20-%20Efecto%20de%20la%20crisis%20en%20los%20organos%20judiciales%20por%20provincias%202T-2026.xlsx", "Series por provincias 2T-2026", "trimestral 2013T1-2026T2", "provincia", "hojas 'Lanzamientos pract. Total/E.hipotecaria/L.A.U./Otros prov', 'Ej.Hipot por provincias', 'Ver. pos.ocupas'; NUEVO respecto a v5 (v5 solo tenía TSJ)"),
 ("cgpj_datos_crisis_2T2026.xlsx", "Datos%20sobre%20el%20efecto%20de%20la%20crisis%20en%20los%20organos%20judiciales%202T-2026-%20con%20Microempresas.xlsx", "Datos efecto crisis 2T-2026", "2026T2 (trimestre)", "partido judicial/órgano, provincia, TSJ (según hoja)", "fichero trimestral; no inspeccionado en detalle"),
 ("cgpj_datos_crisis_anual2025.xlsx", "Datos%20sobre%20el%20efecto%20de%20la%20crisis%20en%20los%20organos%20judiciales%20-%20Anual%202025.xlsx", "Datos efecto crisis Anual 2025", "2025 (anual)", "partido judicial/órgano, provincia, TSJ (según hoja)", "fichero anual; no inspeccionado en detalle"),
]
for fn, u, ed, per, niv, nota in cg:
    p = F + "_terceros/" + fn
    rows.append(["cgpj_efecto_crisis", p, base + u, FECHA, ed, per, niv, "", sha(p), CG_LIC, "dudoso", nota])
p = F + "_terceros/mjusticia_nomenclator_partidos_judiciales.pdf"
rows.append(["mjusticia_nomenclator_pj", p,
  "https://www.mjusticia.gob.es/es/JusticiaEspana/OrganizacionJusticia/Documents/Nomencl%C3%A1tor%20de%20Partidos%20Judiciales.pdf",
  FECHA, "Nomenclátor de Partidos Judiciales, fecha de pie 30/12/2025", "vigente a 30/12/2025", "partido judicial -> municipio (código INE 5 dígitos)", "",
  sha(p),
  "Min. Justicia: aviso legal general limita a uso privado (https://www.mjusticia.gob.es/es/aviso-legal); términos de reutilización con cita en datos abiertos (https://sede.mjusticia.gob.es/informacion-ayuda/datos-abiertos-ministerio); el PDF no consta publicado como conjunto de datos abiertos",
  "dudoso", "PDF de 204 págs; el partido judicial se numera dentro de cada provincia (sin código oficial único); 8132 municipios, 431 partidos"])
p = F + "_terceros/derivado_pj_municipio.csv"
rows.append(["mjusticia_nomenclator_pj (derivado)", p, "derivado del PDF anterior con _scripts/parsea_nomenclator_pj.py", FECHA, "30/12/2025", "vigente 30/12/2025",
  "partido judicial -> municipio", sum(1 for _ in open(os.path.join(R, p), encoding="utf-8")) - 1, sha(p), "hereda la del PDF de origen", "dudoso",
  "DERIVADO (no original). Cruce con el nombre de partido en ficheros CGPJ pendiente: CGPJ usa nombres, el PDF numeración por provincia (orden = orden del PDF)"])
INE_LIC = "INE: reutilización con cita de la fuente (Ley 37/2007; https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177012#_tabs-1254736194496 / aviso legal https://www.ine.es/ss/Satellite?L=es_ES&c=Page&cid=1254735849170&p=1254735849170&pagename=MenuFooter/Texto)"
orig = {}
for ln in open(os.path.join(R, F, "_scripts/sha256_csv_originales_sin_comprimir.txt")):
    h, f = ln.split(); orig[f] = h
for p in sorted(glob.glob(os.path.join(R, F, "emcr/*.gz"))):
    rel = os.path.relpath(p, R); t = os.path.basename(p).split("_")[-1].split(".")[0]
    base_rel = rel[len(F):-3]
    rows.append(["ine_emcr", rel, f"https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/{t}.csv?nocab=1", FECHA,
      "EMCR (Estadística de Migraciones y Cambios de Residencia, op. 455), tabla " + t, "2021-2024", "municipio (código INE en etiqueta) y provincia", nl(rel), sha(rel), INE_LIC, "sí",
      f"gzip -9 -n del CSV original (ISO-8859-15, ';'); sha256 del original sin comprimir {orig[base_rel]}; serie nueva EMCR 2021+ (ruptura con EVR 1988-2021 de v11)"])
p = F + "padron_cifras_oficiales/ine_cifras_oficiales_padron_municipio_29005.csv.gz"
rows.append(["ine_cifras_oficiales_padron", p, "https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/29005.csv?nocab=1", FECHA,
  "Cifras oficiales del padrón por municipio (op. 22), tabla 29005, cifras a 1 enero 2025", "1996-2025 (1 enero)", "municipio", nl(p), sha(p), INE_LIC, "sí",
  f"solo población total por sexo (sin nacionalidad); gzip del CSV original; sha256 original {orig[p[len(F):-3]]}. Cubre 2023-2025, que faltan en data/raw/v9/ine_padron_nacionalidad (2003-2022)"])
for p in sorted(glob.glob(os.path.join(R, F, "padron_seccion_2022_nacionalidad_continentes/*.px"))):
    rel = os.path.relpath(p, R); fn = os.path.basename(p)
    rows.append(["ine_padron_seccion_censal", rel, f"https://www.ine.es/jaxi/files/_px/es/px/t20/e245/p07/a2022/l0/{fn}", FECHA,
      "Padrón 1 enero 2022 (PC-Axis, creación 2025-09-30)", "2022 (1 enero)", "sección censal (provincia " + fn[:2] + ")", "", sha(rel), INE_LIC, "sí",
      "sexo x sección x nacionalidad (continentes); original PC-Axis sin transformar"])
with open(os.path.join(R, F, "_manifest.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["fuente", "fichero", "url", "fecha_descarga", "edicion", "periodo", "nivel_territorial", "n_filas", "sha256", "licencia", "redistribuible", "notas"])
    w.writerows(rows)
print(len(rows), "filas")
