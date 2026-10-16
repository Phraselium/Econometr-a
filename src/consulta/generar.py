"""V8.1-B · `make consulta`: genera consulta/ y llms.txt (capa de consulta para asistentes y lectores). Nunca se editan a mano.

Fuentes: output/v5/cifras_clave.csv (única fuente de cifras), output/v5/cifras_superadas.csv, fichas del verificador (v5, v7.1, V8),
docs/v6_1/historial_conclusiones.md (conclusiones v1-V8), output/v8/M2/hipotesis_m2_retirada.csv, docs/v8/notas_release.md y
docs/v8/tareas_autor.md. Determinista y sin red: dos ejecuciones dan el mismo contenido.

Las cifras de consulta/ se insertan SIEMPRE desde cifras_clave por id (función `valor_texto`); ninguna se teclea.
V14.2: las cifras que terceros_1_0 = «excluir» retira (src/v14/terceros_1_0.py) aparecen con estado «no publicada (1.0)», sin
valor y con la marca en lugar de la cifra; siguen en cifras_clave sin cambios.
Elección de version.json: el campo `commit` es el del último cambio de contenido de output/ (`git log -1 --format=%h -- output`), no
HEAD: HEAD cambia con cada commit (incluido el que versiona consulta/) y rompería la comparación con lo versionado.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
from src.v14 import terceros_1_0 as T10  # noqa: E402

PROYECTO = json.loads((RAIZ / "proyecto.json").read_text(encoding="utf-8"))   # V13: versión pública, repositorio, web y DOI (única fuente)
CAB_MD = "<!-- Generado por `make consulta` (src/consulta/generar.py). No editar a mano: se regenera y un test lo comprueba. -->\n\n"
CAPAS_VALIDAS = ("C1", "C2", "C3", "C3s", "C4")
ORDEN_VERSION = ["v4", "v5", "v5.1", "v6", "v6.1", "v6.2", "v6.3", "v7", "v7.1", "v7.2", "V8"]
FICHEROS = ("LEEME_ASISTENTE.md", "hallazgos.json", "hallazgos.md", "preguntas_frecuentes.md", "glosario.md", "indice_ficheros.md",
            "version.json")


# ---------------------------------------------------------------- lectura de fuentes
def _csv(ruta: str) -> list[dict]:
    with open(RAIZ / ruta, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def cargar_cifras() -> dict[str, dict]:
    ret = T10.retiradas()
    cifras = {r["id"]: r for r in _csv("output/v5/cifras_clave.csv")}
    for i, f in ret.items():   # V14.2: no publicadas en la 1.0 (terceros_1_0 = excluir)
        if i in cifras:
            cifras[i]["_no_publicada"] = T10.marca(f)
    return cifras


def cargar_superadas() -> dict[str, dict]:
    return {r["id"]: r for r in _csv("output/v5/cifras_superadas.csv")}


def _num(s) -> float | None:
    try:
        return float(s) if str(s).strip() != "" else None
    except ValueError:
        return None


def fmt_num(x: float) -> str:
    a = abs(x)
    if a >= 1000:
        t = f"{x:,.0f}".replace(",", ".")
    elif a >= 100:
        t = f"{x:.1f}"
    elif a >= 1:
        t = f"{x:.2f}"
    elif a >= 0.01:
        t = f"{x:.3f}"
    else:
        t = f"{x:.3g}"
    if "," not in t and "." in t and a < 1000:
        t = t.rstrip("0").rstrip(".")
        return t.replace(".", ",")
    return t


def _unidad(u: str) -> str:
    u = re.split(r"\s\(|;", u)[0].strip()
    return u if len(u) <= 30 else u[:29].rstrip() + "…"


def valor_texto(r: dict) -> str:
    """Valor de una fila de cifras_clave con unidad y rango: la única forma en que consulta/ escribe una cifra."""
    if r.get("_no_publicada"):
        return r["_no_publicada"]
    v, lo, hi = _num(r["valor"]), _num(r["min"]), _num(r["max"])
    if r.get("sentido_min_max", "rango") != "rango":   # min y max no son un rango del valor (umbral, banda de otra cosa, variantes…)
        lo = hi = None
    u = _unidad(r["unidad"])
    if u in ("p-valor", "proporción", "probabilidad", "coeficiente", "rho", "correlación") or u.startswith("estadístico"):
        u = ""
    if v is None and lo is not None and hi is not None:
        base, rango = f"{fmt_num(lo)} a {fmt_num(hi)}", ""
    elif v is None:
        base, rango = "sin valor puntual", ""
    else:
        base = fmt_num(v)
        ok = lo is not None and hi is not None and lo <= hi and lo - 1e-9 <= v <= hi + 1e-9 and (lo, hi) != (v, v)
        rango = f" ({fmt_num(lo)} a {fmt_num(hi)})" if ok else ""
    return f"{base} {u}{rango}".strip()


def _ruta_fichero(origen: str) -> str:
    return origen.split(":")[0].strip()


def _version_de_ruta(ruta: str) -> str:
    m = re.match(r"output/(v\d+(?:_\d+)?)/", ruta)
    if not m:
        return "v5"
    v = m.group(1)
    return "V8" if v == "v8" else v.replace("_", ".")


METODOS = [
    (r"^V8-(SVAR|QNA|PFSTAR|OBS|H8-[1-4]-)", "SVAR bayesiano con restricciones de signo y de cero (descomposición histórica)"),
    (r"^V8-(H8-[5-7]|M5)", "LP-IV con instrumento externo (diagnóstico de primera etapa, F efectivo)"),
    (r"^V8-(REGLA|VOTOS)", "Regla de designación del factor más relevante (votos de cuatro métodos)"),
    (r"^V8-M0", "Efectos por periodo (M0), control BH"), (r"^V8-(M1|H8-[89])", "Factor común de las 17 CCAA (componentes principales)"),
    (r"^V8-M4", "Largo plazo: ARDL con cotas y contabilidad hogares-viviendas"), (r"^V8-M7", "Multiverso de especificaciones (tope 50.000)"),
    (r"^V8-M8", "Componente común regional (M8)"), (r"^V8-(M9|OOS)", "Predicción fuera de muestra frente a AR(4)"),
    (r"^V71", "Simulación condicional de instrumentos (dosis y coste)"), (r"^V72", "GSADF (exuberancia)"),
    (r"^V7-", "Paneles de CCAA (MG, PMG, CS-DL), diferido"), (r"^V6-M4|^K1|^m3", "Predicción con validación sellada"),
    (r"^m2_", "BMA (probabilidad de inclusión posterior)"), (r"^m1a|^m1b|^K3|^K2", "Efectos fijos de panel (asociación)"),
    (r"^(B1|B2|E-B1|T[1-4]|L3|D2|dh_|terminadas|latente)", "Contabilidad de hogares y viviendas (déficit y necesidad)"),
    (r"^(R1A|R1B|R1C|compradores|A23|CA-|CB-|CC-|A4-|A5-|D3)", "Estadística descriptiva de fuentes oficiales"),
    (r"^(D1)", "Rúbrica de instrumentos"), (r"^(B3|B4)", "Asociación y reparto de varianza (Shapley)"),
]


def metodo_de(i: str) -> str:
    for pat, m in METODOS:
        if re.search(pat, i):
            return m
    return "ver ficha de origen"


def mercado_de(texto: str) -> str:
    t = texto.lower()
    alq = bool(re.search(r"alquiler|renta de fianzas|fianzas|contratos nuevos", t))
    cmp_ = bool(re.search(r"compra|precio|tasad|compraventa|ipv|venta", t))
    if alq and re.search(r"contratos nuevos|fianzas|ipva", t):
        return "alquiler (contratos nuevos)" if not cmp_ else "ambos"
    if alq and re.search(r"stock|serpavi|ipc|parque", t):
        return "alquiler (parque)" if not cmp_ else "ambos"
    if alq and cmp_:
        return "ambos"
    return "alquiler" if alq else ("compra" if cmp_ else "no aplica")


def _limpia(s: str, n: int | None = None) -> str:
    s = re.sub(r"\s+", " ", str(s)).replace("|", "/").strip()
    return s if n is None or len(s) <= n else s[: n - 1].rstrip() + "…"


def _capa(txt: str) -> str:
    c = re.findall(r"C3s|C[1-4]", txt)
    return max(c, key=CAPAS_VALIDAS.index) if c else "C4"


# ---------------------------------------------------------------- hallazgos
def _fichas() -> list[tuple[str, Path]]:
    out = []
    for p in sorted((RAIZ / "output/v5/verificador/fichas").glob("*.json")):
        out.append(("v5", p))
    for rel, v in (("output/v7_1/fichas/fichas_verificador.json", "v7.1"), ("output/v8/fichas_verificador_v8.json", "V8")):
        if (RAIZ / rel).exists():
            out.append((v, RAIZ / rel))
    return out


def _tablas_historial() -> list[dict]:
    txt = (RAIZ / "docs/v6_1/historial_conclusiones.md").read_text(encoding="utf-8")
    filas, cab, seccion = [], None, "v1-v6"
    for linea in txt.splitlines():
        if linea.startswith("## "):
            m = re.search(r"Adenda (V?\d+(?:\.\d+)?)", linea)
            seccion = m.group(1) if m else seccion
            cab = None
            continue
        if not linea.startswith("|"):
            cab = None if linea.strip() == "" else cab
            continue
        celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
        if set("".join(celdas)) <= set("-: "):
            continue
        if cab is None:
            cab = celdas
            continue
        d = dict(zip(cab, celdas))
        d["_seccion"] = seccion
        filas.append(d)
    return filas


def construir_hallazgos(cifras: dict[str, dict], superadas: dict[str, dict]) -> list[dict]:
    H: list[dict] = []

    def base(**kw):
        h = {"id": "", "enunciado": "", "cifra": None, "rango": None, "unidad": "", "periodo": "", "ambito": "", "mercado": "",
             "capa": "C4", "metodo": "", "fuente": "", "ruta": "", "version": "", "estado": "vigente", "tipo": "cifra"}
        h.update(kw)
        return h

    for i, r in cifras.items():
        ruta = _ruta_fichero(r["origen"])
        if r.get("_no_publicada"):   # V14.2: sin valor, con la marca y su propio estado
            H.append(base(id=i, enunciado=_limpia(r["indicador"]), unidad=r["unidad"], periodo=r["periodo"], ambito=r["cobertura"],
                          mercado=mercado_de(r["indicador"] + " " + r["unidad"]), capa=r["capa"], metodo=metodo_de(i), fuente=r["fuentes"],
                          ruta=ruta, version=_version_de_ruta(ruta), estado="no publicada (1.0)", fecha_dato=r["fecha_dato"],
                          cifra_texto=r["_no_publicada"], motivo="no publicada en la versión 1.0 por la licencia de su fuente "
                          "(proyecto.json, terceros_1_0 = excluir; publicacion/cifras_no_publicadas_1_0.csv). Sigue en cifras_clave sin cambios."))
            continue
        lo, hi = _num(r["min"]), _num(r["max"])
        es_rango = r["sentido_min_max"] == "rango"
        H.append(base(id=i, enunciado=_limpia(r["indicador"]), cifra=_num(r["valor"]), rango=[lo, hi] if es_rango and lo is not None and hi is not None else None,
                      unidad=r["unidad"], periodo=r["periodo"], ambito=r["cobertura"], mercado=mercado_de(r["indicador"] + " " + r["unidad"]),
                      capa=r["capa"], metodo=metodo_de(i), fuente=r["fuentes"], ruta=ruta, version=_version_de_ruta(ruta),
                      fecha_dato=r["fecha_dato"], cifra_texto=valor_texto(r), min_max=[lo, hi, r["sentido_min_max"]]))
    for i, r in superadas.items():
        ruta = _ruta_fichero(r["origen"])
        lo, hi = _num(r["min"]), _num(r["max"])
        H.append(base(id=i, enunciado=_limpia(r["indicador"]), cifra=_num(r["valor"]), rango=[lo, hi] if r["sentido_min_max"] == "rango" and lo is not None and hi is not None else None,
                      unidad=r["unidad"], periodo=r["periodo"], ambito=r["cobertura"], mercado=mercado_de(r["indicador"] + " " + r["unidad"]),
                      capa=r["capa"], metodo=metodo_de(i), fuente=r["fuentes"], ruta=ruta, version=_version_de_ruta(ruta), estado="superada",
                      fecha_dato=r["fecha_dato"], sustituida_por=r["sustituida_por"], motivo=_limpia(r["motivo"])))
    for v, p in _fichas():
        for f in json.loads(p.read_text(encoding="utf-8")) if p.read_text(encoding="utf-8").lstrip().startswith("[") else [json.loads(p.read_text(encoding="utf-8"))]:
            ev = f.get("evidencia") or []
            H.append(base(id=f"FICHA-{f['id']}", enunciado=_limpia(f.get("enunciado", "")), periodo="", ambito="España",
                          mercado=mercado_de(f.get("enunciado", "") + " " + f.get("tema", "")), capa=_capa(str(f.get("capa", "C4"))),
                          metodo="Ficha del verificador (afirmación evaluada)", fuente=("verificador" if str(f.get("literatura", "")).startswith("No aplica") else _limpia(str(f.get("literatura", "")), 200)) or "verificador",
                          ruta=ev[0] if ev and (RAIZ / ev[0]).exists() else p.relative_to(RAIZ).as_posix(), version=v, tipo="ficha",
                          veredicto=f.get("veredicto", ""), ids_cifras=f.get("ids_cifras", []), magnitud=_limpia(f.get("magnitud", ""))))
    for k, d in enumerate(_tablas_historial(), 1):
        enun = " · ".join(x for x in (d.get("Variable") or d.get("Factor"), d.get("Medida de resultado")) if x)
        if not enun:
            enun = " · ".join(v for k, v in d.items() if not k.startswith("_") and v)[:200]
        if not enun:
            continue
        est = next((v for kk, v in d.items() if kk.startswith("Estado")), "")
        vs = re.findall(r"[vV](\d+(?:\.\d+)?)", d.get("Versión") or d["_seccion"])
        ver = ("V8" if vs[-1] == "8" else f"v{vs[-1]}") if vs else "v6.1"
        H.append(base(id=f"HIST-{k:03d}", enunciado=_limpia(enun), periodo=d.get("Periodo", ""), ambito=d.get("Nivel", ""),
                      mercado=mercado_de(d.get("Medida de resultado", "")), capa=_capa(d.get("Capa", "C4")), metodo=_limpia(d.get("Método", ""), 160),
                      fuente=_limpia(d.get("Fuente", "") or "historial de conclusiones", 200), ruta="metodologia/historial_conclusiones.md",
                      version=ver, estado="superada" if "**Cambia" in est else "vigente", tipo="conclusion_historica",
                      magnitud=_limpia(d.get("Magnitud", ""), 300), estado_texto=_limpia(est, 300)))
    for k, r in enumerate(_csv("output/v8/M2/hipotesis_m2_retirada.csv"), 1):
        H.append(base(id=f"RET-{r['id']}", enunciado=_limpia(r["hipotesis"]), cifra=_num(r["contribucion_pp"]), unidad="pp", periodo=r["periodo"],
                      ambito="España", mercado=r["mercado"], capa=r["capa"], metodo="SVAR bayesiano (versión retirada por especificación errónea)",
                      fuente="output/v8/M2", ruta="output/v8/M2/hipotesis_m2_retirada.csv", version="V8", estado="retirada", tipo="hipotesis_retirada",
                      motivo=_limpia(r["estado"])))
    orden = {v: n for n, v in enumerate(ORDEN_VERSION)}
    H.sort(key=lambda h: (orden.get(h["version"], 99), h["tipo"], h["id"]))
    return H


def hallazgos_md(H: list[dict], cifras: dict[str, dict]) -> str:
    L = [CAB_MD, "# Registro de hallazgos\n\n",
         "Un registro por hallazgo de las versiones vigentes (v5-V8, con v4 donde sigue en cifras_clave): cifras de `output/v5/cifras_clave.csv`, fichas del verificador, ",
         "conclusiones del historial e hipótesis retiradas. Las superadas y retiradas están al final y **no se citan**. La versión legible por máquina es "
         "[hallazgos.json](hallazgos.json). Las capas se leen según [metodologia/capas.md](../metodologia/capas.md): causalidad solo en C3 y C3s.\n\n"]
    vig = [h for h in H if h["estado"] == "vigente"]
    cnt: dict[str, int] = {}
    for h in vig:
        cnt[h["version"]] = cnt.get(h["version"], 0) + 1
    L.append("Vigentes por versión: " + "; ".join(f"{v}: {n}" for v, n in sorted(cnt.items(), key=lambda t: ORDEN_VERSION.index(t[0]) if t[0] in ORDEN_VERSION else 99)) + f". Total vigentes: {len(vig)}.\n\n")
    for ver in [v for v in ORDEN_VERSION if any(h["version"] == v for h in vig)] + sorted({h["version"] for h in vig} - set(ORDEN_VERSION)):
        sub = [h for h in vig if h["version"] == ver]
        L.append(f"## Versión {ver}\n\n| id | enunciado | cifra | capa | periodo | origen |\n|---|---|---|---|---|---|\n")
        for h in sub:
            cifra = valor_texto(cifras[h["id"]]) if h["tipo"] == "cifra" else (h.get("veredicto") or "(sin cifra puntual)")
            if h["tipo"] == "conclusion_historica":
                cifra = _limpia(h.get("magnitud", ""), 90) or "(sin cifra puntual)"
            enlace = f"[{Path(h['ruta']).name}](../{h['ruta']})" if (RAIZ / h["ruta"]).exists() else h["ruta"]
            L.append(f"| `{h['id']}` | {_limpia(h['enunciado'], 130)} | {cifra} | {h['capa']} | {_limpia(h['periodo'], 40)} | {enlace} |\n")
        L.append("\n")
    L.append("## Superadas, retiradas y no publicadas en la 1.0 (no citar)\n\nCada fila indica por qué ya no vale o no se publica y, si existe, la cifra que la sustituye.\n\n"
             "| id | estado | enunciado | sustituida por / motivo |\n|---|---|---|---|\n")
    for h in H:
        if h["estado"] != "vigente":
            L.append(f"| `{h['id']}` | {h['estado']} | {_limpia(h['enunciado'], 110)} | {_limpia((h.get('sustituida_por') or '') + ' ' + (h.get('motivo') or ''), 200)} |\n")
    return "".join(L)


# ---------------------------------------------------------------- preguntas frecuentes
# (pregunta, respuesta con marcadores {id}, ids citados, ruta de la fuente). Las cifras se insertan desde cifras_clave.
FAQ: list[tuple[str, str, list[str], str]] = [
    ("¿Se puede señalar un único factor como el más relevante en la subida del precio?",
     "No. La regla pre-registrada de V8 no designa ningún factor en ninguno de los diez casos (mercado por periodo). En la compra de 2022 en adelante, el máximo de métodos que coinciden es {V8-VOTOS-c-P5} de cuatro.",
     ["V8-REGLA-c-P5", "V8-VOTOS-c-P5"], "docs/v8/cierre_proyecto.md"),
    ("¿Cuánto de la subida reciente de la compra es común a todas las comunidades?",
     "En 2022T3-último dato el primer componente común explica {V8-M1-cuota-c-P5} de la varianza del crecimiento interanual del precio real entre las 17 comunidades. Es la mayor cuota de los cinco periodos (C4, asociación).",
     ["V8-M1-cuota-c-P5"], "output/v8/M1/resumen.md"),
    ("¿Y en el alquiler, en el mismo periodo?",
     "El componente común explica {V8-M1-cuota-a-P5} de la varianza del crecimiento interanual del alquiler real entre comunidades en 2022T3-último dato. Describe comovimiento territorial, no causa.",
     ["V8-M1-cuota-a-P5"], "output/v8/M1/resumen.md"),
    ("¿Y durante la crisis de 2008-2013, en la compra?",
     "La cuota del factor común fue {V8-M1-cuota-c-P2} en P2 (2008T3-2013T4), la más baja junto con P4. La subida reciente es más común entre comunidades que la de la crisis.",
     ["V8-M1-cuota-c-P2"], "output/v8/M1/resumen.md"),
    ("¿Es el factor común más de la mitad de la variación en cada periodo (H8-8)?",
     "No se sostiene. La cuota mínima entre periodos es {V8-H8-8-est} y el p ajustado por Holm es {V8-H8-8-pholm}. H8-8 exigía más de la mitad en todos los periodos.",
     ["V8-H8-8-est", "V8-H8-8-pholm"], "docs/v8/cierre_proyecto.md"),
    ("¿El precio de la vivienda en España acompaña al de la zona euro?",
     "Hay asociación: la correlación del factor común español con el precio de la zona euro es {V8-H8-9-est} (p de Holm {V8-H8-9-pholm}). Es la única hipótesis confirmatoria de V8 que se sostiene; es C4, sin lectura causal.",
     ["V8-H8-9-est", "V8-H8-9-pholm"], "docs/v8/cierre_proyecto.md"),
    ("¿Qué parte del precio de compra en la crisis se asocia al precio europeo?",
     "En P2 la parte asociada al precio de la vivienda de la zona euro es {V8-M1-eur-c-P2}. La banda excluye el cero en la crisis; en P3-P5 la incluye. Es asociación (C4).",
     ["V8-M1-eur-c-P2"], "output/v8/M1/resumen.md"),
    ("¿Cuánto varió el precio real de compra en 2022T3-último dato?",
     "La variación observada en P5 es {V8-OBS-c-P5} (log por 100, unidad común del SVAR). Es un dato observado; las contribuciones por factor llevan siempre banda.",
     ["V8-OBS-c-P5"], "output/v8/por_que_ha_subido.md"),
    ("¿Y el alquiler real en el mismo periodo?",
     "La variación observada del alquiler real en P5 es {V8-OBS-a-P5}. El alquiler y la compra no se mueven igual en este periodo, por eso se analizan por separado.",
     ["V8-OBS-a-P5"], "output/v8/por_que_ha_subido.md"),
    ("¿Qué aportan el crédito y los tipos a la subida reciente de la compra?",
     "En P5 la contribución media del SVAR es {V8-SVAR-c-P5-credito_tipos-media}. La banda del 68 % incluye el cero, así que no se distingue de cero. Vale solo condicionado a las restricciones de signo y de cero (C3s).",
     ["V8-SVAR-c-P5-credito_tipos-media"], "output/v8/M2/resumen.md"),
    ("¿Frenó la subida de tipos el precio de compra (H8-2)?",
     "No está respaldado. La estimación de H8-2 es {V8-H8-2-est} y el p de Holm es {V8-H8-2-pholm}. El intervalo incluye valores positivos y negativos (C3s, condicionado a las restricciones).",
     ["V8-H8-2-est", "V8-H8-2-pholm"], "output/v8/F5/fichas.md"),
    ("¿Qué aportan la actividad y la renta a la compra en P5?",
     "La media posterior de su contribución es {V8-SVAR-c-P5-empleo_renta-media}, con banda del 68 % que incluye el cero. Es el factor con mayor media en la compra de P5, pero la regla no lo designa (C3s).",
     ["V8-SVAR-c-P5-empleo_renta-media"], "output/v8/M2/resumen.md"),
    ("¿Explica la demografía la evolución del alquiler reciente?",
     "En P5 la contribución media del SVAR es {V8-SVAR-a-P5-demografia-media}, con banda que incluye el cero. H8-1 tiene p de Holm {V8-H8-1-pholm}: no respaldada (C3s, condicionado a las restricciones).",
     ["V8-SVAR-a-P5-demografia-media", "V8-H8-1-pholm"], "output/v8/M2/resumen.md"),
    ("¿Qué papel tiene la oferta en el alquiler de P5?",
     "La contribución media de la oferta es {V8-SVAR-a-P5-oferta-media}, con banda que incluye el cero. No permite designar la oferta como factor del alquiler en ese periodo (C3s).",
     ["V8-SVAR-a-P5-oferta-media"], "output/v8/M2/resumen.md"),
    ("¿Cuánto de la variación de la compra queda sin atribuir a ningún factor?",
     "La cuota no atribuida (parte determinista y no identificada) en P5 es {V8-QNA-c-P5} de la variación. Una atribución sin esta parte sería incompleta; por eso se publica con bandas.",
     ["V8-QNA-c-P5"], "output/v8/por_que_ha_subido.md"),
    ("¿Y la parte no atribuida del alquiler?",
     "En P5 la cuota no atribuida del alquiler real es {V8-QNA-a-P5} de la variación observada: casi toda. Leer siempre con su banda.",
     ["V8-QNA-a-P5"], "output/v8/por_que_ha_subido.md"),
    ("¿Qué probabilidad hay de que crédito y tipos sea el factor de mayor contribución en la compra de P5?",
     "La probabilidad posterior de que sea el factor de mayor contribución es {V8-PFSTAR-c-P5}. Es una probabilidad dentro del modelo y de sus restricciones, no una prueba de causa (C4).",
     ["V8-PFSTAR-c-P5"], "output/v8/F5/fichas.md"),
    ("¿Algún instrumento externo permite una lectura causal?",
     "No. Los instrumentos de M5 que cumplen las condiciones de C3 son {V8-M5-c3}. Los tres tienen primera etapa débil, por lo que no hay lectura causal externa.",
     ["V8-M5-c3"], "output/v8/M5/resumen.md"),
    ("¿Es fuerte el instrumento de los shocks monetarios del BCE sobre la compra?",
     "No. El F efectivo de la primera etapa es {V8-H8-5-F}, frente a un umbral de 10. H8-5 queda sin respaldo y sin lectura causal (C4).",
     ["V8-H8-5-F"], "output/v8/M5/resumen.md"),
    ("¿Y para el alquiler?",
     "El F efectivo del instrumento monetario sobre el alquiler (H8-6) es {V8-H8-6-F}, muy por debajo de 10. No supera las condiciones de C3.",
     ["V8-H8-6-F"], "output/v8/M5/resumen.md"),
    ("¿Es válido el instrumento de empuje migratorio?",
     "No. El F efectivo de H8-7 es {V8-H8-7-F}, con solo 20 observaciones anuales. No permite estimar el efecto de la inmigración sobre el alquiler.",
     ["V8-H8-7-F"], "output/v8/M5/resumen.md"),
    ("¿Hay una relación estable de largo plazo entre precio y fundamentales?",
     "No se demuestra. De {V8-M4-ardl-total} probadas, el ARDL con cotas rechaza la ausencia de cointegración solo en {V8-M4-ardl-rechaza}. Por eso la contabilidad de largo plazo no vota en la designación de factores.",
     ["V8-M4-ardl-total", "V8-M4-ardl-rechaza"], "output/v8/M4/resumen.md"),
    ("¿Cuántos modelos del multiverso cumplen la regla de robustez?",
     "De {V8-M7-combinaciones} evaluadas, cumplen la regla {V8-M7-cumplen}, ambas de demografía en el alquiler (P2 y muestra completa). Es asociación (C4) y la regla de periodo no se cumple a la vez.",
     ["V8-M7-combinaciones", "V8-M7-cumplen"], "output/v8/M7/resumen.md"),
    ("¿Cuántas especificaciones se exploraron en el multiverso?",
     "La rejilla tiene {V8-M7-rejilla} y se ajustaron con éxito {V8-M7-ajustadas}. El tope del pre-registro es 50.000. Las fallidas constan en el registro del módulo.",
     ["V8-M7-rejilla", "V8-M7-ajustadas"], "output/v8/M7/resumen.md"),
    ("¿Sobreviven los efectos por periodo al control de falsos descubrimientos?",
     "Tras BH (q = 0,10) hay {V8-M0-bh}, pero {V8-M0-cumplen} cumplen la regla de periodo y ninguno de ellos sobrevive a BH. Resultado exploratorio (C4).",
     ["V8-M0-bh", "V8-M0-cumplen"], "output/v8/M0/resumen.md"),
    ("¿Mejora algún modelo la predicción de un AR(4) en el precio de compra?",
     "No. El RMSE fuera de muestra del AR(4) es {V8-OOS-c-ar4-rmse}; el del ECM v1 es {V8-OOS-c-ecm_v1-rmse}. Ningún modelo lo supera en la misma muestra.",
     ["V8-OOS-c-ar4-rmse", "V8-OOS-c-ecm_v1-rmse"], "output/v8/F5/fichas.md"),
    ("¿Y en el alquiler?",
     "El AR(4) tiene RMSE fuera de muestra de {V8-OOS-a-ar4-rmse}; el BVAR de M2, {V8-OOS-a-bvar_m2-rmse}. Ninguno mejora al AR(4).",
     ["V8-OOS-a-ar4-rmse", "V8-OOS-a-bvar_m2-rmse"], "output/v8/F5/fichas.md"),
    ("¿Supera el aprendizaje automático a la línea base en V8?",
     "No. Los modelos de M9 que superan al AR(4) tras BH en la compra nacional son {V8-M9-oos-c-nacional-mejor}. Su mejor modelo tiene RMSE {V8-M9-oos-c-nacional-ml}, frente a {V8-M9-oos-c-nacional-base} de la base.",
     ["V8-M9-oos-c-nacional-mejor", "V8-M9-oos-c-nacional-ml", "V8-M9-oos-c-nacional-base"], "output/v8/M9/resumen.md"),
    ("¿Qué coeficiente asocia el tipo hipotecario con el alquiler en el panel de CCAA?",
     "El coeficiente DML es {V8-M9-dml-a-tipo}. Es una asociación sin identificación (C4) y no debe leerse como efecto. Las importancias y el SHAP tampoco son causas.",
     ["V8-M9-dml-a-tipo"], "output/v8/M9/resumen.md"),
    ("¿Qué mide el SHAP o la dominancia LMG: causa o predicción?",
     "Miden contribución a la predicción o al ajuste, no causa. En V8 el coeficiente DML del tipo sobre la compra es {V8-M9-dml-c-tipo} y se reporta como asociación (C4).",
     ["V8-M9-dml-c-tipo"], "output/v8/M9/resumen.md"),
    ("¿Cuál es el déficit de vivienda acumulado en 2021-2024?",
     "Sin bajas del parque, la cifra de referencia y el rango entre variantes son {L3-DEF-2124-SINBAJAS}. Es una cota (C2): la dirección positiva se mantiene en todas las variantes, la amplitud no permite una cifra única.",
     ["L3-DEF-2124-SINBAJAS"], "output/v6_2/L3/deficit_alternativas.md"),
    ("¿Y con las bajas estimadas del parque?",
     "Con las bajas estimadas en v5.1 el déficit 2021-2024 es {L3-DEF-2124-BAJAST1} (todas las variantes). Es C4: depende de una estimación de bajas.",
     ["L3-DEF-2124-BAJAST1"], "output/v6_2/L3/deficit_alternativas.md"),
    ("¿Cuál es el déficit acumulado 2021-2025?",
     "Sin bajas, el rango de todas las variantes es {L3-DEF-2125}. Es C4 (contabilidad con correcciones de la EPA). Debe citarse con rango, no con un valor único.",
     ["L3-DEF-2125"], "output/v6_2/L3/deficit_alternativas.md"),
    ("¿Cuántas viviendas hacen falta cada año de 2026 a 2035?",
     "La necesidad anual recalculada es {T3-H5b} sin la sensibilidad X y {T3-H5} con ella (cifra de referencia y rango entre escenarios). Es C4, no una cifra puntual.",
     ["T3-H5b", "T3-H5"], "output/v5_1/T3"),
    ("¿Se restan de la necesidad las viviendas liberadas por envejecimiento?",
     "No, nunca. La proyección de hogares del INE ya las descuenta. Se estiman {T2-H2} liberadas; frente a la necesidad central equivalen a {T2-H15}, pero no se restan.",
     ["T2-H2", "T2-H15"], "output/v5_1/T2"),
    ("¿Cuál será el déficit acumulado a fin de 2030?",
     "En la rejilla de v5.1 el déficit a fin de 2030 es {T4-H1} (mínimo, central y máximo). Es una proyección condicional (C4); no una predicción.",
     ["T4-H1"], "output/v5_1/T4"),
    ("¿Empeora el déficit entre 2025 y 2030?",
     "En toda la rejilla de v5.1 la dirección nacional es que empeora (C2), con un cambio de {T4-H2}. La magnitud es C4. Hay provincias con dirección indeterminada.",
     ["T4-H2"], "output/v5_1/T4"),
    ("¿Cuántas viviendas al año habría que terminar para no aumentar el déficit?",
     "Para mantener constante el déficit 2026-2030 hacen falta {T4-H6}. Es un cálculo condicional a hogares INE central y bajas de T1 (C4).",
     ["T4-H6"], "output/v5_1/T4"),
    ("¿Cuántas veces cabe la producción actual en la necesidad?",
     "La necesidad equivale a {T3-H9} la producción reciente (terminadas 2019-2024), según el cálculo de v5.1. Depende de los escenarios de necesidad y es C4.",
     ["T3-H9"], "output/v5_1/T3"),
    ("¿Cuántos hogares se crearon en 2021-2025?",
     "El aumento de hogares fue {dh_2125}, hecho C1 (al menos dos fuentes coinciden dentro de la tolerancia declarada).",
     ["dh_2125"], "output/v4/M2"),
    ("¿Cuántas viviendas se terminan al año?",
     "En el territorio común (sin País Vasco ni Navarra), las terminadas de 2019-2024 van de {terminadas_1924}, hecho C1 (rango entre fuentes). Sirve de referencia para la oferta reciente.",
     ["terminadas_1924"], "output/v4/M0"),
    ("¿Cuántas viviendas vacías hay que se pudieran movilizar?",
     "Se estiman {B1-H6} movilizables en zonas con presión en 10 años (10-30 % de las vacías); es C4. El Censo 2021 da una mediana municipal de vacías de {R1C-021}.",
     ["B1-H6", "R1C-021"], "output/v5/B1"),
    ("¿Qué peso tienen los compradores extranjeros?",
     "En 2025 el {compradores_extranjeros} de las compraventas tiene comprador extranjero (residente o no) y los no residentes son {compradores_no_residentes}. Es dato descriptivo (C4, una fuente).",
     ["compradores_extranjeros", "compradores_no_residentes"], "output/v4/M4"),
    ("¿Compran las personas jurídicas muchas viviendas?",
     "En 2024 las compraventas con comprador persona jurídica son {R1C-004}. Es descriptivo (C4) y no distingue el uso posterior de la vivienda.",
     ["R1C-004"], "output/v5/R1C"),
    ("¿Cuántos hogares viven en propiedad?",
     "Tienen la vivienda principal en propiedad {R1C-001}; es C1 (dos fuentes, 2021-2022). La mayoría de las compras no pasa por el mercado de alquiler.",
     ["R1C-001"], "output/v5/R1C"),
    ("¿Ha subido el coste de construcción más que el precio?",
     "Entre 2014T1 y 2025T4, el coste de construcción menos el precio de tasación varió {R1C-013}. Es una diferencia de variaciones (C4), no un margen de beneficio.",
     ["R1C-013"], "output/v5/R1C"),
    ("¿Cuántos lanzamientos por impago de alquiler hay?",
     "Los lanzamientos practicados por la LAU, principalmente por alquiler impagado, son {CB-C5-01}. Es una estadística de fuente única (C4) y no dice cuántos hogares afectados siguen en la vivienda.",
     ["CB-C5-01"], "output/v5/CB"),
    ("¿Cuánta vivienda protegida se califica al año?",
     "La media anual de calificaciones definitivas de vivienda protegida es {CC-C2-nuevas5a}. Es fuente única (C4); la oferta protegida es pequeña frente a la necesidad anual.",
     ["CC-C2-nuevas5a"], "output/v5/CC"),
    ("¿Cuántos instrumentos de política se han evaluado y con qué resultado?",
     "Se evaluaron {D1-H01} con una rúbrica; en {D1-H02} el signo no es evaluable. Se evalúan instrumentos, no partidos ni personas, y siempre como escenario condicional (C4).",
     ["D1-H01", "D1-H02"], "output/v5/D1"),
    ("¿Qué parte de una ayuda a la demanda se traslada al precio?",
     "En provincias de clase A4 1, el método A da {D1-H11} en la rejilla de elasticidad 0,3-1,5. Es una simulación con parámetros supuestos (C4), no un efecto medido.",
     ["D1-H11"], "output/v5/D1"),
    ("¿Cuánto bajaría el precio de compra con 10.000 viviendas más de construcción?",
     "En la simulación condicional de V7.1, la variación del precio por cada 10.000 viviendas es {V71-S1-a_construccion-compra-efecto_10k} (mediana entre CCAA). Es C4 y el signo lo fija en parte la fórmula; lo informativo es la magnitud relativa.",
     ["V71-S1-a_construccion-compra-efecto_10k"], "metodologia/dosis_coste.md"),
    ("¿Y movilizando vacías, en el alquiler?",
     "La simulación da {V71-S1-b_vacias-alquiler-efecto_10k} por cada 10.000 viviendas, con la dosis y el coste declarados. Es un escenario condicional (C4), no una previsión.",
     ["V71-S1-b_vacias-alquiler-efecto_10k"], "metodologia/dosis_coste.md"),
    ("¿Qué efecto tendría regular los alquileres turísticos?",
     "En la simulación de V7.1 la regulación local de turísticos da {V71-S1-d_turisticos-alquiler-efecto_10k} en el alquiler por cada 10.000 viviendas. Es un escenario con parámetros supuestos (C4); no se mide un efecto.",
     ["V71-S1-d_turisticos-alquiler-efecto_10k"], "metodologia/dosis_coste.md"),
    ("¿Cuánto cuestan las ayudas a la demanda?",
     "El coste fiscal anual aproximado de la simulación es {V71-S1-e_ayuda_demanda-compra-coste_anual_meur} (mediana entre CCAA). Se compara por dosis y coste, no por ideología del instrumento.",
     ["V71-S1-e_ayuda_demanda-compra-coste_anual_meur"], "metodologia/dosis_coste.md"),
    ("¿En cuántas comunidades es robusta la movilización de vacías en alquiler?",
     "En la simulación, es robusta en {V71-S3-R6-b_vacias-alquiler-robustas}. Robusta significa que el esfuerzo baja en todas las extracciones del escenario; es C4, condicionado a los supuestos.",
     ["V71-S3-R6-b_vacias-alquiler-robustas"], "metodologia/dosis_coste.md"),
    ("¿Hay burbuja en el precio nacional?",
     "El GSADF no encuentra exuberancia en los cocientes precio/renta y precio/alquiler tras BH: {V72-GSADF-ratios-bh}. Sí en {V72-GSADF-niveles-bh} de niveles, que no controlan fundamentales (C4).",
     ["V72-GSADF-ratios-bh", "V72-GSADF-niveles-bh"], "output/v7_2/gsadf/ficha_burbuja.md"),
    ("¿Y en las comunidades autónomas?",
     "Tras BH hay exuberancia en {V72-GSADF-ccaa-bh} regionales (17 CCAA); en las provincias de entrenamiento de v6, en {V72-GSADF-ccaa-v6}. Es exploratorio (C4): detecta aceleración, no sobrevaloración.",
     ["V72-GSADF-ccaa-bh", "V72-GSADF-ccaa-v6"], "output/v7_2/gsadf/ficha_burbuja.md"),
    ("¿Se confirma que empleo y población determinan el alquiler a largo plazo en las CCAA?",
     "No. Ninguna de las hipótesis de largo plazo del atlas regional se confirma tras Holm. La velocidad de ajuste media del alquiler es {V7-R4-PHI-ALQUILER-A}, sin intervalo válido (C4, diferido).",
     ["V7-R4-PHI-ALQUILER-A"], "output/v7/R4"),
    ("¿Qué rentabilidad bruta da el alquiler?",
     "La mediana provincial de la rentabilidad bruta (alquiler sobre valor tasado) es {m1b_rentabilidad_bruta_mediana}, y el ratio precio/alquiler, {m1b_ratio_precio_alquiler_mediana}. Descriptivo (C4).",
     ["m1b_rentabilidad_bruta_mediana", "m1b_ratio_precio_alquiler_mediana"], "output/v6/M1B"),
    ("¿Cuál es el coste de uso de comprar?",
     "El coste de uso anual (tipo hipotecario más 2,0 % de depreciación y mantenimiento) es {m1b_coste_uso_g2}. La brecha con la rentabilidad bruta es {m1b_brecha_rentabilidad_coste_uso}. Descriptivo (C4).",
     ["m1b_coste_uso_g2", "m1b_brecha_rentabilidad_coste_uso"], "output/v6/M1B"),
    ("¿Se asocia la población extranjera con el alquiler en las provincias?",
     "En el modelo provincial S0, +1 punto de población extranjera se asocia con {m1a_provincia_S0_share_ext_pob} en el alquiler de stock; en S1 es {m1a_provincia_S1_share_ext_pob}. El signo y la magnitud dependen de la especificación (C4).",
     ["m1a_provincia_S0_share_ext_pob", "m1a_provincia_S1_share_ext_pob"], "output/v6/M1A"),
    ("¿Se asocian las viviendas turísticas con el alquiler?",
     "En provincias, +1.000 viviendas turísticas se asocian con {m1a_provincia_S0_ln_vut} en el alquiler de stock; ningún intervalo al 95 % excluye el cero. No concluyente (C4).",
     ["m1a_provincia_S0_ln_vut"], "output/v6/M1A"),
    ("¿Bajaron el alquiler los topes de precios catalanes?",
     "Los resultados cambian de signo según la especificación: {m1a_municipio_S0_tope_cat_mun} en S0 y {m1a_municipio_S1_tope_cat_mun} en S1. No concluyente (C4); las pretendencias fallan.",
     ["m1a_municipio_S0_tope_cat_mun", "m1a_municipio_S1_tope_cat_mun"], "output/v6/M1A"),
    ("¿Hay modelos de predicción que mejoren a la línea base más exigente en datos sellados?",
     "En la validación sellada de v6 (K1), el mejor modelo predice mejor que la base más exigente en {K1-N-MEJOR} (de {K1-N-TAREAS} comparadas). Solo cuenta como «predice mejor» si supera a la base más exigente.",
     ["K1-N-MEJOR", "K1-N-TAREAS"], "output/v6_1/K1"),
    ("¿Hay variables relevantes con seguridad en la predicción provincial de v6?",
     "No: son {V6-M4-N-REL} según los criterios pre-registrados A y B, en alquiler y compra. Es predicción y asociación, no causa (C4).",
     ["V6-M4-N-REL"], "output/v6/M4"),
    ("¿Cuál es la probabilidad de inclusión de la población en el precio de compra provincial?",
     "El BMA da una probabilidad de inclusión posterior de {m2_pip_cp_ln_pob} para la población. Una probabilidad alta no implica signo positivo ni causa (C4).",
     ["m2_pip_cp_ln_pob"], "output/v6/M2"),
    ("¿Cuántas viviendas turísticas hay según el registro valenciano frente al INE?",
     "El cociente entre el registro vigente de la Generalitat Valenciana y el INE es {R1A-H7}. La discrepancia indica que las fuentes miden cosas distintas (C4).",
     ["R1A-H7"], "output/v5/R1A"),
    ("¿Cuántas referencias de organismos coinciden con las cifras del proyecto?",
     "Referencias que coinciden: {D3-coincide}; que difieren: {D3-difiere}. El resto no es comparable o lo es en parte. La comparación es descriptiva (C4).",
     ["D3-coincide", "D3-difiere"], "output/v5/D3"),
    ("¿Cuánto rotan los contratos en Cataluña?",
     "La rotación (fianzas Incasòl sobre contratos vigentes SERPAVI) es {A23-A11}. Es C4: combina dos fuentes con medidas distintas (contratos nuevos y stock).",
     ["A23-A11"], "output/v5/A23"),
    ("¿Cuánto crédito hay en construcción e inmobiliarias?",
     "El saldo de crédito a construcción y actividades inmobiliarias es {CA-CR-saldo-2025}. Es una estadística oficial de fuente única (C4).",
     ["CA-CR-saldo-2025"], "output/v5/CA"),
    ("¿Cuál fue el atraso a absorber en diez años?",
     "El atraso (déficit 2021-2025 más emancipación retrasada) es {B1-H2}. Es C4 y no se suma a la necesidad anual sin declarar el escenario.",
     ["B1-H2"], "output/v5/B1"),
    ("¿Cuántas viviendas libres de baja se han estimado por demolición?",
     "Con licencias de demolición, la tasa anual de bajas es {T1-H8} (media 2015-2024). Es una estimación (C4) y la identidad de censos da una tasa distinta.",
     ["T1-H8"], "output/v5_1/T1"),
]


def _cita(i: str, cifras: dict[str, dict]) -> str:
    r = cifras[i]
    fecha = re.split(r";|\(", r["fecha_dato"])[0].strip()
    ruta = _ruta_fichero(r["origen"])
    enlace = f" Origen: [{Path(ruta).name}](../{ruta})." if (RAIZ / ruta).exists() else ""
    return f"- `{i}` = {valor_texto(r)}; capa {r['capa']}; periodo {_limpia(r['periodo'], 50)}; dato {fecha}.{enlace}"


def faq_md(cifras: dict[str, dict]) -> str:
    L = [CAB_MD, "# Preguntas frecuentes\n\n",
         "Respuestas breves a las preguntas más habituales. Cada cifra se lee de `output/v5/cifras_clave.csv` por su id, con su capa y su fecha; "
         "el enlace lleva a la fuente. Capas: [glosario](glosario.md). Reglas para responder: [LEEME_ASISTENTE.md](LEEME_ASISTENTE.md).\n\n"]
    for n, (q, resp, ids, ruta) in enumerate(FAQ, 1):
        for i in ids:
            assert i in cifras, f"FAQ {n}: id inexistente en cifras_clave: {i}"
        assert (RAIZ / ruta).exists(), f"FAQ {n}: ruta inexistente {ruta}"
        txt = re.sub(r"\{([^}]+)\}", lambda m: valor_texto(cifras[m.group(1)]), resp)
        assert len(txt.split()) <= 60, f"FAQ {n} supera 60 palabras ({len(txt.split())})"
        L.append(f"### {n}. {q}\n\n{txt}\n\n")
        L.extend(_cita(i, cifras) + "\n" for i in ids)
        L.append(f"- Fuente: [{ruta}](../{ruta})\n\n")
    return "".join(L)


# ---------------------------------------------------------------- LEEME para asistentes
MAPA: list[tuple[str, str]] = [
    ("Por qué ha subido el precio o el alquiler; qué factor pesa más", "output/v8/por_que_ha_subido.md"),
    ("Qué responde V8 y qué no pudo hacerse", "docs/v8/cierre_proyecto.md"),
    ("Contribución de cada factor por periodo (SVAR, descomposición histórica)", "output/v8/M2/resumen.md"),
    ("Fichas de atribución y regla de designación del factor", "output/v8/F5/fichas.md"),
    ("Factor común entre comunidades y relación con la zona euro", "output/v8/M1/resumen.md"),
    ("Periodos detectados y efectos por periodo", "output/v8/M0/resumen.md"),
    ("Relación de largo plazo, cointegración, contabilidad hogares-viviendas", "output/v8/M4/resumen.md"),
    ("Instrumentos externos (LP-IV, Anderson-Rubin, F efectivo)", "output/v8/M5/resumen.md"),
    ("Colinealidad y dominancia entre factores", "output/v8/M6/resumen.md"),
    ("Multiverso de especificaciones", "output/v8/M7/resumen.md"),
    ("Descomposición regional (CCAA)", "output/v8/M8/resumen.md"),
    ("Predicción, aprendizaje automático, SHAP", "output/v8/M9/resumen.md"),
    ("Predicciones congeladas y evaluación diferida de V8", "docs/v8/evaluate_v8_accesos.md"),
    ("Evaluar una afirmación del debate público", "publicacion/verificador/verificador_v8.md"),
    ("Fichas de afirmaciones en formato máquina", "publicacion/verificador/fichas_v8.json"),
    ("Verificador de afirmaciones de v5 y fichas de V7.1", "publicacion/verificador/verificador.md"),
    ("Déficit de vivienda y necesidad 2026-2035", "publicacion/lo_que_sabemos.md"),
    ("Informe técnico con déficit, necesidad y oferta", "publicacion/informe_tecnico.md"),
    ("Resumen en una página", "publicacion/una_pagina.md"),
    ("Qué cambió entre versiones", "publicacion/que_cambio.md"),
    ("Simulaciones de instrumentos, dosis y coste", "metodologia/dosis_coste.md"),
    ("Atlas regional por comunidad autónoma", "publicacion/atlas_regional/atlas_resumen.md"),
    ("Burbuja y exuberancia (GSADF)", "output/v7_2/gsadf/ficha_burbuja.md"),
    ("Paneles regionales de largo plazo", "output/v7/R4"),
    ("Compradores extranjeros y no residentes", "output/v5/R1A"),
    ("Turismo y alquiler; topes de precios en provincias", "output/v6/M1A"),
    ("Vivienda protegida y política de suelo", "output/v5/CC"),
    ("Instrumentos de política evaluados con rúbrica", "output/v5/D1"),
    ("Validación sellada y predicción provincial", "output/v6_1/K1"),
    ("Qué significa cada capa y cómo se redacta", "metodologia/capas.md"),
    ("Conclusiones por versión y su estado actual", "metodologia/historial_conclusiones.md"),
    ("Cómo se calcula una cifra del anexo", "metodologia/anexo_metodologico.md"),
    ("Pre-registro de V8 y desviaciones", "metodologia/preregistro_v8.md"),
    ("Cómo reproducir los resultados", "reproducir/instrucciones.md"),
    ("Errores corregidos tras publicar", "ERRATA.md"),
    ("Cómo citar y licencias", "CITATION.cff"),
    ("Referencias bibliográficas y estado de verificación", "docs/literatura.md"),
    ("Pendientes del autor (DOI, etiquetas, revisión humana)", "docs/v14/tareas_autor.md"),
    ("Cualquier cifra concreta (id, valor, capa, fecha)", "output/v5/cifras_clave.csv"),
    ("Quién soporta el coste y dónde (atlas)", "publicacion/atlas_descriptivo.md"),
    ("La base de datos única", "docs/v10/diccionario_base.md"),
    ("Figuras y mapas", "figuras/README.md"),
    ("Web y monitor", "web/README.md"),
]


def leeme_md(cifras: dict[str, dict], version: dict) -> str:
    for _, ruta in MAPA:
        assert (RAIZ / ruta).exists(), f"MAPA: ruta inexistente {ruta}"
    ejemplo = "V8-M5-c3"
    fecha = re.split(r";|\(", cifras[ejemplo]["fecha_dato"])[0].strip()
    cita = f"`{ejemplo}` = {valor_texto(cifras[ejemplo])}; capa {cifras[ejemplo]['capa']}; dato {fecha}"
    mapa = "\n".join(f"- Si te preguntan por **{x}**, mira [{y}](../{y})." for x, y in MAPA)
    return f"""{CAB_MD}# Guía para asistentes: cómo usar este repositorio

