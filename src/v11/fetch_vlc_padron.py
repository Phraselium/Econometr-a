"""V11-DATOS (3.ª pasada): Padrón Municipal de València (Oficina d'Estadística del Ajuntament), PDF anuales.

Variantes de nombre comprobadas (sondeo 2026-10-16, años 1990-2026; docs/v11/vlc_padron_ficheros.md):
- Padrón «Características de la población»: <A>/Padron<A>.pdf (2001-2013 y 2015) y <A>/Padron<A>Cast.pdf (2016-2026;
  también ...Val.pdf). 2014 no existe con ninguna variante.
- Población de nacionalidad extranjera: <A>/Pob_estrangera_<A>.pdf (2001-2015), _Cas.pdf (2016-2023), _Cast.pdf
  (2024-2026); también _Val.pdf desde 2016.
- Altas y bajas: AltasBajas/<A>/AltasBajasPadron<A>.pdf (2004-2016; 2007-2014 también en <A>/). Desde 2017 no existe.
Los PDF van a data/raw/v11/vlc_padron/original/ (no versionados; sha256 en el manifiesto). La extracción de tablas la
hace src/v11/extrae_vlc_padron.py (llamado desde main): tablas normalizadas versionadas en data/raw/v11/vlc_padron/.
Licencia: Ajuntament de València, datos abiertos (reutilización con cita de la fuente).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.v11.comun import RAW11, descargar, registrar, verificar_manifiesto  # noqa: E402

FUENTE = "vlc_padron"
DIR = RAW11 / FUENTE
B = "https://www.valencia.es/estadistica/Padron"
LIC = "Ajuntament de València, Oficina d'Estadística: reutilización con cita de la fuente"


def urls() -> list[tuple[str, int, str]]:
    out = []
    for a in list(range(2001, 2014)) + [2015]:
        out.append(("padron", a, f"{B}/{a}/Padron{a}.pdf"))
    # 2025-2026: la versión en castellano usa fuentes sin mapa Unicode (texto «(cid:..)» en la mitad de las páginas);
    # la versión en valenciano sí se lee: se usa esa (mismas tablas, rótulos bilingües)
    for a in range(2016, 2027):
        out.append(("padron", a, f"{B}/{a}/Padron{a}{'Cast' if a <= 2024 else 'Val'}.pdf"))
    for a in range(2001, 2016):
        out.append(("extranjera", a, f"{B}/{a}/Pob_estrangera_{a}.pdf"))
    for a in range(2016, 2027):
        out.append(("extranjera", a, f"{B}/{a}/Pob_estrangera_{a}_{'Cas' if a <= 2023 else 'Cast' if a == 2024 else 'Val'}.pdf"))
    for a in range(2004, 2017):
        out.append(("altas_bajas", a, f"{B}/AltasBajas/{a}/AltasBajasPadron{a}.pdf"))
    return out


def main(verificar: bool = False) -> int:
    if verificar:
        return verificar_manifiesto(FUENTE)
    DIR.mkdir(parents=True, exist_ok=True)
    fallos = []
    for tipo, a, u in urls():
        dest = DIR / "original" / f"{tipo}_{a}.pdf"
        try:
            descargar(u, dest, timeout=600, intentos=3)
        except RuntimeError as e:
            fallos.append(f"{u}: {e}")
            continue
        registrar(FUENTE, dest, u, edicion=f"Ajuntament de València, {tipo.replace('_', ' ')} {a}", periodo=f"{a}-01-01" if tipo != "altas_bajas" else str(a),
                  nivel_territorial="ciudad, distrito, barrio (y sección)", licencia=LIC, redistribuible=True,
                  notas="no versionado (PDF): se regenera con make datos_v11")
    from src.v11 import extrae_vlc_padron
    extrae_vlc_padron.main()
    for f in fallos:
        print("FALLO", f)
    return 0


if __name__ == "__main__":
    sys.exit(main("--verificar" in sys.argv))
