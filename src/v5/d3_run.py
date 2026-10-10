"""D3 · Tabla de convergencia: cifras clave del proyecto frente a organismos.

Sin red y determinista. Lee output/v5/cifras_clave.csv y data/raw/v5/d3_referencias.csv;
escribe output/v5/D3/{convergencia.csv, convergencia.md, registro.csv, resultado.json, hechos.json}.

Regla: «coincide» si los rangos se solapan o si la diferencia entre puntos medios es
<= 15 % del valor del proyecto; «difiere» en otro caso; «no comparable» cuando el concepto
o el periodo no permiten la comparación (columna comparable = no) o no se localizó la cifra.
"""
from __future__ import annotations

import csv
import json
import random
from pathlib import Path

SEED = 20261010
random.seed(SEED)
RAIZ = Path(__file__).resolve().parents[2]
CIFRAS = RAIZ / "output/v5/cifras_clave.csv"
REFS = RAIZ / "data/raw/v5/d3_referencias.csv"
SAL = RAIZ / "output/v5/D3"
TOL = 0.15
FECHA = "2026-10-10"
# Cifras cuyo min/max no es incertidumbre de España (rango entre países o p10-p90 municipal): se usa solo el valor.
SOLO_VALOR_PREFIJOS = ("CA-EU-", "R1C-021")

# Controles de transcripción: misma fuente primaria que el proyecto (no cuentan como coincidencia independiente).
CONTROL_MISMA_FUENTE = {"R15", "R16", "R19", "R20"}
# Referencias que repiten la misma cifra de otra referencia (la OCDE cita la estimación del BdE).
DUPLICADO_DE = {"R06": "R05"}
# Coincidencias con los mismos insumos primarios (ECP del INE y terminadas del MIVAU): concordancia aritmética.
MISMOS_INSUMOS = {"R03", "R04"}

# Contexto de método del proyecto que explica diferencias (no valora a los organismos).
METODO_PROY = {
    "deficit_2124_c1": "proyecto: aumento de hogares (ECP y EPA corregida) menos terminadas (Ministerio y Catastro), sin bajas",
    "B2-H2": "proyecto: déficit 2021-2025 de partida con bajas del parque = 0",
    "dh_2125": "proyecto: aumento de hogares ECP y EPA corregida por la ruptura de 2021",
    "terminadas_1924": "proyecto: rango Ministerio (fin de obra) y Catastro (altas), territorio común",
    "B1-H1": "proyecto: necesidad total A+R+V+F-M-K, suma provincial",
    "B2-H1": "proyecto: déficit acumulado a fin de 2030, suma de 52 provincias",
    "A23-P2": "proyecto: núcleo MIVAU (tasación), Notariado y Registradores en €/m2",
    "A23-P1": "proyecto: INE IPV",
    "A23-A2": "proyecto: núcleo IPC alquiler e IPVA",
    "A23-A3": "proyecto: IPVA nuevo contrato",
    "compradores_extranjeros": "proyecto: Ministerio y Notariado (residentes y no residentes)",
    "R1C-001": "proyecto: hogares (EFF, ECV, Censo 2021)",
    "R1C-021": "proyecto: mediana municipal",
}


def num(x: str) -> float | None:
    x = (x or "").strip()
    try:
        return float(x)
    except ValueError:
        return None


def intervalo(valor, mn, mx):
    v, a, b = num(valor), num(mn), num(mx)
    if a is not None and b is not None:
        lo, hi = min(a, b), max(a, b)
        if v is not None:
            lo, hi = min(lo, v), max(hi, v)
        return lo, hi
    if v is not None:
        return v, v
    return None


def fmt(iv) -> str:
    if iv is None:
        return "—"
    lo, hi = iv

    def f(z):
        return f"{z:,.0f}".replace(",", ".") if abs(z) >= 1000 else f"{z:g}"

    return f(lo) if lo == hi else f"{f(lo)}–{f(hi)}"


def clasificar(proy, ref, comparable, estado):
    if estado != "localizada" or ref is None:
        return "no comparable", None, ""
    if comparable == "no":
        return "no comparable", None, ""
    solapa = proy[0] <= ref[1] and ref[0] <= proy[1]
    mp, mr = (proy[0] + proy[1]) / 2, (ref[0] + ref[1]) / 2
    dif = (mr - mp) / abs(mp) if mp else None
    num_ok = solapa or (dif is not None and abs(dif) <= TOL)
    if comparable == "parcial":   # periodo, concepto o cobertura distintos: misma regla para todas las referencias
        return "comparable en parte", dif, ("numéricamente compatible" if num_ok else "numéricamente distinta")
    return ("coincide" if num_ok else "difiere"), dif, ""