Estás ante una base de evidencia sobre la vivienda en España. Autor: Borja Romero, economista (firma individual, independiente). Esta guía resume qué es vigente, cómo leer las capas y qué reglas seguir al responder. Léela entera antes de contestar; es corta.

## 1. Versión vigente

- Versión pública: **{version['version']}** ({version['fecha_version']}). Reúne las versiones internas de desarrollo v1 a V12 (correspondencia en CHANGELOG.md). Metadatos en [version.json](version.json). Para cada tema vale una versión interna:
- **V8** (redacción y tablas de v8.1) para la modelización: por qué ha subido la vivienda, factores, periodos y factor común (SVAR, factor común, instrumentos, multiverso, predicción).
- **V9** para qué causa qué: diseños pre-registrados; ninguno alcanza C3 ni C3s.
- **V10** (sin modelos nuevos): base única, atlas descriptivo (ids `V10-ATL-*`), figuras, web y monitor; los datos desde 2026T3 no se contrastan con predicciones.
- **V12** (descriptivo, datos de V11): demografía, hogares, titularidad, oferta, condiciones por origen y turismo (ids `V12-*`).
- **v7.1 y v7.2** para el **déficit y la necesidad de vivienda**, las simulaciones de instrumentos (dosis y coste) y el atlas regional. v5 a v6.3 siguen vigentes en lo que no han sido superadas.
- Repositorio: {version['repositorio']}. DOI: {version['doi']}. Fecha verificable del pre-registro: {version['fecha_verificable']} (también en [version.json](version.json)).
- Una cifra **superada** no se cita nunca: las lista [output/v5/cifras_superadas.csv](../output/v5/cifras_superadas.csv) con su sustituta. El registro completo está en [hallazgos.md](hallazgos.md) y [hallazgos.json](hallazgos.json) (campo `estado`: vigente, superada o retirada).

