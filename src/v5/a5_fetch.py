"""A5 fetch (con red; fuera de make). Descarga documentos oficiales a data/raw/v5/programas/ y escribe el inventario.

Idempotente: no vuelve a descargar un fichero ya presente (salvo FORCE=1).
"""
import csv
import datetime
import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / "data/raw/v5/programas"
INV = ROOT / "docs/v5/programas/inventario.csv"
BOCG = "https://www.congreso.es/public_oficiales/L15/CONG/BOCG/B/BOCG-15-B-{}-1.PDF"

# (doc_id, formacion, tipo, titulo, url, fichero, oficial, nota)
DOCS = [
    ("A5-D01", "PSOE", "programa electoral 2023", "Programa electoral generales 2023",
     "https://www.psoe.es/", "", "no oficial: excluido",
     "Web oficial protegida por Incapsula (HTML de bloqueo, no se evade). Solo existe la copia alojada por un medio (usada en v4)."),
    ("A5-D02", "PP", "programa electoral 2023 (completo)", "Programa electoral 23J (completo)",
     "https://www.pp.es/", "", "no oficial: excluido",
     "No se localizo el PDF completo en pp.es (URL probadas 404). Solo copia de medio (v4)."),
    ("A5-D03", "PP", "resumen oficial del programa 2023", "Resumen programa electoral (4/7/2023)",
     "https://www.pp.es/storage/2023/07/23.07.04._resumen_programa_electoral.pdf", "pp_resumen.pdf", "si",
     "Resumen oficial de 5 pp.; no es el programa completo: cota."),
    ("A5-D04", "Vox", "programa electoral 2023", "Programa electoral 23J",
     "https://www.voxespana.es/", "", "no oficial: excluido",
     "voxespana.es devuelve 403 a curl (no se evade). Solo copia de medio (v4)."),
    ("A5-D05", "Sumar", "programa electoral 2023", "Un programa para ti",
     "https://movimientosumar.es/wp-content/uploads/2023/07/Un-Programa-para-ti.pdf", "sumar.pdf", "si", "Web oficial."),
    ("A5-D06", "ERC", "programa electoral 2023", "Programa Eleccions Generals 2023",
     "https://static.esquerra.cat/uploads/20230905/e2023-programa.pdf", "erc.pdf", "si", "Texto en catalan."),
    ("A5-D07", "EH Bildu", "programa electoral 2023", "Compromiso de Euskal Herria Bildu 23J",
     "https://ehbildu.eus/dokumentuak/23J-COMPROMISO-DE-EUSKAL-HERRIA-BILDU.pdf", "bildu.pdf", "si", "Web oficial."),
    ("A5-D08", "PNV", "programa electoral 2023", "Con voz propia. Programa Electoral 23-J",
     "https://www.eaj-pnv.eus/es/adjuntos-documentos/20945/pdf/con-voz-propia-programa-electoral-23-j", "pnv.pdf", "si", "Web oficial."),
    ("A5-D09", "BNG", "programa electoral 2023", "Programa Electoral Eleccions Xerais 2023",
     "https://www.bng.gal/media/bnggaliza/files/2023/07/05/23_bng_xerais_programa.pdf", "bng.pdf", "si", "Texto en gallego."),
    ("A5-D10", "UPN", "programa electoral 2023", "Programa Electoral Generales 23 julio 2023",
     "https://www.upn.org/wp-content/uploads/2023/07/Programa-Generales-23J_V2-1.pdf", "upn.pdf", "si", "Web oficial."),
    ("A5-D11", "Gobierno", "ley", "Ley 12/2023, de 24 de mayo, por el derecho a la vivienda (BOE-A-2023-12203)",
     "https://www.boe.es/boe/dias/2023/05/25/pdfs/BOE-A-2023-12203.pdf", "ley12.pdf", "si", "BOE."),
    ("A5-D12", "Gobierno", "plan", "Real Decreto 326/2026, Plan Estatal de Vivienda 2026-2030 (BOE-A-2026-8872)",
     "https://www.boe.es/boe/dias/2026/04/23/pdfs/BOE-A-2026-8872.pdf", "plan_estatal.pdf", "si",
     "BOE; el plan mas reciente (sustituye al 2022-2025)."),
    ("A5-D13", "Junts", "programa electoral 2023", "Programa generales 2023",
     "https://www.junts.cat", "", "no localizado", "Sin PDF del programa 2023 en el sitio oficial ni en busqueda; solo manifiesto de otra convocatoria. Ver D26."),
    ("A5-D14", "CC", "programa electoral 2023", "Programa generales 2023",
     "https://www.coalicioncanaria.org", "", "no localizado", "Sin programa general 2023 en el sitio oficial (solo programas locales/insulares)."),
    ("A5-D15", "Podemos", "programa electoral 2023", "Programa generales 2023",
     "https://www.podemos.info", "", "no localizado", "Sitio oficial devuelve 403 a curl (no se evade); no se probo otra via."),
    ("A5-D16", "Compromis", "programa electoral 2023", "Programa generales 2023",
     "https://compromis.net", "", "no localizado", "Sin conexion (codigo 000) desde el entorno."),
]
# Proposiciones de ley de la XV legislatura (congreso.es), numero de BOCG-B
PL = [
    ("122/000196", "PSOE", "196+0", "Proposicion de Ley para impulsar el alquiler de viviendas a precios asequibles", 229),
    ("122/000253", "PP", "", "PL de medidas administrativas y procesales para la seguridad juridica de la ordenacion territorial y urbanistica", 303),
    ("122/000254", "PP", "", "PLO contra la ocupacion ilegal de inmuebles", 304),
    ("122/000193", "Vox", "", "PL de modificacion de la LAU (adquisicion preferente del inquilino)", 226),
    ("122/000039", "Vox", "", "PL de modificacion de la Ley de Bases del Regimen Local (padron y ocupacion)", 47),
    ("122/000251", "Sumar", "", "PL de modificacion de la Ley 12/2023", 300),
    ("122/000278", "Sumar", "", "PL de reforma del IBI y derecho a la vivienda", 327),
    ("122/000162", "Sumar", "", "PL de modificacion de la LAU", 186),
    ("122/000119", "Sumar", "", "PL de contratos de alquiler de temporada y de habitaciones", 134),
    ("122/000150", "Junts", "", "PLO de medidas urgentes contra la ocupacion ilegal de inmuebles", 173),
    ("122/000136", "ERC (con otros grupos)", "", "PL de contratos de alquiler temporales y de habitaciones", 154),
    ("122/000114", "PNV", "", "PL de modificacion del TRLSRU (RDL 7/2015)", 128),
    ("122/000102", "Grupo Mixto", "", "PL de prevencion de la especulacion y garantias de la vivienda como bien social", 115),
]
for i, (exp, form, _, tit, n) in enumerate(PL):
    DOCS.append((f"A5-D{17 + i:02d}", form, f"proposicion de ley {exp} (XV leg.)", tit, BOCG.format(n),
                 f"pl_{exp.replace('/', '_')}.pdf", "si", "BOCG congreso.es; texto de la iniciativa."))