def main() -> None:
    SAL.mkdir(parents=True, exist_ok=True)
    with CIFRAS.open(encoding="utf-8") as f:
        cif = {r["id"]: r for r in csv.DictReader(f)}
    with REFS.open(encoding="utf-8") as f:
        refs = list(csv.DictReader(f))

    filas = []
    for r in refs:
        c = cif.get(r["id_cifra"])
        if c is None:
            raise SystemExit(f"id_cifra ausente en cifras_clave: {r['id_cifra']}")
        if r["id_cifra"].startswith(SOLO_VALOR_PREFIJOS):
            proy = intervalo(c["valor"], "", "")
        else:
            proy = intervalo(c["valor"], c["min"], c["max"])
        ref = intervalo(r["valor"], r["min"], r["max"])
        veredicto, dif, num_parcial = clasificar(proy, ref, r["comparable"], r["estado"])
        if r["ref_id"] in CONTROL_MISMA_FUENTE and veredicto in ("coincide", "difiere"):
            veredicto = "control misma fuente"
        motivos = []
        if num_parcial:
            motivos.append(f"comparable en parte ({num_parcial}; no cuenta como coincidencia ni como diferencia)")
        if r["ref_id"] in DUPLICADO_DE:
            motivos.append(f"misma cifra que {DUPLICADO_DE[r['ref_id']]} (la OCDE cita al BdE): no se cuenta dos veces")
        if r["ref_id"] in MISMOS_INSUMOS:
            motivos.append("el BdE usa los mismos insumos primarios que B2-H2 (ECP del INE y terminadas del MIVAU): concordancia aritmética, no confirmación independiente")
        if r["estado"] != "localizada":
            motivos.append("cifra del organismo no localizada")
        if r["periodo"].strip() != c["periodo"].strip():
            motivos.append(f"periodo: proyecto {c['periodo']}, organismo {r['periodo']}")
        if r["cobertura"].strip().lower() != c["cobertura"].strip().lower():
            motivos.append(f"cobertura: proyecto {c['cobertura']}, organismo {r['cobertura']}")
        motivos.append(f"concepto del organismo: {r['concepto']}")
        if r["id_cifra"] in METODO_PROY:
            motivos.append(f"método: {METODO_PROY[r['id_cifra']]}")
        if r["nota"]:
            motivos.append(r["nota"])
        filas.append({
            "ref_id": r["ref_id"],
            "id_cifra": r["id_cifra"],
            "indicador": c["indicador"],
            "valor_proyecto": fmt(proy),
            "unidad_proyecto": c["unidad"],
            "periodo_proyecto": c["periodo"],
            "capa": c["capa"],
            "organismo": r["organismo"],
            "documento": f"{r['documento']} ({r['edicion']})" if r["edicion"] else r["documento"],
            "pagina_cuadro": r["pagina_cuadro"],
            "valor_organismo": fmt(ref),
            "unidad_organismo": r["unidad"],
            "periodo_organismo": r["periodo"],
            "diferencia_relativa_pct": "" if dif is None else f"{100 * dif:.1f}",
            "veredicto": veredicto,
            "explicacion": "; ".join(motivos),
            "url": r["url"],
        })

    cols = list(filas[0].keys())
    with (SAL / "convergencia.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(filas)

    cats = ("coincide", "difiere", "comparable en parte", "control misma fuente", "no comparable")
    n = {k: sum(1 for x in filas if x["veredicto"] == k) for k in cats}
    n_ins = sum(1 for x in filas if x["veredicto"] == "coincide" and x["ref_id"] in MISMOS_INSUMOS)
    n_noloc = sum(1 for r in refs if r["estado"] != "localizada")
    cifras_usadas = sorted({x["id_cifra"] for x in filas})

    md = [
        "# D3 · Convergencia de cifras clave con organismos",
        "",
        f"Generado por src/v5/d3_run.py (sin red). Fecha: {FECHA}. Referencias: data/raw/v5/d3_referencias.csv.",
        "",
        f"Regla: «coincide» o «difiere» solo si concepto, periodo y cobertura son comparables: coincide si los rangos se solapan o la diferencia entre puntos medios es ≤ {int(TOL * 100)} % "
        "del valor del proyecto. «Comparable en parte» (periodo, concepto o cobertura distintos) no cuenta como coincidencia ni como diferencia, con la misma regla para todas las referencias. "
        "«Control misma fuente» = misma fuente primaria que el proyecto (transcripción). «No comparable» si el concepto lo impide o la cifra no se localizó. "
        "Las diferencias se describen por concepto, periodo, cobertura, método o bajas; no se valora a ningún organismo.",
        "",
        f"Resumen: {len(cifras_usadas)} cifras del proyecto, {len(filas)} referencias; "
        f"coincidencias de fuentes distintas con concepto, periodo y cobertura comparables: {n['coincide']} (de ellas {n_ins} con los mismos insumos primarios); "
        f"difieren {n['difiere']}; comparables en parte {n['comparable en parte']} (R06 repite la cifra de R05); "
        f"controles de la misma fuente {n['control misma fuente']} (no cuentan); no comparables {n['no comparable']} (de ellas {n_noloc} no localizadas).",
        "",
        "| ref | cifra (id) | proyecto | capa | organismo · documento · pág. | organismo | dif. % | veredicto | explicación |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for x in filas:
        md.append(
            f"| {x['ref_id']} | {x['id_cifra']} | {x['valor_proyecto']} {x['unidad_proyecto']} ({x['periodo_proyecto']}) "
            f"| {x['capa']} | {x['organismo']} · {x['documento']} · {x['pagina_cuadro'] or '—'} "
            f"| {x['valor_organismo']} {x['unidad_organismo']} ({x['periodo_organismo']}) "
            f"| {x['diferencia_relativa_pct'] or '—'} | {x['veredicto']} | {x['explicacion']} |"
        )
    md += [
        "",
        "Notas:",
        "- Varias referencias de Eurostat (sobrecarga, emancipación, IPV, IPCA alquiler) proceden de la misma fuente "
        "primaria que la cifra del proyecto: su coincidencia es un control de transcripción, no una confirmación independiente.",
        "- La cifra de 600.000 de la OCDE (2022-2025) es la estimación del Banco de España citada por la OCDE (R06 = R05, una sola cifra).",
        "- Tensión interna declarada: R01/R02 comparan la cifra C1 de 2021-2024 (aumento de hogares con ECP y EPA corregida, 562.692-688.692), mientras que R03-R05 usan B2-H2 (2021-2025, solo ECP, 700.934): "
        "son dos construcciones distintas. Con el aumento de hogares de 2025 (240.000, BdE) y las terminadas de 2025 (92.000), 562.692 + (240.000 − 92.000) ≈ 710.692 supera 700.934; "
        "la diferencia (≈ 9.800 viviendas, 1,4 %) puede deberse a las dos construcciones (EPA corregida frente a solo ECP; terminadas de cada fuente) y no se ha descompuesto en D3. "
        "Esta tensión no afecta al recuento de coincidencias, que usa B2-H2 para R03-R05.",
        "- R09 y R10 son paráfrasis de docs/literatura.md, no citas literales; R04 no tiene URL de documento localizada (véase la referencia).",
        "- La coincidencia numérica no cambia la capa de la cifra del proyecto (sin promoción de capa).",
    ]
    (SAL / "convergencia.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    with (SAL / "registro.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["especificacion", "descripcion", "n", "p", "p_ajustado", "nota"])
        w.writerow(["D3-regla-15", f"coincide si solape o |dif| <= {TOL}", len(filas), "", "",
                    "comparación contable; sin contraste de hipótesis, Holm/BH no aplica"])

    resultado = {
        "rama": "D3",
        "pregunta": "¿Coinciden las cifras clave del proyecto con las publicadas por BdE, Ministerio, INE, OCDE y Eurostat?",
        "capa": "C4 (comparación descriptiva; no altera la capa de cada cifra)",
        "datos": "output/v5/cifras_clave.csv; data/raw/v5/d3_referencias.csv",
        "N": len(filas),
        "metodo": f"comparación de rangos; coincide si solape o diferencia <= {int(TOL * 100)} %",
        "estimacion": n,
        "ic95": None,
        "p_ajustado": None,
        "nivel_evidencia": "DESCRIPTIVO",
        "diagnosticos": {"referencias_no_localizadas": n_noloc, "cifras_proyecto": cifras_usadas},
        "fuera_muestra": {"modelo": None, "rmse": None, "dm_vs_ar4": None},
        "notas": "Titular: solo cuentan coincidencias de fuentes distintas con concepto, periodo y cobertura comparables; controles de la misma fuente, comparables en parte y R06 = R05 se separan. Tensión entre el déficit C1 2021-2024 (ECP+EPA) y B2-H2 (solo ECP) declarada en convergencia.md. Las coincidencias con Eurostat en sobrecarga, emancipación, IPV y alquiler comparten fuente primaria con el proyecto.",
    }
    (SAL / "resultado.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    hechos = [
        {"id": f"D3-{k.replace(' ', '_')}", "indicador": f"Referencias de organismos: {k}", "valor": v,
         "min": None, "max": None, "unidad": "referencias", "periodo": FECHA, "cobertura": "España",
         "fuentes": "BdE; OCDE; Eurostat; INE; Ministerio", "capa": "C4", "fecha_dato": FECHA}
        for k, v in n.items()
    ]
    (SAL / "hechos.json").write_text(json.dumps(hechos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"D3: {len(filas)} referencias; {n}")


if __name__ == "__main__":
    main()
