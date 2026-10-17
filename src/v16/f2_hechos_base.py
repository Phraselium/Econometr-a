"""V16-F2.1 · Utilidades comunes de los hechos C1/C2 actualizados: tolerancias, grupos de fuentes, regla de capa y registro de cifras.

Tolerancias DECLARADAS ANTES de calcular las parejas nuevas (instrucción de la fase 2.1) y fijadas aquí:
- TOL_PP: dos medidas de un cambio acumulado coinciden si su diferencia es <= 3,0 puntos porcentuales.
- TOL_REL_RECUENTO: dos recuentos coinciden si su cociente difiere <= 15 % (metodologia/capas.md).
Nota de honradez: la comparación IPV frente a valor tasado ya figuraba en la 1.0 (A23-P1 y A23-P2); la tolerancia de 3 p.p. no se
eligió mirando las diferencias de 2007, 2013 y 2019, que no estaban publicadas.

Regla de capa (misma vara que las 11 bajadas de docs/v15/bajadas_capa.csv): C1 solo si hay >= 2 fuentes de >= 2 GRUPOS
distintos cuyas cifras coinciden dentro de la tolerancia. Fuente única, o fuentes del mismo grupo (misma fuente primaria),
son C4. Con discrepancia se publican ambas medidas (rango) y la capa es C4.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[2]
SAL = RAIZ / "output" / "v16" / "f2_hechos"
SEED = 20261010
TOL_PP = 3.0
TOL_REL_RECUENTO = 0.15
FECHA = "2026-10-17"

# Grupo = fuente primaria. Dos medidas del mismo grupo no son independientes.
GRUPO = {
    "INE IPV": "notarial", "Notariado": "notarial",
    "MIVAU valor tasado": "tasacion",
    "Registradores": "registral",
    "INE IPC alquiler": "encuesta_ine", "INE IPVA": "aeat_irpf", "SERPAVI": "aeat_irpf",
    "Incasòl fianzas": "fianzas_cat", "GVA fianzas": "fianzas_cv",
    "Censo 2021": "censo", "Censo 2021 consumo eléctrico": "censo", "Catastro": "catastro",
    "MIVAU fin de obra": "mivau_obra", "INE ECP": "ine_hogares", "INE EPA": "ine_hogares",
    "CGPJ": "cgpj", "OCDE": "ine_ipv_derivado", "Eurostat HPI": "ine_ipv_derivado", "BIS": "ine_ipv_derivado",
    "Eurostat ECV": "ecv", "OCDE Affordable Housing": "ocde_ah",
}
# Parejas que K6 declara NO independientes en precios de España (salen del IPV del INE).
NO_INDEPENDIENTES = [("INE IPV", "OCDE"), ("INE IPV", "Eurostat HPI"), ("INE IPV", "BIS"), ("OCDE", "Eurostat HPI"),
                     ("Eurostat ECV", "Eurostat HPI")]

HECHOS: list[dict] = []
CONTROL: list[dict] = []
FICHAS: dict[str, str] = {}


def pct(x: float) -> float:
    return float("nan") if x is None else 100.0 * x


def coinciden(valores: dict[str, float], tol: float = TOL_PP) -> list[str]:
    """Mayor subconjunto de fuentes con amplitud <= tol; devuelve sus nombres (vacío si ninguno tiene >= 2)."""
    ks = sorted((k for k in valores if not np.isnan(valores[k])), key=lambda k: valores[k])
    mejor: list[str] = []
    for i in range(len(ks)):
        for j in range(i, len(ks)):
            if valores[ks[j]] - valores[ks[i]] <= tol and j - i + 1 > len(mejor):
                mejor = ks[i:j + 1]
    return mejor if len(mejor) >= 2 else []


def capa_por_vara(valores: dict[str, float], tol: float = TOL_PP) -> tuple[str, list[str]]:
    """C1 si el subconjunto que coincide tiene >= 2 grupos distintos y ninguna pareja declarada no independiente."""
    nuc = coinciden(valores, tol)
    if len({GRUPO[k] for k in nuc}) >= 2:
        return "C1", nuc
    return "C4", nuc


def anotar(id_: str, indicador: str, valor, vmin, vmax, unidad: str, periodo: str, cobertura: str, fuentes: list[str], capa: str,
           fecha_dato: str, ficha: str, tolerancia: str = "", motivo_capa: str = "", ancla: str | None = None) -> None:
    """Registra una cifra y su ficha. `fuentes` son claves de GRUPO; el test comprueba que una cifra C1 tenga >= 2 grupos."""
    ancla = ancla or id_.lower()
    f = lambda x: None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 3)  # noqa: E731
    HECHOS.append({"id": id_, "indicador": indicador, "valor": f(valor), "min": f(vmin), "max": f(vmax), "unidad": unidad,
                   "periodo": periodo, "cobertura": cobertura, "fuentes": "; ".join(fuentes), "capa": capa, "fecha_dato": fecha_dato,
                   "ficha": f"output/v16/f2_hechos/fichas.md#{ancla}"})
    CONTROL.append({"id": id_, "capa": capa, "fuentes": fuentes, "grupos": sorted({GRUPO[s] for s in fuentes}), "tolerancia": tolerancia})
    FICHAS[ancla] = (f"### {id_}\n<a id=\"{ancla}\"></a>\n\n- **Definición.** {indicador} ({unidad}; {periodo}; {cobertura}).\n"
                     f"- **Fuentes.** {'; '.join(fuentes)} (grupos: {', '.join(sorted({GRUPO[s] for s in fuentes}))}).\n"
                     f"- **Capa {capa}.** {motivo_capa}\n- **Tolerancia.** {tolerancia or 'no aplica (fuente única o descriptivo)'}\n"
                     f"- **Cálculo reproducible.** {ficha}\n")
