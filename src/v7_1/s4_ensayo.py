"""V7.1-S4 · Ensayo de `make evaluate_v7` con datos FUTUROS SIMULADOS. Nunca descarga datos reales ni toca data/raw ni el
registro real de accesos (docs/v7/evaluate_v7_accesos.md).

Recorre el camino real de src/v7/evaluate_v7.py (no el modo --simular) en un directorio temporal:
  1. «descarga» simulada: ficheros con el MISMO formato que data/raw (ine_ipv_80270.csv trimestral e ine_ipc_alquiler.csv
     mensual) con 2026T3-2027T2 generados por paseo aleatorio desde el último dato hasta 2026T2 (SEED);
  2. detección de periodos nuevos (formatos) y comprobación del sha256 de la congelación (93795a94…);
  3. registro de la apertura en un registro TEMPORAL antes de evaluar; carga de los modelos congelados; métricas;
  4. casos de control: segunda ejecución (debe negarse), sha256 alterado (debe negarse), sin datos nuevos (no registra).
Escribe output/v7_1/S4/ensayo.md y ensayo.json (sin marcas de tiempo, deterministas). Las métricas son de datos simulados:
no dicen nada sobre la capacidad predictiva real.
"""
from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v7"))
import evaluate_v7 as E  # noqa: E402
import r5_prediccion as R5  # noqa: E402

SEED = 20261010
OUT = RAIZ / "output" / "v7_1" / "S4"
TRIM = ["2026T3", "2026T4", "2027T1", "2027T2"]
MESES = [f"2026M{m:02d}" for m in range(7, 13)] + [f"2027M{m:02d}" for m in range(1, 7)]


def _fecha(p: str) -> str:
    if "T" in p:
        a, t = p.split("T")
        return f"{a}-{3 * (int(t) - 1) + 1:02d}-01"
    a, m = p.split("M")
    return f"{a}-{m}-01"


def simular_descarga(destino: Path, futuro: bool = True) -> None:
    """Escribe en `destino` ficheros con el formato de data/raw: historia real hasta 2026T2 y, si futuro, 2026T3-2027T2 simulados."""
    rng = np.random.default_rng(SEED)
    destino.mkdir(parents=True, exist_ok=True)
    for fich, sufijo, periodos, mu, sd, corte in (("ine_ipv_80270.csv", ". General. Índice.", TRIM, 0.012, 0.015, "2026T2"),
                                                   ("ine_ipc_alquiler.csv", ". Alquiler de vivienda. Índice.", MESES, 0.003, 0.002, "2026M06")):
        d = pd.read_csv(RAIZ / "data" / "raw" / fich, dtype=str)   # solo lectura
        d = d[d["nombre"].str.endswith(sufijo) & (d["periodo"] <= corte)]
        filas = []
        if futuro:
            for nombre, g in d.groupby("nombre", sort=True):
                ult = g.sort_values("periodo").iloc[-1]
                v = float(ult["valor"]) * np.exp(np.cumsum(rng.normal(mu, sd, len(periodos))))
                for p, x in zip(periodos, v):
                    filas.append({**ult.to_dict(), "periodo": p, "fecha": _fecha(p), "valor": f"{x:.3f}",
                                  "fuente": "SIMULADO (ensayo v7.1)", "url": "SIMULADO"})
        pd.concat([d, pd.DataFrame(filas, columns=d.columns)]).to_csv(destino / fich, index=False)


