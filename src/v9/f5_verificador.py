"""V9 F5 · verificador de afirmaciones con los diseños de V9 (turismo, topes, zonas tensionadas, inmigración, tipos,
ayudas a jóvenes, hogares). El veredicto se refiere a la afirmación, nunca a quién la hace. Toda cifra sale de
output/v5/cifras_clave.csv (ids «V9-…»). Sin lenguaje causal: ningún resultado de V9 alcanza C3/C3s.
Salidas: output/v9/fichas_verificador_v9.json y output/v9/verificador_v9.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paneles as P  # noqa: E402

V9 = P.RAIZ / "output" / "v9"


def main() -> int:
    ck = pd.read_csv(P.RAIZ / "output/v5/cifras_clave.csv", dtype=str).set_index("id")

    def v(i, d=1):
        x = float(ck.loc[i, "valor"])
        return f"{x:.{d}f}".replace(".", ",").replace("-", "−")

    def r(i, d=1):
        lo, hi = float(ck.loc[i, "min"]), float(ck.loc[i, "max"])
        return f"[{lo:.{d}f}; {hi:.{d}f}]".replace(".", ",").replace("-", "−")

    def p(i):
        x = float(ck.loc[i, "valor"])
        return "< 0,001" if x < 0.001 else f"{x:.3f}".replace(".", ",")

    lit = "Referencias: docs/v9_prep/literatura.csv (estado VERIFICADA/NO VERIFICADA y cuartil en cada fila)."
    fichas = [
        {"id": "V9-V1", "tema": "Pisos turísticos", "enunciado": "Los pisos turísticos han encarecido el alquiler.",
         "magnitud": (f"Cataluña (D2, exploratorio): por cada desviación típica más de plazas turísticas por habitante en 2019, la renta de los "
                      f"contratos nuevos varió {v('V9-D2-renta-covid', 2)} % en 2020-2021 (IC {r('V9-D2-renta-covid', 2)}) y "
                      f"{v('V9-D2-renta-reap', 2)} % en 2022-2025 (IC {r('V9-D2-renta-reap', 2)}), respecto a 2019. Las pretendencias se rechazan "
                      f"(p {p('V9-D2-renta-pretend-p')}): la asociación de la reapertura no se puede separar de tendencias previas. "
                      f"Comunitat Valenciana (D3, descriptivo): coeficiente de {v('V9-D3-media', 2)} % en la fianza media 2024→2025 por cada "
                      f"variación de +1 VUT registrada por 100 viviendas (IC {r('V9-D3-media', 2)}); como el registro cayó, una caída mayor se "
                      "asocia con una fianza media algo mayor, y el placebo 2021→2023 muestra una asociación del mismo signo, de modo que no se "
                      "separa de diferencias previas entre códigos postales."),
         "intervalo": "IC 95 % con bootstrap salvaje por municipio (D2) y errores de Conley a 10 km (D3).",
         "literatura": "Garcia-López et al. (2020, LA01, VERIFICADA, Q1): +1,9 % en el barrio medio de Barcelona; unidades no comparables. " + lit,
         "limites": "Sin diseño que supere sus pruebas; dosis municipal, no por barrio; D3 compara un resultado anterior a la mayor parte de la caída del registro.",
         "evidencia": ["output/v9/d2/tabla_d2.csv", "output/v9/d3/tabla_d3.csv", "output/v9/f3/tabla_revista.md"],
         "ids_cifras": ["V9-D2-renta-covid", "V9-D2-renta-reap", "V9-D2-renta-pretend-p", "V9-D3-media"]},
        {"id": "V9-V2", "tema": "Topes de renta (Ley catalana 11/2020)",
         "enunciado": "Los topes de renta de la Ley catalana 11/2020 redujeron la renta de los contratos nuevos.",
         "magnitud": (f"D1b (confirmatoria): ATT {v('V9-D1b-renta-att')} % (IC {r('V9-D1b-renta-att')}), p de Holm {p('V9-D1b-renta-pholm')}; "
                      f"pretendencias p {p('V9-D1b-renta-pretend-p')}, placebo de fecha p {p('V9-D1b-renta-placebo-p')}. No supera la prueba "
                      f"de Honest DiD con M̄ = 1 (M̄ de ruptura {v('V9-D1b-renta-ruptura')}), exigida en el pre-registro: queda en C4. "
                      f"Contratos nuevos: {v('V9-D1b-contratos-att')} % (IC {r('V9-D1b-contratos-att')}), sin diferencia detectable."),
         "intervalo": "IC 95 % con bootstrap multiplicador por municipio; p de Holm en la familia confirmatoria {H1a-renta, H1b-renta}.",
         "literatura": "Jofre-Monseny, Martínez-Mazza y Segú (2023, LB01, VERIFICADA, Q1): −4 % a −6 % en la renta y sin caída de la oferta, con los mismos registros. " + lit,
         "limites": "La regla pre-registrada no se relaja tras ver el resultado; la magnitud coincide con la literatura pero la evidencia no alcanza C3.",
         "evidencia": ["output/v9/d1/tabla_d1.csv", "output/v9/d1/pruebas.csv", "docs/v9/hipotesis_addendum_a1.md"],
         "ids_cifras": ["V9-D1b-renta-att", "V9-D1b-renta-pholm", "V9-D1b-renta-pretend-p", "V9-D1b-renta-placebo-p", "V9-D1b-renta-ruptura",
                        "V9-D1b-contratos-att"]},
        {"id": "V9-V3", "tema": "Zonas tensionadas (Ley 12/2023)",
         "enunciado": "La declaración de zonas tensionadas ha reducido los alquileres de los contratos nuevos en Cataluña.",
         "magnitud": (f"D1a (confirmatoria): ATT {v('V9-D1a-renta-att')} % (IC {r('V9-D1a-renta-att')}), p de Holm {p('V9-D1a-renta-pholm')}. "
                      f"No supera las pruebas: pretendencias p {p('V9-D1a-renta-pretend-p')}, placebo de fecha p {p('V9-D1a-renta-placebo-p')} y "
                      f"Honest DiD con M̄ = 1 incluye el 0: queda en C4. Euskadi (D1c, exploratorio, pocos trimestres): {v('V9-D1c-renta-att')} % "
                      f"(IC {r('V9-D1c-renta-att')})."),
         "intervalo": "IC 95 % con bootstrap multiplicador por municipio; 20 municipios de control con datos completos.",
         "literatura": "Fedea (Pinto 2026, LB03, sin DOI, no revisado por pares): comparación descriptiva Cataluña frente a España. " + lit,
         "limites": "Los municipios declarados ya tenían una evolución distinta antes de 2024; con pocos controles, la comparación es frágil.",
         "evidencia": ["output/v9/d1/tabla_d1.csv", "output/v9/d1/pruebas.csv", "output/v9/d1/fig_d1a_eventos.png"],
         "ids_cifras": ["V9-D1a-renta-att", "V9-D1a-renta-pholm", "V9-D1a-renta-pretend-p", "V9-D1a-renta-placebo-p", "V9-D1c-renta-att"]},
        {"id": "V9-V4", "tema": "Regulación y oferta de alquiler",
         "enunciado": "La regulación de rentas ha reducido el número de contratos de alquiler.",
         "magnitud": (f"Zonas tensionadas (D1a, exploratorio): {v('V9-D1a-contratos-att')} % (IC {r('V9-D1a-contratos-att')}); "
                      f"Ley 11/2020 (D1b, exploratorio): {v('V9-D1b-contratos-att')} % (IC {r('V9-D1b-contratos-att')}). Ninguna diferencia "
                      "detectable tras el ajuste de Benjamini-Hochberg."),
         "intervalo": "IC 95 %; p ajustados en output/v9/f3/tabla_capas.csv.",
         "literatura": "LB01 (VERIFICADA, Q1): sin caída de la oferta con la Ley 11/2020. " + lit,
         "limites": "El número de fianzas mide contratos registrados, no la oferta total (no observa el paso a temporada ni la economía sumergida).",
         "evidencia": ["output/v9/d1/tabla_d1.csv"], "ids_cifras": ["V9-D1a-contratos-att", "V9-D1b-contratos-att"]},
        {"id": "V9-V5", "tema": "Inmigración", "enunciado": "La llegada de inmigrantes explica la subida de los alquileres y de los precios.",
         "magnitud": (f"D4 (réplica 2003-2012, exploratorio): {v('V9-D4-ipc-replica', 2)} % del IPC de alquiler por punto de población extranjera "
                      f"(IC {r('V9-D4-ipc-replica', 2)}); valor tasado {v('V9-D4-tasado-replica', 2)} % (IC {r('V9-D4-tasado-replica', 2)}). "
                      f"Instrumento débil: F efectiva {v('V9-D4-ipc-replica-F')} (umbral 23,1). Ampliación 2015-2022, valor tasado: "
                      f"{v('V9-D4-tasado-ampliacion', 2)} % (IC {r('V9-D4-tasado-ampliacion', 2)}), también con instrumento débil."),
         "intervalo": "IC 95 % de 2SLS; IC de Anderson-Rubin y errores AKM en output/v9/d4/tabla_d4.csv.",
         "literatura": "Saiz (2007, LA09, VERIFICADA, Q1); González y Ortega (2013, LA08, VERIFICADA, Q1); Sanchis-Guarner (2023, LA07, VERIFICADA, Q1). " + lit,
         "limites": "Con 50 provincias el instrumento de redes de origen es débil; la réplica usa 2003 (primer año con país) y el IPC de alquiler (parque de contratos).",
         "evidencia": ["output/v9/d4/tabla_d4.csv", "output/v9/d4/diagnosticos.csv", "output/v9/d4/rotemberg.csv"],
         "ids_cifras": ["V9-D4-ipc-replica", "V9-D4-tasado-replica", "V9-D4-ipc-replica-F", "V9-D4-tasado-ampliacion"]},
        {"id": "V9-V6", "tema": "Tipos de interés",
         "enunciado": "Las subidas de tipos del BCE abaratan más la vivienda donde las hipotecas son a tipo variable.",
         "magnitud": (f"D5 (exploratorio, 18 países): precio a 4 trimestres {v('V9-D5-precio-h4', 1)} (IC {r('V9-D5-precio-h4', 1)}) y a 8 "
                      f"{v('V9-D5-precio-h8', 1)} (IC {r('V9-D5-precio-h8', 1)}) puntos log ×100 por unidad de shock y desviación típica de "
                      f"exposición; alquiler (IPCA) a 4 trimestres {v('V9-D5-alq-h4', 1)} (IC {r('V9-D5-alq-h4', 1)})."),
         "intervalo": "IC 95 % Driscoll-Kraay.",
         "literatura": "Koeniger, Lennartz y Ramelet (2022, LA25, VERIFICADA, Q1), cualitativo. " + lit,
         "limites": "Sin potencia para un contraste confirmatorio; la asociación del alquiler no se mantiene a 8 trimestres en la principal.",
         "evidencia": ["output/v9/d5/tabla_d5.csv", "output/v9/d5/fig_d5.png"], "ids_cifras": ["V9-D5-precio-h4", "V9-D5-precio-h8", "V9-D5-alq-h4"]},
        {"id": "V9-V7", "tema": "Ayudas a jóvenes", "enunciado": "El Bono Alquiler Joven ha subido los alquileres de los jóvenes.",
         "magnitud": "No evaluable con datos públicos: la ECV no publica el mes de nacimiento (no hay edad exacta en los 35 años) y ninguna fuente identifica a los receptores (D6).",
         "intervalo": "—", "literatura": "Laguna documentada (LB23 en docs/v9_prep/literatura.csv). " + lit,
         "limites": "Haría falta el número de beneficiarios por edad en meses, CCAA y año (solicitud de transparencia (d)).",
         "evidencia": ["docs/v9/hipotesis.md", "docs/v9/solicitudes_transparencia.md"], "ids_cifras": []},
        {"id": "V9-V8", "tema": "Hogares y población", "enunciado": "El aumento de hogares se debe sobre todo al crecimiento de la población.",
         "magnitud": (f"D7 (contable): en 2022-2025 el componente población supone {v('V9-D7-ES-2225-cuota-pob', 0)} % del aumento de hogares "
                      f"en España ({v('V9-D7-ES-2225-dH', 0)} hogares) y {v('V9-D7-CV-2225-cuota-pob', 0)} % en la Comunitat Valenciana (más del 100 % "
                      "significa que el componente tasa de jefatura fue negativo: menos hogares por persona). Periodo: stocks a 1-1-2022 y 1-1-2025. En "
                      f"2011-2021 pesa más el componente tasa de jefatura (componente población {v('V9-D7-ES-1121-cuota-pob', 0)} % en España). "
                      f"Censo 2021 y ECP coinciden en {v('V9-D7-c1-dif', 1)} % [C1]."),
         "intervalo": "Descomposición exacta (identidad); sin intervalo.",
         "literatura": "Banco de España (LA18) y OCDE (LA21, NO VERIFICADA) para el déficit: output/v9/d7/reconciliacion_deficit.csv. " + lit,
         "limites": "Es una identidad contable, no una atribución causal; población y hogares de 2022-2025 vienen de fuentes con un año de desfase (marcado).",
         "evidencia": ["output/v9/d7/descomposicion_provincia.csv", "output/v9/d7/reconciliacion_deficit.csv"],
         "ids_cifras": ["V9-D7-ES-2225-cuota-pob", "V9-D7-ES-2225-dH", "V9-D7-CV-2225-cuota-pob", "V9-D7-ES-1121-cuota-pob", "V9-D7-c1-dif"]},
    ]
    for f in fichas:
        f["capa"] = "C4"
        f["cota"] = "—"
        f["veredicto"] = "NO EVALUABLE" if f["id"] == "V9-V7" else ("DESCRIPTIVA (CONTABLE)" if f["id"] == "V9-V8" else "ANALIZADA, NO CONCLUYENTE")
        f["regla"] = "Pre-registro V9 (docs/v9/hipotesis.md y addendum A1): C3 exige superar todas las pruebas; ningún resultado de V9 las supera."
        f["version"] = "V9"
        for i in f["ids_cifras"]:
            assert i in ck.index, i
    (V9 / "fichas_verificador_v9.json").write_text(json.dumps(fichas, ensure_ascii=False, indent=1), encoding="utf-8")
    lin = ["# Verificador V9 · qué causa qué", "",
           "Borja Romero, economista (firma individual, independiente). Generado por src/v9/f5_verificador.py; cifras de output/v5/cifras_clave.csv (ids «V9-…»). "
           "El veredicto se refiere a la afirmación, nunca a quién la hace. Ningún resultado de V9 alcanza C3/C3s: no hay lectura causal.", ""]
    for f in fichas:
        lin += [f"## {f['id']} · {f['tema']}", "", f"**Afirmación.** {f['enunciado']}", "", f"**Veredicto.** {f['veredicto']} [{f['capa']}]", "",
                f"**Magnitud.** {f['magnitud']}", "", f"**Intervalo.** {f['intervalo']}", "", f"**Literatura.** {f['literatura']}", "",
                f"**Límites.** {f['limites']}", "", "**Evidencia.** " + ", ".join(f"`{e}`" for e in f["evidencia"]), ""]
    (V9 / "verificador_v9.md").write_text("\n".join(lin), encoding="utf-8")
    print(len(fichas), "fichas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
