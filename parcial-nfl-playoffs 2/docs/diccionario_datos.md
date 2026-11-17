# Diccionario de datos

Este documento incluiría **todas las variables del dataset original** (`data/raw/games.csv`, 7.548 filas y 46 columnas) y también las variables construidas para el modelo. Las descripciones del archivo original provienen de la documentación del repositorio nflverse/nfldata (`DATASETS.md`). Las marcadas con `*` no figuran en esa documentación y se deducirían del nombre de la columna. Las escalas y las categorías (por ejemplo el tipo de partido) las define el propio dataset; las variables de rendimiento por corte las calcula este proyecto.

> Los faltantes se calcularon sobre las 7.548 filas del archivo crudo, que incluyen la temporada 2026 en curso (sus partidos no jugados tienen puntaje vacío). Un faltante en `away_score` o `home_score` significaría «partido todavía no jugado» y no un cero. En las variables de apuestas y clima, la falta de dato indicaría que no se registró o no corresponde (por ejemplo, la temperatura no se mide en estadios cerrados).

## 1. Términos técnicos para quien no conoce el tema
- **Temporada regular (`REG`)**: los partidos del campeonato, 16 por equipo hasta 2020 y 17 desde 2021.
- **Playoffs**: fase final a la que acceden 12 equipos hasta 2019 y 14 desde 2020. Sus rondas son `WC` (comodines), `DIV` (divisional), `CON` (final de conferencia) y `SB` (Super Bowl).
- **Semana de descanso (*bye*)**: la semana en que un equipo no juega. Por eso «el partido N» de un equipo no siempre cae en la semana N.
- **Mariscal de campo (*quarterback*, QB)**: el jugador que dirige el ataque.
- **Moneyline, spread y over/under**: cuotas y líneas del mercado de apuestas. Indicarían qué equipo se esperaba que ganara y cuántos puntos se esperaban en total.

