"""BI · orquestador: smoke (2009-2015) -> run completo. Un único Registry por ejecución.
Uso: python src/v2/bi_run.py [--solo-smoke]"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bi_h3  # noqa: E402
import bi_het  # noqa: E402
import bi_oos  # noqa: E402
import bi_report  # noqa: E402
import econ_utils  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "output" / "v2" / "BI"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rs = econ_utils.Registry(OUT / "smoke_registro.csv")
    bi_h3.run(rs, smoke=True)
    bi_het.run(rs, smoke=True)
    bi_oos.run(rs, smoke=True)
    rs.flush()
    if "--solo-smoke" in sys.argv:
        return
    reg = econ_utils.Registry(OUT / "registro.csv")
    h3 = bi_h3.run(reg)
    het = bi_het.run(reg)
    oos = bi_oos.run(reg)
    reg.flush()
    bi_report.escribir(h3, het, oos, OUT)


if __name__ == "__main__":
    main()
