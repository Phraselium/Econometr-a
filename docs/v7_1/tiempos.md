# Tiempos de ejecución medidos

Todos los tiempos son de reloj, en un clon limpio, sin red y con un solo hilo (CPU genérica del entorno de trabajo). Son orientativos: dependen de la máquina.

| Orden | Qué hace | Tiempo medido | Cuándo |
|---|---|---|---|
| `make all` | datos en caché → paneles → modelos v1-v6.3 → entregables → verificador | 7.435 s (unas 2 h 4 min) | cierre de V7, 12-10-2026 |
| `make v7` | atlas regional V7 (R1-R7) y, desde v7.1, `make v7_1` | 3.053 s y 3.044 s (dos ejecuciones idénticas) | cierre de V7 |
| `make v7_1` | dosis y coste (S1), atlas v7.1, cifras de difusión (S3), cifras_clave y render | unos 40 s | V7.1 |
| `make publicacion` | genera publicacion/, metodologia/ y reproducir/ | unos 5 s | V7.1 |
| `make check` | ruff, pytest, controles de texto, cifras y capas | unos 6 min | V7.1 |
| Monte Carlo de R2 (ronda 3) | incluido en `make v7` | unos 1.600 s | V7 |
| `make evaluate_v7 --simular` | ensayo con datos simulados (sin red, sin registrar apertura) | ver output/v7_1/S4/ensayo.md | V7.1 |

Los tiempos del cierre de V7.1 se añaden en docs/v7_1/estado.md al terminar.