## 2. Capas de evidencia y cómo citarlas

| Capa | Qué es | Cómo se redacta |
|---|---|---|
| C1 | Hecho: al menos dos fuentes que coinciden en la tolerancia declarada | «es», «fue»; rango entre fuentes |
| C2 | Cota con supuestos explícitos, o dirección estable en una rejilla de escenarios | «como máximo», «en todos los escenarios de la rejilla» |
| C3 | Efecto identificado (instrumento externo o diseño que supera las pruebas) | lenguaje causal permitido; ningún resultado del proyecto la alcanza |
| C3s | Descomposición del SVAR con restricciones de signo y de cero explícitas | siempre «condicionado a las restricciones de signo y de cero»; con banda |
| C4 | Exploratorio: asociación, contabilidad, proyección, predicción, simulación | «se asocia», «en la simulación»; sin lenguaje causal |

La capa de un resultado es la menor de las de sus componentes; **nunca se promueve de capa**. Escala de evidencia: CAUSAL > ASOCIACIÓN ROBUSTA > EXPLORATORIO > DESCRIPTIVO. Cita cada cifra así: «valor (id; capa; periodo; fecha del dato)». Ejemplo: {cita}.

## 3. Reglas para responder

1. **Solo cifras de `output/v5/cifras_clave.csv`**, con su id y la fecha del dato. Si no está allí, no es una cifra del proyecto: dilo. Nunca cites una cifra superada.
2. **Sin causalidad fuera de C3 y C3s.** Nada causal desde SHAP, importancias, dominancia (LMG) ni coeficientes de aprendizaje automático. Predecir no es explicar. Los resultados C3s valen solo bajo las restricciones del modelo.
3. **Atribuciones siempre con banda** (68 % en el SVAR; 95 % donde se indique). Si la banda incluye el cero, no digas que el factor «explica» nada.
4. **Di «no concluyente» cuando lo sea.** Es el resultado más frecuente de V8: ninguna regla designa un factor único. Un veredicto «ANALIZADA, NO CONCLUYENTE» no es una evasiva, es el resultado.
5. **Neutralidad.** Se evalúan afirmaciones e instrumentos, nunca partidos ni personas; sin lenguaje valorativo. Si te piden juzgar a quien dice algo, evalúa la afirmación con la ficha del verificador y nada más. Los programas electorales y la divulgación quedan fuera de alcance.
6. **Distingue mercados y medidas.** Compra no es alquiler. En el alquiler, el **parque** (stock de contratos vigentes: IPC de alquiler, SERPAVI) no es **contratos nuevos** (fianzas, IPVA); en la compra, el valor tasado no es el precio de escritura ni el IPV. Cada resultado declara su medida de precio; no mezcles medidas.
7. **Distingue unidades.** `pp` son puntos porcentuales (log por 100); las proyecciones de hogares y viviendas son por año o por periodo según el id; no sumes rangos de escenarios distintos.
8. **No inventes ni redondees al alza.** Si una cifra no cuadra con su id, prevalece `cifras_clave`. Si la pregunta requiere un dato que el proyecto no tiene (por ejemplo, un índice nacional trimestral de contratos nuevos), dilo y señala la tarea pendiente en [docs/v8/cierre_proyecto.md](../docs/v8/cierre_proyecto.md).
9. **Las referencias bibliográficas** están VERIFICADAS (DOI y cuartil) o marcadas NO VERIFICADA; respeta la marca.
10. **Ante una discrepancia entre métodos**, reporta ambos (media y mediana, con y sin bajas, MCO y 2SLS).

