<!-- Generado por `make publicacion` desde docs/v7_1/tiempos.md. No editar a mano: se regenera y un test lo comprueba. -->

# Tiempos de ejecución medidos

Todos los tiempos son de reloj, en un clon limpio, sin red y con un solo hilo (CPU genérica del entorno de trabajo). Son orientativos: dependen de la máquina.

| Orden | Qué hace | Tiempo medido | Cuándo |
|---|---|---|---|
| `make all` | datos en caché → paneles → modelos v1-v6.3 → entregables → verificador | 8.683 s (unas 2 h 25 min; en paralelo con `make v7`) y 7.435 s (cierre de V7) | cierre de V7.1 y de V7 |
| `make v7` | atlas regional V7 (R1-R7) y, desde v7.1, `make v7_1` | 2.926 s y 2.969 s (dos ejecuciones idénticas, 523 ficheros con md5 iguales) | cierre de V7.1 |
| `make v7_1` | dosis y coste (S1), atlas v7.1, cifras de difusión (S3), cifras_clave y render | unos 40 s | V7.1 |
| `make publicacion` | genera publicacion/, metodologia/ y reproducir/ | unos 5 s | V7.1 |
| `make check` | ruff, pytest, controles de texto, cifras y capas | 360 s y 341 s | cierre de V7.1 |
| Monte Carlo de R2 (ronda 3) | incluido en `make v7` | unos 1.600 s | V7 |
| `python3 src/v7_1/s4_ensayo.py` | ensayo de evaluate_v7 con datos futuros simulados (sin red, sin registrar apertura) | unos 6 s | V7.1 |

Cierre de V7.1: clones limpios sin red (proxy a 127.0.0.1:9), un hilo, commit 76683a9; `make v7` ×2 y `make all` en paralelo en una máquina de 4 núcleos.