def _ejecutar(tmp: Path, notas: Path, futuro: bool = True) -> tuple[int, str]:
    E.RAIZ, E.ACCESOS, E.OUT, E.NOTAS = tmp, tmp / "accesos.md", tmp / "evaluate", notas
    E.descargar = lambda destino: simular_descarga(destino, futuro)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = E.main(simular=False)
    return rc, buf.getvalue().strip()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    orig = (E.RAIZ, E.ACCESOS, E.OUT, E.NOTAS, E.descargar)
    acc_real = (RAIZ / "docs" / "v7" / "evaluate_v7_accesos.md")
    antes = acc_real.read_bytes() if acc_real.exists() else None
    casos = {}
    notas = E.NOTAS   # se fija antes: _ejecutar cambia E.NOTAS en el caso del sha alterado
    try:
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            # 0. formatos: la descarga simulada se lee con el lector real y da los 4 trimestres nuevos
            simular_descarga(tmp / "fmt")
            nuevos = R5.nuevos_periodos(tmp / "fmt", despues_de=E.ULTIMO_ENTRENO)
            obs = R5.observados(tmp / "fmt")
            casos["formatos"] = dict(periodos_nuevos=nuevos, ccaa_por_mercado=obs[obs.trimestre.isin(nuevos)].groupby("mercado").codigo_ine_ccaa.nunique().to_dict())
            # 1. camino real con sha correcto
            rc, msg = _ejecutar(tmp / "a", notas)
            acc = (tmp / "a" / "accesos.md").read_text(encoding="utf-8")
            res = json.loads((tmp / "a" / "evaluate" / "resultado.json").read_text(encoding="utf-8"))
            casos["apertura"] = dict(rc=rc, apertura_registrada="APERTURA" in acc, evaluacion_registrada="EVALUACIÓN" in acc,
                                     apertura_antes_de_evaluar=acc.find("APERTURA") < acc.find("EVALUACIÓN"),
                                     sha_en_registro=E.sha256(E.CONG) in acc)
            # 2. segunda ejecución: debe negarse (una sola evaluación)
            rc2, msg2 = _ejecutar(tmp / "a", notas)
            casos["segunda_ejecucion"] = dict(rc=rc2, mensaje=msg2)
            # 3. sha256 anotado distinto: debe negarse sin registrar
            mala = tmp / "notas_malas.md"
            mala.write_text("sha256_modelos_congelados: " + "0" * 64 + "\n", encoding="utf-8")
            rc3, msg3 = _ejecutar(tmp / "b", mala)
            casos["sha_alterado"] = dict(rc=rc3, mensaje=msg3, registro_creado=(tmp / "b" / "accesos.md").exists())
            # 4. sin periodos nuevos: no registra apertura
            rc4, msg4 = _ejecutar(tmp / "c", notas, futuro=False)
            casos["sin_datos_nuevos"] = dict(rc=rc4, mensaje=msg4, registro_creado=(tmp / "c" / "accesos.md").exists())
    finally:
        E.RAIZ, E.ACCESOS, E.OUT, E.NOTAS, E.descargar = orig
    despues = acc_real.read_bytes() if acc_real.exists() else None
    casos["registro_real_intacto"] = antes == despues
    r = res["resumen"]
    rm = pd.DataFrame(r["rmse_x100"])
    tabla = rm[rm.h == 1].pivot(index="modelo", columns="mercado", values="rmse_x100").round(3)
    ok = (casos["apertura"]["rc"] == 0 and casos["apertura"]["apertura_registrada"] and casos["apertura"]["apertura_antes_de_evaluar"]
          and casos["segunda_ejecucion"]["rc"] == 3 and casos["sha_alterado"]["rc"] == 2 and not casos["sha_alterado"]["registro_creado"]
          and casos["sin_datos_nuevos"]["rc"] == 0 and not casos["sin_datos_nuevos"]["registro_creado"] and casos["registro_real_intacto"] and len(casos["formatos"]["periodos_nuevos"]) == 4)
    js = dict(ensayo_superado=bool(ok), sha256_congelacion=E.sha256(E.CONG), casos=casos,
              metricas_simuladas=dict(etiqueta=r.get("etiqueta"), periodos_objetivo=r.get("periodos_objetivo"), n_ccaa=r.get("n_ccaa"),
                                      rmse_h1_x100=tabla.reset_index().to_dict("records")),
              nota="Datos futuros SIMULADOS (paseo aleatorio, SEED). Las métricas no informan de la capacidad predictiva real.")
    (OUT / "ensayo.json").write_text(json.dumps(js, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    L = ["# Ensayo de `make evaluate_v7` con datos futuros simulados (V7.1-S4)", "",
         f"**Resultado del ensayo: {'SUPERADO' if ok else 'NO SUPERADO'}.** Se recorrió el camino real de src/v7/evaluate_v7.py, no el modo `--simular`, "
         "en un directorio temporal. Los datos 2026T3-2027T2 son simulados. No se descargó ningún dato real, no se escribió en data/raw y el registro real "
         f"de accesos (docs/v7/evaluate_v7_accesos.md) quedó intacto ({'sí' if casos['registro_real_intacto'] else 'NO'}).", "",
         "| Comprobación | Esperado | Obtenido |", "|---|---|---|",
         f"| Formatos: periodos nuevos detectados por el lector real | 2026Q3-2027Q2 | {', '.join(casos['formatos']['periodos_nuevos'])} |",
         f"| CCAA con dato nuevo por mercado | 17 y 17 | {casos['formatos']['ccaa_por_mercado']} |",
         f"| sha256 de la congelación | 93795a94… | {E.sha256(E.CONG)[:8]}… (coincide con docs/v7/notas_release.md) |",
         f"| Apertura registrada antes de evaluar | sí | {'sí' if casos['apertura']['apertura_registrada'] and casos['apertura']['apertura_antes_de_evaluar'] else 'no'} |",
         f"| Evaluación (código de salida) | 0 | {casos['apertura']['rc']} |",
         f"| Segunda ejecución | se niega (3) | {casos['segunda_ejecucion']['rc']} |",
         f"| sha256 anotado distinto | se niega (2), sin registro | {casos['sha_alterado']['rc']}, registro {'creado' if casos['sha_alterado']['registro_creado'] else 'no creado'} |",
         f"| Sin periodos nuevos | sale sin registrar | código {casos['sin_datos_nuevos']['rc']}, registro {'creado' if casos['sin_datos_nuevos']['registro_creado'] else 'no creado'} |",
         "", "## Métricas del ensayo (datos simulados; solo comprueban que el cálculo funciona)", "",
         f"Periodos objetivo: {', '.join(r.get('periodos_objetivo', []))}; CCAA: {r.get('n_ccaa')}. RMSE ×100 a h = 1 por modelo congelado:", "",
         tabla.to_markdown(), "",
         "Estas cifras **no** se publican ni entran en cifras_clave: miden el error frente a un paseo aleatorio simulado.", ""]
    (OUT / "ensayo.md").write_text("\n".join(L), encoding="utf-8")
    print(f"s4_ensayo: {'SUPERADO' if ok else 'NO SUPERADO'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
