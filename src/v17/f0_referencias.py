"""V17 · Fase 0 · docs/v17/referencias_bde.md: índice de documentos leídos y comparación con el proyecto (análisis a posteriori).

Lee las fichas de la fase 0 (output/v17/f0/*.json, escritas por los lectores de literatura a partir de los documentos originales) y
output/v5/cifras_clave.csv. Escribe el índice y la tabla «cifra del proyecto frente a la del Banco de España» cuando miden lo mismo
o algo parecido, con la razón de la diferencia. Las cifras del Banco de España se transcriben de las fichas (documento y página);
las del proyecto se leen de cifras_clave por su id. Determinista; sin red.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
F0 = RAIZ / "output" / "v17" / "f0"
SALIDA = RAIZ / "docs" / "v17" / "referencias_bde.md"


def n(x, d=None) -> str:
    if x is None or pd.isna(x):
        return "n/d"
    if d is None:
        d = 0 if abs(x) >= 100 else 2
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


# (magnitud, ids del proyecto, cifra del BdE o del BCE con su documento, por qué difieren o coinciden)
COMPARACION = [
    ("Déficit de vivienda acumulado", ["L3-DEF-2124-SINBAJAS", "L3-DEF-2124-SENS"],
     "Unas 750.000 viviendas en 2021-2025, el 3,7 % de los hogares de 2025; el 52,5 % en seis provincias (IA2025, cap. 2, pp. 145-146). "
     "700.000 con datos del primer semestre de 2025 (IEF otoño 2025). Entre 400.000 y 450.000 en 2022-2024 (IA2024, recuadro 4, p. 167). "
     "Unas 375.000 en 2022-2023 más de 225.000 proyectadas para 2024-2025 (IA2023, p. 251).",
     "Periodo: el BdE incluye 2025; nuestra cota C2 es 2021-2024 sin bajas. Definición: el BdE compara la creación neta de hogares con las "
     "viviendas terminadas; el proyecto usa el mismo saldo con correcciones de la EPA y variantes de terminadas, y da un rango en lugar de "
     "un punto. Sumando un año más de déficit (hogares de 2025 menos terminadas de 2025, unos 150.000 según el propio BdE), el máximo de "
     "nuestra cota (710.542) queda en el orden de la cifra del BdE. No hay contradicción de signo ni de orden de magnitud."),
    ("Hogares nuevos en 2025", ["dh_2125"],
     "Unos 240.000 (IA2025, pp. 124 y 146); 225.000 en el IEF de primavera de 2026 (inconsistencia interna del BdE).",
     "Nuestro dh_2125 acumula 2021-2025 (en torno a 1 millón, unos 200.000-250.000 por año), compatible con el orden del BdE."),
    ("Viviendas terminadas al año", ["terminadas_1924"],
     "Unas 92.000 en 2025 (IA2025, pp. 124 y 126).",
     "El proyecto da 2019-2024 en territorio común (sin País Vasco ni Navarra); el BdE da 2025 nacional. Mismo orden."),
    ("Sobrevaloración del precio", ["R1B-G-0", "V72-GSADF-ratios-bh", "V17-B5-PRECIO-RENTA"],
     "Desequilibrio de precios del 10-15 % en diciembre de 2025 (IEF primavera 2026), 5,3-12,7 % en junio de 2025 y 3,0-9,4 % a finales "
     "de 2024 (IEF otoño 2025); máximo del promedio del 24 % a finales de 2007.",
     "No miden lo mismo. El GSADF del proyecto contrasta si hay una explosión estadística (burbuja racional) en el cociente; no la "
     "encuentra tras el ajuste múltiple. El BdE mide la distancia del precio a sus fundamentales con varios modelos. Un precio "
     "puede estar por encima de sus fundamentales sin crecer de forma explosiva. «No hay exuberancia estadística» es compatible con «hay "
     "sobrevaloración moderada»; la fase 3 (fila «burbuja») lo audita."),
    ("Esfuerzo de acceso", ["V17-B5-ESFUERZO-TEORICO", "V16-ESF-DES-alquiler_mercado-observado-total-2019_2025"],
     "Esfuerzo teórico del 38 % de la renta en 2026T2 (Síntesis de indicadores del BdE, serie SI_1_5.44); el IA2025 lo describe como "
     "deterioro de la accesibilidad, sobre todo para jóvenes e inquilinos.",
     "El indicador del BdE es teórico (cuota de una hipoteca tipo sobre la renta bruta por hogar); el del proyecto es el esfuerzo "
     "observado en la ECV (gasto efectivo sobre renta neta). Miden cosas distintas y se presentan juntas."),
    ("Compras de no residentes", ["R1A-H1", "V16-Q8-5"],
     "7,4 % de las compras en 2021-2025 (IA2025, p. 149; la tabla 2.8 lo rotula como cuota de 2025: inconsistencia interna). Unas "
     "30.000 compras en 2025 (IA2025) frente a 55.000 brutas y 30.000 netas (IEF primavera 2026).",
     "Del mismo orden que nuestras cuotas de 2025 (6,8 % de extranjeros no residentes según el MIVAU; 7,6 % según V16-Q8). La diferencia es de "
     "fuente (Registradores, notarios o MIVAU) y de definición (extranjeros no residentes o todos los no residentes)."),
    ("Efecto de los tipos sobre el precio", ["V16-Q5-p-h4", "V16-Q5-a-h4"],
     "BCE, zona euro: +1 pp en el tipo hipotecario, en torno a −5 % en precios y −8 % en inversión residencial tras dos años "
     "(docs/v17/referencias/bde_bce_documentos.md, tema 4). No se encontró una elasticidad del BdE para España.",
     "No son comparables directamente. Q5 mide la respuesta a una DT de sorpresa monetaria de alta frecuencia (Jarociński-Karadi), no "
     "a 1 pp del tipo hipotecario, y es un resultado no concluyente (C4). La fase 3 (fila «tipos») usa la elasticidad del BCE como "
     "referencia externa."),
    ("Vivienda turística sobre el alquiler", ["B4-v3-vut-cantidad"],
     "10,8 % de vivienda turística sobre el alquiler (IA2025, diapositiva 40 de la presentación); 11,8 % en el cuadro A.3 del DO 2432 "
     "(mediana de secciones 2,3 %).",
     "No miden lo mismo. La cota publicada del proyecto («como máximo 2,7 % del stock de alquiler») es el AUMENTO 2020-2024 de las "
     "viviendas turísticas sobre el stock de alquiler, con sustitución uno a uno, no su peso. El BdE da el peso del stock turístico. "
     "La fase 3 (fila «turísticos») audita cómo se resumió la cota en la divulgación."),
    ("Grandes tenedores", [],
     "2,4 % de las viviendas alquiladas como residencia habitual en manos de personas físicas con 11 o más viviendas, 2024 (IA2025, "
     "cuadro 2.11, p. 169); no incluye a las personas jurídicas.",
     "El proyecto no publicó una cifra («no hay datos de titularidad»). La fase 1 reunió cifras parciales (docs/v17/fuentes/titularidad.md) "
     "y la fase 3 (fila «grandes_tenedores») audita la frase."),
    ("Compras financiadas con hipoteca", ["V17-B5-SIN-HIPOTECA-MIN"],
     "52 % de las compras de 2025 financiadas con hipoteca (IA2025, p. 124).",
     "Nuestra aproximación (cota inferior de compras sin hipoteca, 30 % en 2025) es compatible con el 48 % sin hipoteca que implica el "
     "BdE, porque la estadística de hipotecas incluye préstamos no ligados a una compra."),
]


def main() -> int:
    ck = pd.read_csv(RAIZ / "output" / "v5" / "cifras_clave.csv").set_index("id")
    hechos_v17 = {}
    for p in (RAIZ / "output" / "v17").rglob("hechos.json"):
        for h in json.loads(p.read_text(encoding="utf-8")):
            hechos_v17[h["id"]] = h
    L = ["# V17 · Referencias del Banco de España, el BCE y el INE", "",
         "Análisis a posteriori (V17). Generado por src/v17/f0_referencias.py a partir de las fichas de la fase 0 "
         "(docs/v17/referencias/*.md, output/v17/f0/*.json) y de output/v5/cifras_clave.csv. Las cifras ajenas se transcriben de "
         "los documentos originales, con su página o recuadro; las de prensa están comprobadas en docs/v17/correcciones.md.", "",
         "## Documentos leídos", "", "| Documento | Fecha | Lectura | URL |", "|---|---|---|---|"]
    for nombre in ("bde_informes", "bde_bce_documentos", "ine_demografia"):
        d = json.loads((F0 / f"{nombre}.json").read_text(encoding="utf-8"))
        for x in d["documentos"]:
            tit = x.get("titulo") or x.get("operacion") or x.get("publicacion") or x.get("id")
            fecha = x.get("fecha") or x.get("publicacion") or ""
            lect = x.get("lectura") or x.get("leido") or ""
            L.append(f"| {str(tit)[:110]} | {str(fecha)[:40]} | {str(lect)[:40]} | {x.get('url', '')} |")
    L += ["", "Fichas completas: docs/v17/referencias/bde_informes.md, bde_bce_documentos.md e ine_demografia.md.", "",
          "## Comparación con el proyecto", "",
          "| Magnitud | Proyecto (id: valor [rango], capa) | Banco de España o BCE | Por qué coinciden o difieren |", "|---|---|---|---|"]
    for mag, ids, bde, porque in COMPARACION:
        proy = []
        for i in ids:
            if i in ck.index:
                r = ck.loc[i]
                proy.append(f"{i}: {n(r.valor)} [{n(r['min'])}; {n(r['max'])}] {r.unidad}, {r.periodo}, {r.capa}")
            elif i in hechos_v17:
                h = hechos_v17[i]
                proy.append(f"{i}: {n(h['valor'])} {h['unidad']}, {h['periodo']}, C4 (V17, {h['lectura_v17']})")
            else:
                raise SystemExit(f"id {i} no encontrado")
        L.append(f"| {mag} | {'<br>'.join(proy) or 'sin cifra publicada'} | {bde} | {porque} |")
    L += ["", "## Lo que no se encontró", "",
          "- Ninguna elasticidad del Banco de España del precio o de las compraventas a los tipos para España (solo estimaciones del BCE para la zona euro).",
          "- Ningún documento del Banco de España sobre inmigración y vivienda con una estimación propia.",
          "- La estimación del Ministerio del 15 % de la oferta de alquiler en grandes propietarios (tarea del autor).",
          "- Series descargables de LTI y de sobrevaloración: solo están en gráficos del IEF.", ""]
    SALIDA.write_text("\n".join(L), encoding="utf-8")
    print(f"f0_referencias V17: {len(COMPARACION)} comparaciones -> {SALIDA.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