## 4. Qué sostiene y qué no sostiene la evidencia (V8)

- Sostiene: no hay un factor único designable; la subida reciente es muy común entre comunidades; el precio español acompaña al europeo (asociación, C4); el precio sigue su propia inercia a corto plazo.
- No sostiene: que un único factor explique la subida; que la subida de tipos frenara el precio; que el turismo sea el motor; efectos causales de los instrumentos (los tres son débiles).
- Evaluación diferida: `make evaluate_v7` y `make evaluate_v8` se ejecutan una sola vez, en 2027. No hay validación limpia de V7 ni V8 todavía.

## 5. Si te preguntan X, mira Y

{mapa}

## 6. Cómo se genera esto

Todo `consulta/` y `llms.txt` lo genera `make consulta` (src/consulta/generar.py) desde `output/`, `docs/` y `cifras_clave`; nunca se edita a mano. Las preguntas frecuentes están en [preguntas_frecuentes.md](preguntas_frecuentes.md), los términos en [glosario.md](glosario.md) y el mapa de ficheros en [indice_ficheros.md](indice_ficheros.md).
"""


# ---------------------------------------------------------------- glosario
GLOSARIO: list[tuple[str, str]] = [
    ("Capas (C1, C2, C3, C3s, C4)", "Niveles de evidencia. C1 hechos (dos fuentes o más); C2 cotas con supuestos; C3 efectos identificados (instrumento externo o diseño que supera las pruebas); C3s identificación por restricciones de signo y de cero, válida solo bajo ellas; C4 exploratorio. Nunca se promueve de capa. Véase [capas](../metodologia/capas.md)."),
    ("Escala de evidencia", "CAUSAL > ASOCIACIÓN ROBUSTA > EXPLORATORIO > DESCRIPTIVO. Por debajo de CAUSAL no se usa lenguaje causal."),
    ("SVAR", "Vector autorregresivo estructural. En V8 es bayesiano, de 7 variables, con restricciones de signo y de cero. Separa shocks (actividad y renta, demográfico, crédito y tipos, demanda de vivienda, oferta) y atribuye la variación observada a cada uno."),
    ("Restricciones de signo", "Supuestos sobre el signo de la respuesta de las variables a cada shock (por ejemplo, un shock de oferta baja el precio). Identifican parcialmente el modelo; los resultados valen solo condicionados a ellas (C3s)."),
    ("Restricciones de cero", "Supuestos de que ciertos shocks no afectan a ciertas variables en el impacto. Se combinan con las de signo."),
    ("Descomposición histórica", "Reparto de la variación observada de una serie en un periodo entre las contribuciones acumuladas de cada shock más una parte no atribuida (determinista). Se publica con bandas del 68 %."),
    ("Banda del 68 %", "Percentiles 16-84 de la distribución posterior. Si incluye el cero, la contribución no se distingue de cero. Los ids con sufijo -media y -mediana comparten la misma banda."),
    ("Parte no atribuida", "Componente determinista y no identificado del SVAR (condiciones iniciales y término de deriva). Se publica porque una atribución sin ella sería incompleta."),
    ("LP-IV", "Proyecciones locales con variables instrumentales. Estiman la respuesta a un shock a distintos horizontes usando un instrumento externo; solo valen si el instrumento es fuerte."),
    ("Anderson-Rubin", "Contraste y región de confianza para el coeficiente de una regresión con instrumentos que es válido aunque el instrumento sea débil; por eso se usa cuando el F efectivo es bajo."),
    ("F efectivo", "Estadístico de fuerza del instrumento robusto a heteroscedasticidad y autocorrelación (Montiel Olea y Pflueger). El umbral operativo de C3 es F efectivo mayor o igual que 10."),
    ("Dominancia LMG", "Reparto del R² entre regresores promediando sobre todos los órdenes de entrada (Lindeman, Merenda y Gold). Describe ajuste, no causa."),
    ("Contabilidad hogares-viviendas", "Identidad que descompone el cambio en hogares y viviendas; asociación, no causa. Demografía y oferta no se separan en ella."),
    ("Multiverso", "Conjunto de especificaciones razonables (variables, muestras, retardos, transformaciones) que se ajustan todas; se reporta la distribución de signos y significatividades. En V8 el tope es 50.000 especificaciones."),
    ("BH (Benjamini-Hochberg)", "Control de la tasa de falsos descubrimientos. Se aplica a familias grandes de contrastes (por ejemplo, el multiverso, con q = 0,10)."),
    ("Holm", "Corrección de comparaciones múltiples que controla la tasa de error por familia; se usa en las hipótesis confirmatorias (H8-1 a H8-9)."),
    ("Hipótesis confirmatoria", "Hipótesis pre-registrada con una sola evaluación. De las nueve de V8, solo H8-9 se sostiene tras Holm."),
    ("Pre-registro", "Documento con hipótesis, reglas y análisis fijados antes de ver los resultados. Las desviaciones se registran en docs/v8/desviaciones.md."),
    ("Muestra sellada", "Datos reservados que solo abre src/holdout.py, registrando cada acceso, una vez por hipótesis confirmatoria."),
    ("SHAP", "Reparto aditivo de la predicción de un modelo entre sus variables. Describe la predicción del modelo, no efectos causales."),
    ("DML", "Aprendizaje automático doble (double machine learning): estima un coeficiente tras limpiar controles con modelos flexibles. Sin identificación externa sigue siendo asociación (C4)."),
    ("AR(4) y ECM v1", "Líneas base de predicción: autorregresivo de orden 4 y modelo de corrección del error de la v1. Un modelo solo «predice mejor» si supera a la más exigente en la misma muestra."),
    ("RMSE", "Raíz del error cuadrático medio de predicción. Menor es mejor; solo se compara en la misma muestra."),
    ("Diebold-Mariano", "Contraste de igualdad de precisión predictiva entre dos modelos."),
    ("Cointegración, ARDL con cotas", "Relación de largo plazo estable entre series no estacionarias. El ARDL con cotas contrasta su existencia sin saber si las series son I(0) o I(1)."),
    ("Factor común", "Primer componente principal de las series de las 17 CCAA; su cuota mide cuánto de la variación se mueve a la vez en todo el país. Es comovimiento, no causa."),
    ("GSADF", "Contraste de exuberancia (raíz explosiva) en series de precios. Detecta aceleración, no sobrevaloración."),
    ("Periodos P1-P5", "P1 1995-2007 (versión larga); P2 2008T3-2013T4 (crisis); P3 2014T1-2019T4; P4 2020T2 en adelante (pandemia y tipos); P5 2022T3 hasta el último dato. Detalle en docs/v8/hipotesis.md."),
    ("pp", "Puntos porcentuales. En V8, log por 100 (aproximadamente un porcentaje en variaciones pequeñas)."),
    ("IPC de alquiler vs IPVA", "El IPC de alquiler mide el alquiler del parque (contratos vigentes, con actualizaciones lentas); el IPVA, el de contratos nuevos. Se mueven distinto y no son intercambiables."),
    ("Parque vs contratos nuevos", "El parque es el conjunto de contratos vigentes (stock); los contratos nuevos reflejan el precio de mercado de entrada. Un resultado de uno no vale para el otro."),
    ("Valor tasado", "Precio medio por m² de las tasaciones hipotecarias (Ministerio de Vivienda). Es una medida de precio de compra distinta del IPV del INE y del precio de escritura."),
    ("IPV", "Índice de precios de vivienda del INE."),
    ("SERPAVI", "Sistema estatal de referencia del precio del alquiler de vivienda (Ministerio). Mide el alquiler del parque."),
    ("Dosis y coste", "Cada instrumento simulado declara cuánto se aplica (dosis) y cuánto cuesta. Las simulaciones son escenarios condicionales (C4)."),
    ("Déficit y necesidad", "El déficit acumulado es hogares menos viviendas terminadas (con o sin bajas); la necesidad es el flujo anual 2026-2035 (A+R+V+F-M-K). Las viviendas liberadas por envejecimiento nunca se restan de la necesidad."),
    ("Identificación parcial (Manski)", "Cotas sobre un parámetro cuando los supuestos no bastan para un valor puntual. Fundamento de la capa C2."),
    ("Superada / retirada", "Una cifra superada fue sustituida por otra mejor (consta en cifras_superadas.csv); una hipótesis retirada se publicó con una especificación errónea y se conserva con su motivo."),
    ("Verificador", "Fichas que evalúan una afirmación (no a quien la formula) con magnitud, intervalo, límites y veredicto. Con capa C4 el veredicto es como máximo «ANALIZADA, NO CONCLUYENTE»."),
]


def glosario_md() -> str:
    return CAB_MD + "# Glosario\n\nTérminos del proyecto, en el orden en que suelen aparecer. Las definiciones son operativas y no sustituyen al [anexo metodológico](../metodologia/anexo_metodologico.md).\n\n" + "".join(f"## {t}\n\n{d}\n\n" for t, d in GLOSARIO)


# ---------------------------------------------------------------- índice de ficheros
INDICE: list[tuple[str, list[tuple[str, str]]]] = [
    ("Raíz", [("README.md", "Presentación del proyecto"), ("LEEME_PRIMERO.md", "Itinerarios de lectura por perfil"), ("CLAUDE.md", "Instrucciones de trabajo para los agentes"),
              ("CHANGELOG.md", "Cambios por versión"), ("ERRATA.md", "Errores corregidos tras publicar"), ("CITATION.cff", "Metadatos de cita"),
              ("DECLARACION_IA.md", "Declaración de uso de IA"), ("README_REPLICACION.md", "Paquete de replicación"), ("llms.txt", "Entrada para modelos de lenguaje (generado)"),
              ("Makefile", "Objetivos: all, v7, v8, publicacion, consulta, check")]),
    ("consulta/ (generado por `make consulta`)", [("consulta/LEEME_ASISTENTE.md", "Reglas para asistentes y mapa «si te preguntan X, mira Y»"), ("consulta/hallazgos.json", "Registro de hallazgos legible por máquina"),
              ("consulta/hallazgos.md", "Registro de hallazgos legible por personas"), ("consulta/preguntas_frecuentes.md", "Preguntas frecuentes con cifra, capa y fuente"),
              ("consulta/glosario.md", "Términos"), ("consulta/indice_ficheros.md", "Este mapa"), ("consulta/version.json", "Versión, commit de contenido, DOI y pendientes")]),
    ("publicacion/ (generado por `make publicacion`)", [("publicacion/MANIFIESTO.md", "Fuente y sha256 de cada fichero"), ("publicacion/una_pagina.md", "Resumen en una página"),
              ("publicacion/lo_que_sabemos.md", "Lo que se sabe y lo que no, por capa"), ("publicacion/policy_brief.md", "Nota de políticas"), ("publicacion/informe_tecnico.md", "Informe técnico"),
              ("publicacion/working_paper.md", "Documento de trabajo"), ("publicacion/por_que_ha_subido.md", "V8: por qué ha subido la vivienda"), ("publicacion/informe_econometrico_v8.md", "V8: informe econométrico"),
              ("publicacion/tablas_modelos_destacados.md", "V8: tablas de modelos destacados"), ("publicacion/cifras_clave.csv", "Copia publicada de las cifras clave"),
              ("publicacion/dosis_coste.csv", "Dosis y coste de los instrumentos simulados"), ("publicacion/que_cambio.md", "Qué cambió entre versiones"),
              ("publicacion/verificador/verificador_v8.md", "Fichas del verificador V8"), ("publicacion/verificador/fichas_v8.json", "Fichas V8 en JSON"),
              ("publicacion/verificador/verificador.md", "Verificador de afirmaciones v5"), ("publicacion/atlas_regional/atlas_resumen.md", "Atlas regional: resumen")]),
    ("metodologia/", [("metodologia/capas.md", "Capas de evidencia y escala de lectura"), ("metodologia/anexo_metodologico.md", "Ficha de cada cifra publicable"),
              ("metodologia/guia_revisor.md", "Guía para revisores"), ("metodologia/historial_conclusiones.md", "Conclusiones por versión y su estado"),
              ("metodologia/preregistro_v8.md", "Pre-registro de V8"), ("metodologia/desviaciones_v8.md", "Desviaciones del pre-registro de V8"),
              ("metodologia/validacion_montecarlo.md", "Validación Monte Carlo de las herramientas de panel"), ("metodologia/dosis_coste.md", "Resumen de dosis y coste")]),
    ("reproducir/", [("reproducir/instrucciones.md", "Instrucciones de reproducción"), ("reproducir/tiempos.md", "Tiempos de ejecución"), ("reproducir/evaluacion_2027.md", "Protocolo de la evaluación diferida")]),
    ("output/ (salidas por versión)", [("output/v5/cifras_clave.csv", "Única fuente de cifras difundibles (id, valor, capa, fecha)"), ("output/v5/cifras_superadas.csv", "Cifras superadas y su sustituta"),
              ("output/v8/por_que_ha_subido.md", "V8: ensayo principal"), ("output/v8/informe_econometrico.md", "V8: informe técnico"), ("output/v8/F5/fichas.md", "V8: fichas de atribución y regla de designación"),
              ("output/v8/M0/resumen.md", "V8-M0: periodos y efectos por periodo"), ("output/v8/M1/resumen.md", "V8-M1: factor común"), ("output/v8/M2/resumen.md", "V8-M2: SVAR y descomposición histórica"),
              ("output/v8/M4/resumen.md", "V8-M4: largo plazo y contabilidad"), ("output/v8/M5/resumen.md", "V8-M5: instrumentos externos"), ("output/v8/M6/resumen.md", "V8-M6: colinealidad y dominancia"),
              ("output/v8/M7/resumen.md", "V8-M7: multiverso"), ("output/v8/M8/resumen.md", "V8-M8: nivel regional"), ("output/v8/M9/resumen.md", "V8-M9: aprendizaje automático y predicción"),
              ("output/v8/F6/hechos.json", "V8: hechos que alimentan cifras_clave"), ("output/v8/verificador_v8.md", "Fichas del verificador V8"), ("output/v8/tablas_v8.xlsx", "V8: tablas en formato de revista"),
              ("output/v7_1/S1", "V7.1: dosis y coste"), ("output/v7_2/gsadf", "V7.2: reverificación del GSADF"), ("output/v7", "V7: atlas regional y paneles"), ("output/v6_2", "v6.2: déficit L3 y anexo"),
              ("output/v5_1", "v5.1: bajas, liberadas, necesidad y déficit a 2030"), ("output/v5", "v5: módulos R, A, B, C, D, E")]),
    ("docs/", [("docs/v8/estado.md", "Estado de V8"), ("docs/v8/plan.md", "Plan de V8"), ("docs/v8/decisiones.md", "Decisiones de V8"), ("docs/v8/hipotesis.md", "Hipótesis pre-registradas de V8"),
              ("docs/v8/cierre_proyecto.md", "Cierre: qué responde V8, qué no y qué falta"), ("docs/v8/tareas_autor.md", "Tareas pendientes del autor"), ("docs/v8/notas_release.md", "Notas de la release del pre-registro"),
              ("docs/v8/plantillas/README.md", "Marcadores de las plantillas y ids de V8"), ("docs/v8_1/decisiones.md", "Decisiones de V8.1"), ("docs/v8_1/estado.md", "Estado de V8.1"),
              ("docs/v7_1/capas.md", "Fuente de metodologia/capas.md"), ("docs/MAPA.md", "Mapa del repositorio"), ("docs/literatura.md", "Literatura y estado de verificación"),
              ("docs/estado_proyecto/informe_estado.md", "Inventario v1-v6.2"), ("docs/v5/licencias_datos.md", "Licencias de los datos de terceros")]),
    ("src/", [("src/holdout.py", "Único acceso a data/sealed (registra cada acceso)"), ("src/econ_utils.py", "Utilidades y Registry de especificaciones"), ("src/v8", "Módulos de V8"),
              ("src/v7_1/publicacion.py", "Generador de publicacion/, metodologia/ y reproducir/"), ("src/consulta/generar.py", "Generador de consulta/ y llms.txt"),
              ("src/v5/cifras_clave.py", "Generador de cifras_clave"), ("src/v3/check_texto.py", "Control de léxico, neutralidad y promoción de capa")]),
    ("data/", [("data/raw", "Datos brutos de solo lectura"), ("data/processed", "Paneles construidos por make clean"), ("data/CHECKSUMS.sha256", "Sumas de control de ficheros grandes")]),
    ("V10: base, atlas, figuras, web y paper", [("data/base/publica", "Capa pública de la base única (Parquet; redistribuible)"),
              ("docs/v10/diccionario_base.md", "Diccionario de la base"), ("docs/v10/decisiones.md", "Decisiones de V10"),
              ("output/v10/atlas", "Tablas del atlas descriptivo"), ("publicacion/atlas_descriptivo.md", "Atlas descriptivo (texto)"),
              ("publicacion/tablas_atlas.xlsx", "Tablas del atlas en Excel"), ("figuras/README.md", "Figuras con ficha"),
              ("web/README.md", "Web pública"), ("output/v10/monitor/monitor.csv", "Monitor de últimos datos"),
              ("paper/manuscrito.qmd", "Manuscrito en Quarto")]),
    ("historico/", [("historico/INDICE.md", "Documentos de versiones superadas, por versión")]),
]


def indice_md() -> str:
    L = [CAB_MD, "# Índice de ficheros\n\nMapa de carpetas y ficheros clave, con una línea por fichero. Los enlaces son relativos a `consulta/`. `data/sealed` no se lista: solo se abre vía `src/holdout.py`.\n\n"]
    for sec, items in INDICE:
        L.append(f"## {sec}\n\n")
        for ruta, desc in items:
            if ruta == "llms.txt" or ruta.startswith("consulta/"):
                L.append(f"- [{ruta}](../{ruta}): {desc}\n")
                continue
            assert (RAIZ / ruta).exists(), f"INDICE: ruta inexistente {ruta}"
            L.append(f"- [{ruta}](../{ruta}): {desc}\n")
        L.append("\n")
    return "".join(L)


# ---------------------------------------------------------------- version.json y llms.txt
def _git(*args: str) -> str:
    try:
        r = subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True, timeout=30)
        return r.stdout.strip() if r.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


REPOSITORIO = PROYECTO["repositorio"]   # V13: desde proyecto.json


def construir_version(cifras: dict[str, dict]) -> dict:
    notas = (RAIZ / "docs/v8/notas_release.md").read_text(encoding="utf-8")
    m = re.search(r"^fecha_verificable:\s*(\S+)", notas, re.M)
    d = re.search(r"^doi:\s*(\S+)", notas, re.M)
    tareas = (RAIZ / "docs/v14/tareas_autor.md").read_text(encoding="utf-8")
    pend = [re.sub(r"^\d+\.\s*", "", t.lstrip("# ").strip()) for t in tareas.splitlines() if t.startswith("## ")]
    sha = hashlib.sha256((RAIZ / "output/v5/cifras_clave.csv").read_bytes()).hexdigest()
    return {"_generado": "Generado por `make consulta` (src/consulta/generar.py). No editar a mano.", "version": PROYECTO["version_publica"],
            "fecha_version": PROYECTO["fecha_version"],
            "versiones_internas_vigentes": {k: v["version_interna"] for k, v in PROYECTO["vigentes"].items()},
            "referencia_modelizacion": "V8", "referencia_deficit_y_necesidad": "v7.1 con correcciones de v7.2",
            "commit": _git("log", "-1", "--format=%h", "--", "output") or "desconocido",
            "commit_nota": "commit del último cambio de contenido de output/ (git log -1 --format=%h -- output), no HEAD: HEAD cambia con cada commit y rompería la comparación con lo versionado",
            "fecha": _git("log", "-1", "--format=%cs", "--", "output") or "desconocido", "doi": PROYECTO["doi"], "doi_preregistro_v8": d.group(1) if d else "pendiente",
            "repositorio": REPOSITORIO,
            "fecha_verificable": m.group(1) if m else "desconocido", "pendientes": pend, "n_cifras_clave": len(cifras), "sha256_cifras_clave": sha,
            "autor": "Borja Romero, economista (firma individual, independiente)",
            "difusion": "V10: base única, atlas descriptivo, figuras, web y monitor (sin modelos nuevos)",
            "web_prevista": PROYECTO["web"]}


def construir_llms() -> str:
    for r in ("consulta/LEEME_ASISTENTE.md", "output/v5/cifras_clave.csv", "docs/v8/cierre_proyecto.md"):
        assert (RAIZ / r).exists() or r.startswith("consulta/"), r
    return """# Vivienda en España: base de evidencia reproducible