## 2. Variables del dataset original
| Variable | Tipo | Valores posibles (rango o categorías) | Faltantes | ¿Se usa? | Significado y motivo |
|---|---|---|---|---|---|
| `game_id` | texto / categoría | 7548 valores distintos, por ejemplo 1999_01_MIN_ATL, 1999_01_KC_CHI, 1999_01_PIT_CLE | 0 (0.0%) | No | Identificador legible del partido: temporada, semana, visitante y local (ej. 1999_01_MIN_ATL). Identificador de otra fuente o del partido. No describe rendimiento deportivo. |
| `season` | número entero | 1999 a 2026 | 0 (0.0%) | Sí | Año de la temporada. Los partidos de enero y los playoffs cuentan en la temporada del año anterior. Se usa para construir la etiqueta y las variables de rendimiento. |
| `game_type` | texto / categoría | CON, DIV, REG, SB, WC | 0 (0.0%) | Sí | Tipo de partido: REG (temporada regular), WC, DIV, CON (playoffs) o SB (Super Bowl). Se usa para construir la etiqueta y las variables de rendimiento. |
| `week` | número entero | 1 a 22 | 0 (0.0%) | Sí | Semana de la temporada (1 a 17/18 en regular; 18 a 21 en playoffs, según la documentación). Se usa para construir la etiqueta y las variables de rendimiento. |
| `gameday` | fecha (texto AAAA-MM-DD) | 1999-09-12 a 2027-01-10 | 0 (0.0%) | Sí | Fecha del partido. Se usa para construir la etiqueta y las variables de rendimiento. |
| `weekday` | texto / categoría | Friday, Monday, Saturday, Sunday, Thursday, Tuesday, Wednesday | 0 (0.0%) | No | Día de la semana. Calendario del partido. No se incluye en esta versión del modelo. |
| `gametime` | texto / categoría | 57 valores distintos, por ejemplo 13:00, 16:05, 16:15 | 259 (3.4%) | No | Hora de inicio (hora del Este, 24 h). Calendario del partido. No se incluye en esta versión del modelo. |
| `away_team` | texto / categoría | 35 valores distintos, por ejemplo MIN, KC, PIT | 0 (0.0%) | Sí | Equipo visitante. Se usa para construir la etiqueta y las variables de rendimiento. |
| `away_score` | número decimal | 0 a 59 | 152 (2.0%) | Sí | Puntos del visitante (faltante si el partido no se jugó). Se usa para construir la etiqueta y las variables de rendimiento. |
| `home_team` | texto / categoría | 35 valores distintos, por ejemplo ATL, CHI, CLE | 0 (0.0%) | Sí | Equipo local designado. Se usa para construir la etiqueta y las variables de rendimiento. |
| `home_score` | número decimal | 0 a 70 | 152 (2.0%) | Sí | Puntos del local (faltante si el partido no se jugó). Se usa para construir la etiqueta y las variables de rendimiento. |
| `location` | texto / categoría | Home, Neutral | 0 (0.0%) | No | Home si el local juega en su estadio; Neutral si se juega en cancha neutral. Condiciones del lugar del partido. No se incluyen para mantener un modelo basado solo en resultados; podrían ser trabajo futuro. |
| `result` | número decimal | -49 a 59 | 152 (2.0%) | No | Puntos del local menos puntos del visitante. Se deduce de los puntajes del propio partido, que ya se usan; sería redundante y mezclaría información del partido que se quiere describir. |
| `total` | número decimal | 3 a 106 | 152 (2.0%) | No | Suma de los puntos de ambos equipos. Se deduce de los puntajes del propio partido, que ya se usan; sería redundante y mezclaría información del partido que se quiere describir. |
| `overtime` | número decimal | 0 a 1 | 152 (2.0%) | No | 1 si el partido llegó a tiempo extra. * Se deduce de los puntajes del propio partido, que ya se usan; sería redundante y mezclaría información del partido que se quiere describir. |
| `old_game_id` | número entero | 1.99909e+09 a 2.02701e+09 | 0 (0.0%) | No | Identificador antiguo del partido. * Identificador de otra fuente o del partido. No describe rendimiento deportivo. |
| `gsis` | número decimal | 588 a 1.9991e+09 | 151 (2.0%) | No | Identificador del partido en el sistema GSIS de la NFL. Identificador de otra fuente o del partido. No describe rendimiento deportivo. |
| `nfl_detail_id` | texto / categoría | 272 valores distintos, por ejemplo 10160000-0585-0395-7f87-0c3334b38e2e, 10160000-0585-0480-6b01-c3eef69858d5, 10160000-0585-05c2-6453-a2e392056a4d | 7276 (96.4%) | No | Identificador del partido en otra fuente de la NFL. * Identificador de otra fuente o del partido. No describe rendimiento deportivo, y tiene muchos faltantes. |
| `pfr` | texto / categoría | 7548 valores distintos, por ejemplo 199909120atl, 199909120chi, 199909120cle | 0 (0.0%) | No | Identificador en Pro Football Reference. Identificador de otra fuente o del partido. No describe rendimiento deportivo. |
| `pff` | número decimal | 731 a 30726 | 2879 (38.1%) | No | Identificador en Pro Football Focus. Identificador de otra fuente o del partido. No describe rendimiento deportivo, y tiene muchos faltantes. |
| `espn` | número entero | 1.90912e+08 a 4.01873e+08 | 0 (0.0%) | No | Identificador en ESPN. Identificador de otra fuente o del partido. No describe rendimiento deportivo. |
| `ftn` | número decimal | 5058 a 7290 | 5602 (74.2%) | No | Identificador del partido en FTN. * Identificador de otra fuente o del partido. No describe rendimiento deportivo, y tiene muchos faltantes. |
| `away_rest` | número entero | 4 a 21 | 0 (0.0%) | No | Días de descanso del visitante. * Calendario del partido. No se incluye en esta versión del modelo. |
| `home_rest` | número entero | 4 a 16 | 0 (0.0%) | No | Días de descanso del local. * Calendario del partido. No se incluye en esta versión del modelo. |
| `away_moneyline` | número decimal | -1800 a 2173 | 2117 (28.0%) | No | Cuota moneyline del visitante. * Cuota o línea del mercado de apuestas: información externa al rendimiento del equipo y con muchos faltantes en parte de las columnas. Se prefirió un modelo basado solo en resultados. |
| `home_moneyline` | número decimal | -5000 a 1100 | 2117 (28.0%) | No | Cuota moneyline del local. * Cuota o línea del mercado de apuestas: información externa al rendimiento del equipo y con muchos faltantes en parte de las columnas. Se prefirió un modelo basado solo en resultados. |
| `spread_line` | número decimal | -19 a 27 | 136 (1.8%) | No | Línea de ventaja (spread): positiva si el local era favorito. Coincide en signo con result. Cuota o línea del mercado de apuestas: información externa al rendimiento del equipo y con muchos faltantes en parte de las columnas. Se prefirió un modelo basado solo en resultados. |
| `away_spread_odds` | número decimal | -137 a 138 | 2117 (28.0%) | No | Cuota del spread, visitante. * Cuota o línea del mercado de apuestas: información externa al rendimiento del equipo y con muchos faltantes en parte de las columnas. Se prefirió un modelo basado solo en resultados. |
| `home_spread_odds` | número decimal | -146 a 126 | 2117 (28.0%) | No | Cuota del spread, local. * Cuota o línea del mercado de apuestas: información externa al rendimiento del equipo y con muchos faltantes en parte de las columnas. Se prefirió un modelo basado solo en resultados. |
| `total_line` | número decimal | 28.5 a 63.5 | 136 (1.8%) | No | Línea de apuestas de puntos totales. Cuota o línea del mercado de apuestas: información externa al rendimiento del equipo y con muchos faltantes en parte de las columnas. Se prefirió un modelo basado solo en resultados. |
| `under_odds` | número decimal | -125 a 113 | 2120 (28.1%) | No | Cuota de "menos de" en puntos totales. * Cuota o línea del mercado de apuestas: información externa al rendimiento del equipo y con muchos faltantes en parte de las columnas. Se prefirió un modelo basado solo en resultados. |
| `over_odds` | número decimal | -125 a 113 | 2120 (28.1%) | No | Cuota de "más de" en puntos totales. * Cuota o línea del mercado de apuestas: información externa al rendimiento del equipo y con muchos faltantes en parte de las columnas. Se prefirió un modelo basado solo en resultados. |
| `div_game` | número entero | 0 a 1 | 0 (0.0%) | No | 1 si es un partido entre equipos de la misma división. * Calendario del partido. No se incluye en esta versión del modelo. |
| `roof` | texto / categoría | closed, dome, open, outdoors | 25 (0.3%) | No | Techo del estadio: outdoors, open, closed o dome. Condiciones del lugar del partido. No se incluyen para mantener un modelo basado solo en resultados; podrían ser trabajo futuro. |
| `surface` | texto / categoría | 9 valores distintos, por ejemplo astroturf, grass, fieldturf | 99 (1.3%) | No | Tipo de superficie de juego. Condiciones del lugar del partido. No se incluyen para mantener un modelo basado solo en resultados; podrían ser trabajo futuro. |
| `temp` | número decimal | -6 a 109 | 2297 (30.4%) | No | Temperatura en el estadio (solo outdoors y open). Condiciones del lugar del partido. No se incluyen para mantener un modelo basado solo en resultados; podrían ser trabajo futuro. |
| `wind` | número decimal | 0 a 71 | 2297 (30.4%) | No | Viento en mph (solo outdoors y open). Condiciones del lugar del partido. No se incluyen para mantener un modelo basado solo en resultados; podrían ser trabajo futuro. |
| `away_qb_id` | texto / categoría | 337 valores distintos, por ejemplo 00-0003761, 00-0006300, 00-0015700 | 136 (1.8%) | No | Identificador del mariscal de campo visitante. * Identificador de otra fuente o del partido. No describe rendimiento deportivo. |
| `home_qb_id` | texto / categoría | 320 valores distintos, por ejemplo 00-0002876, 00-0010560, 00-0004230 | 136 (1.8%) | No | Identificador del mariscal de campo local. * Identificador de otra fuente o del partido. No describe rendimiento deportivo. |
| `away_qb_name` | texto / categoría | 339 valores distintos, por ejemplo Randall Cunningham, Elvis Grbac, Kordell Stewart | 136 (1.8%) | No | Mariscal de campo visitante. * Persona involucrada en el partido. No se incluye (podría ser trabajo futuro, por ejemplo la calidad del mariscal de campo). |
| `home_qb_name` | texto / categoría | 323 valores distintos, por ejemplo Chris Chandler, Shane Matthews, Ty Detmer | 136 (1.8%) | No | Mariscal de campo local. * Persona involucrada en el partido. No se incluye (podría ser trabajo futuro, por ejemplo la calidad del mariscal de campo). |
| `away_coach` | texto / categoría | 177 valores distintos, por ejemplo Dennis Green, Gunther Cunningham, Bill Cowher | 0 (0.0%) | No | Entrenador del visitante. Persona involucrada en el partido. No se incluye (podría ser trabajo futuro, por ejemplo la calidad del mariscal de campo). |
| `home_coach` | texto / categoría | 177 valores distintos, por ejemplo Dan Reeves, Dick Jauron, Chris Palmer | 0 (0.0%) | No | Entrenador del local. Persona involucrada en el partido. No se incluye (podría ser trabajo futuro, por ejemplo la calidad del mariscal de campo). |
| `referee` | texto / categoría | 91 valores distintos, por ejemplo Gerry Austin, Phil Luckett, Bob McElwee | 208 (2.8%) | No | Árbitro principal. Persona involucrada en el partido. No se incluye (podría ser trabajo futuro, por ejemplo la calidad del mariscal de campo). |
| `stadium_id` | texto / categoría | 67 valores distintos, por ejemplo ATL00, CHI98, CLE00 | 0 (0.0%) | No | Identificador del estadio. * Identificador de otra fuente o del partido. No describe rendimiento deportivo. |
| `stadium` | texto / categoría | 111 valores distintos, por ejemplo Georgia Dome, Soldier Field, Cleveland Browns Stadium | 0 (0.0%) | No | Nombre del estadio. Condiciones del lugar del partido. No se incluyen para mantener un modelo basado solo en resultados; podrían ser trabajo futuro. |

