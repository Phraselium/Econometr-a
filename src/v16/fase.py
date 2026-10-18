"""V16 · Lanzador de fases (`make v16_f0` … `make v16_f7`). Cada fase ejecuta, en orden, sus scripts deterministas y sin red.

Los scripts se añaden a FASES cuando existen; una fase sin scripts todavía lo dice y termina con código 0. Las fases 5 a 7
exigen la etiqueta prereg-v16 publicada en el remoto (pre-registro interno sin sello externo; src/v16/etiquetas.py), igual que
la guarda (f) del hook. Nunca lanza estimaciones de versiones anteriores ni abre muestras selladas.
Uso: python3 src/v16/fase.py f0|f1|…|f7
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "src" / "v16"))
import etiquetas  # noqa: E402

FASES: dict[str, list[str]] = {
    "f0": ["src/v16/f0_comprobaciones.py", "src/v16/f0_lo_ya_visto.py"],
    "f1": ["src/v16/datos/demanda_internacional.py", "src/v16/datos/alquiler_turismo.py", "src/v16/datos/oferta_suelo.py",
           "src/v16/datos/renta_parque.py", "src/v16/datos/tension_social.py", "src/v16/f1_intervenciones.py",
           "src/v16/f1_inventario.py --escribir"],
    "f2": ["src/v16/f2_hechos.py", "src/v16/f2_contabilidad.py", "src/v16/f2_esfuerzo.py", "src/v16/f2_atlas.py"],
    "f3": ["src/v16/f3_verificar_referencias.py", "src/v16/f3_metaanalisis.py", "src/v16/f3_cuatro_cuadrantes.py"],
    "f4": ["src/v16/f4_potencia.py", "src/v16/f4_rejilla.py", "src/v16/f4_sellado.py"],
    "f5": ["src/v16/f5_validacion.py todas"],
    "f6": ["src/v16/q1_zonas.py", "src/v16/q2_turismo.py", "src/v16/q7_bono.py", "src/v16/q8_no_residentes.py", "src/v16/q_salidas.py",
           "src/v16/q3_shiftshare.py", "src/v16/q3_seccion.py", "src/v16/q4_oferta.py", "src/v16/q6_itp.py", "src/v16/qb_informe.py",
           "src/v16/q5_proyecciones.py", "src/v16/q9_burbuja.py", "src/v16/q10_prediccion.py", "src/v16/q_rejilla.py",
           "src/v15/p6_zonas.py", "src/v15/p6_informe.py", "src/v15/p5_turismo.py", "src/v15/p5_informe.py", "src/v15/p5cv_exposicion.py",
           "src/v15/p4_inmigracion.py", "src/v15/p9_prediccion.py", "src/v15/p2_fundamentales.py", "src/v15/p7_demografia.py",
           "src/v15/p10_espacial.py", "src/v15/pb_informe.py", "src/v16/f6_fdr.py", "src/v16/f6_triangulacion.py"],
    "f7": ["src/v16/f7_tablas.py", "src/v16/f7_informe.py"],
}


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in FASES:
        print("uso: fase.py " + "|".join(FASES))
        return 2
    f = sys.argv[1]
    if f in ("f5", "f6", "f7"):
        ok, motivo = etiquetas.prereg_v16_publicada(RAIZ)
        print(f"puerta V16: {motivo}")
        if not ok:
            return 1
    scripts = [s for s in FASES[f] if (RAIZ / s.split()[0]).exists()]
    if not scripts:
        print(f"fase {f}: sin scripts todavía (docs/v16/estado.md)")
        return 0
    for s in scripts:
        print(f">> {s}")
        r = subprocess.run([sys.executable, str(RAIZ / s.split()[0]), *s.split()[1:]], cwd=RAIZ)
        if r.returncode:
            return r.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main())