> Base de evidencia sobre precios, alquileres, déficit y necesidad de vivienda en España, con un análisis de por qué ha subido (V8: factores, periodos y factor común). Cada resultado lleva una capa de evidencia (C1, C2, C3, C3s, C4); la causalidad solo se admite en C3 y C3s. Se evalúan afirmaciones e instrumentos, nunca partidos ni personas. Autor: Borja Romero, economista (firma individual, independiente). Versión pública {VP} ({FV}; versiones internas v1-V12, correspondencia en CHANGELOG.md). Repositorio: {REPO}.

Generado por `make consulta`; no editar a mano. Empieza por la guía para asistentes y cita solo cifras de cifras_clave con su id y su fecha.

## Empieza aquí

- [Guía para asistentes](consulta/LEEME_ASISTENTE.md): versión vigente, capas, reglas para responder y mapa «si te preguntan X, mira Y»
- [Preguntas frecuentes](consulta/preguntas_frecuentes.md): respuestas breves con cifra, capa y fuente
- [Registro de hallazgos](consulta/hallazgos.md): todos los hallazgos vigentes, superados y retirados (también [JSON](consulta/hallazgos.json))
- [Glosario](consulta/glosario.md): términos técnicos
- [Índice de ficheros](consulta/indice_ficheros.md): mapa de carpetas y ficheros clave
- [Versión y pendientes](consulta/version.json): versión, commit de contenido, DOI y tareas del autor