## 3. Variables construidas para el modelo (`data/processed/`)
Se calcularían a partir de los **primeros N partidos de temporada regular de cada equipo** (N = 4, 6, 9 o 12), y no incluirían ningún partido posterior.

| Variable | Tipo | Valores posibles | Significado | ¿Predictor? |
|---|---|---|---|---|
| `season` | entero | 2002 a 2025 | Temporada | No (identificador) |
| `team` | texto | 32 siglas de equipos | Equipo (los que cambiaron de ciudad se unificarían bajo el nombre actual: OAK→LV, SD→LAC, STL→LA) | No (identificador) |
| `corte` | entero | 4, 6, 9 o 12 | Cantidad de partidos usados | No (constante dentro de cada modelo) |
| `partidos` | entero | igual a `corte` | Partidos jugados hasta el corte | No (constante dentro de cada modelo) |
| `victorias` | entero | 0 a N | Partidos ganados | No (redundante con `pct_victorias`) |
| `empates` | entero | 0 a 2 | Partidos empatados | No (ya contados en `pct_victorias`) |
| `derrotas` | entero | 0 a N | Partidos perdidos | No (redundante) |
| `pct_victorias` | decimal | 0 a 1 | `(victorias + 0,5 × empates) / partidos` | **Sí** |
| `puntos_favor_prom` | decimal | puntos por partido | Promedio de puntos anotados | **Sí** |
| `puntos_contra_prom` | decimal | puntos por partido | Promedio de puntos recibidos | **Sí** |
| `dif_puntos_prom` | decimal | puntos por partido | `puntos_favor_prom - puntos_contra_prom` | No (redundante: es exactamente esa resta) |
| `pct_victorias_ult4` | decimal | 0 a 1 | Rendimiento en los últimos 4 partidos del corte | **Sí**, solo desde el corte de 6 (en el de 4 sería idéntica a `pct_victorias`) |
| `partidos_local` | entero | 0 a N | Cuántos de esos partidos se jugaron de local | **Sí** |
| `llega_playoffs` | entero | 0 o 1 | **Etiqueta.** 1 si el equipo jugó al menos un partido `WC`, `DIV`, `CON` o `SB` en esa temporada | Objetivo |

**Disponibilidad temporal.** Todas las variables usadas estarían disponibles justo después del partido N del equipo. La etiqueta se conocería recién al final de la temporada, y es lo que se querría anticipar.

**Variables excluidas por posible fuga de información.** `result`, `total` y `overtime` describen el resultado de un partido, y `season` permitiría al modelo aprender el año en vez del rendimiento. Ninguna se incluye como predictor.