COLS = ["doc_id", "formacion", "tipo", "titulo", "url", "fichero", "fecha_descarga", "sha256", "paginas",
        "oficial", "estado_texto", "nota"]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    INV.parent.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    old = {}
    if INV.exists():
        old = {r["doc_id"]: r for r in csv.DictReader(INV.open(encoding="utf-8"))}
    rows = []
    for d in DOCS:
        did, form, tipo, tit, url, fich, ofi, nota = d
        row = dict(zip(COLS, [did, form, tipo, tit, url, fich, "", "", "", ofi, "", nota]))
        if fich:
            p = DEST / fich
            if (not p.exists() or os.environ.get("FORCE") == "1"):
                subprocess.run(["curl", "-sS", "-L", "-m", "90", "-A", "Mozilla/5.0", "-o", str(p), url], check=False)
                row["fecha_descarga"] = today
            else:
                row["fecha_descarga"] = old.get(did, {}).get("fecha_descarga", today)
            if p.exists() and p.read_bytes()[:4] == b"%PDF":
                row["sha256"] = sha(p)
                out = subprocess.run(["pdfinfo", str(p)], capture_output=True, text=True).stdout
                row["paginas"] = next((ln.split()[1] for ln in out.splitlines() if ln.startswith("Pages")), "")
            else:
                row["estado_texto"] = "descarga fallida"
        rows.append(row)
    with INV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, COLS)
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()