## Cifras y resultados

- [cifras_clave.csv](output/v5/cifras_clave.csv): única fuente de cifras difundibles, con id, capa y fecha del dato
- [cifras_superadas.csv](output/v5/cifras_superadas.csv): cifras que no deben citarse y su sustituta
- [Por qué ha subido la vivienda (V8)](publicacion/por_que_ha_subido.md): ensayo principal
- [Informe econométrico V8](publicacion/informe_econometrico_v8.md): detalle técnico de V8
- [Cierre de V8](docs/v8/cierre_proyecto.md): qué responde, qué no pudo hacerse y qué falta
- [Lo que sabemos](publicacion/lo_que_sabemos.md): déficit y necesidad de vivienda por capa
- [Verificador V8](publicacion/verificador/verificador_v8.md): fichas para evaluar afirmaciones concretas
- [Atlas descriptivo (V10)](publicacion/atlas_descriptivo.md): quién soporta el coste de la vivienda y dónde (ids V10-ATL en cifras_clave)
- [Base de datos única (V10)](docs/v10/diccionario_base.md): diccionario; datos en data/base/publica
- [Web pública (V10)](web/README.md): panel, mapas, fichas territoriales, verificador y monitor

## Metodología

- [Capas de evidencia](metodologia/capas.md)
- [Anexo metodológico](metodologia/anexo_metodologico.md)
- [Historial de conclusiones](metodologia/historial_conclusiones.md)
- [Pre-registro de V8](metodologia/preregistro_v8.md)

## Optional

- [Reproducir](reproducir/instrucciones.md)
- [Errata](ERRATA.md)
- [Cómo citar](CITATION.cff)
- [Mapa del repositorio](docs/MAPA.md)
""".replace("{VP}", PROYECTO["version_publica"]).replace("{FV}", PROYECTO["fecha_version"]).replace("{REPO}", REPOSITORIO)


# ---------------------------------------------------------------- orquestación
def generar() -> dict[str, str]:
    """Devuelve {ruta relativa a la raíz: contenido} sin escribir nada."""
    cifras, superadas = cargar_cifras(), cargar_superadas()
    version = construir_version(cifras)
    H = construir_hallazgos(cifras, superadas)
    hj = {"_generado": "Generado por `make consulta` (src/consulta/generar.py). No editar a mano.", "version": PROYECTO["version_publica"],
          "estados": ["vigente", "superada", "retirada", "no publicada (1.0)"], "capas": list(CAPAS_VALIDAS), "n": len(H), "hallazgos": H}
    return {
        "consulta/LEEME_ASISTENTE.md": leeme_md(cifras, version),
        "consulta/hallazgos.json": json.dumps(hj, ensure_ascii=False, indent=1) + "\n",
        "consulta/hallazgos.md": hallazgos_md(H, cifras),
        "consulta/preguntas_frecuentes.md": faq_md(cifras),
        "consulta/glosario.md": glosario_md(),
        "consulta/indice_ficheros.md": indice_md(),
        "consulta/version.json": json.dumps(version, ensure_ascii=False, indent=1) + "\n",
        "llms.txt": construir_llms(),
    }


def escribir(base: Path = RAIZ) -> list[str]:
    arch = generar()
    for rel, txt in arch.items():
        p = base / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(txt, encoding="utf-8")
    return sorted(arch)


def main() -> int:
    n = escribir()
    print(f"consulta: {len(n)} ficheros escritos ({', '.join(n)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
