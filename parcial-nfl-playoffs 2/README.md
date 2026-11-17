# ¿Qué tan pronto se podría saber quién llega a los playoffs de la NFL?

Proyecto de **Aprendizaje Automático** · Tecnicatura en Ciencia de Datos e IA · Centro Politécnico Superior Malvinas Argentinas
**Alumno:** Tomás Roa Gunn

## 1. Título y resumen

Este proyecto buscaría predecir, a partir de los partidos ya jugados de la temporada regular, si un equipo de la NFL llegaría a los playoffs, y medir cómo cambiaría la calidad de esa predicción según cuántos partidos se hayan jugado (4, 6, 9 o 12). Se compararían regresión logística, árbol de decisión, KNN y SVM contra dos referencias simples, con una evaluación que respeta el orden temporal (temporadas 2010 a 2025). Con los datos y la evaluación descriptos, el mejor resultado en F1 medio sería **0,813** (SVM con 12 partidos), prácticamente igual al de una regla simple por porcentaje de victorias (0,811), y ningún corte cumpliría completo el criterio de «predicción confiable» fijado de antemano.

## 2. Contexto, problema y objetivos

### Contexto y relevancia
La NFL tiene 32 equipos y, desde 2020, clasifican 14 a los playoffs (antes eran 12). Más de la mitad de los equipos queda fuera y la clasificación se define en una temporada regular corta (16 partidos hasta 2020 y 17 desde 2021), donde cada resultado pesaría mucho. Anticipar qué equipos llegarían sería útil para quien toma decisiones durante la temporada (cuerpos técnicos, medios, aficionados y jugadores de fantasy). Es además un problema acotado y con datos públicos, adecuado para construir y explicar un modelo de punta a punta.

Este trabajo continúa uno anterior de la materia (Semana 6), donde se predijo la clasificación mirando solo los primeros 9 partidos, con regresión logística, árbol de decisión y KNN sobre 224 equipos de prueba (temporadas 2019 a 2025). Los tres acertaron cerca del 81 %, frente a un 57 % de un modelo que siempre responde «no llega», y el árbol terminó usando casi una sola regla (más de 62 % de victorias implicaría llegar). Quedaban abiertas dos preguntas: qué pasaría con otros cortes de la temporada y si los modelos superarían a esa regla simple.

### Tipo de problema
Clasificación binaria supervisada. Se predice una categoría (1 = llega a playoffs, 0 = no llega) y los datos históricos traen la respuesta real.

### Definición del problema

| Elemento | Definición |
|---|---|
| **Fila (unidad de análisis)** | Un equipo en una temporada, con sus variables calculadas hasta su partido N |
| **Población** | Los 32 equipos de la NFL en las temporadas 2002 a 2025 (768 equipo-temporadas por corte) |
| **Variable objetivo** | `llega_playoffs`: 1 si el equipo jugó al menos un partido de playoffs (`WC`, `DIV`, `CON` o `SB`) en esa temporada, 0 si no |
| **Cuándo se predice** | Después del partido N de cada equipo (N = 4, 6, 9 o 12). Por las semanas de descanso, ese partido caería entre la semana N y la N+1 |
| **Con qué información** | Solo los resultados de los N partidos ya jugados por el equipo (nada posterior) |
| **Horizonte** | Lo que falta de la temporada regular: entre 4 y 13 partidos según el corte |
| **Uso previsto** | Orientar, con información parcial, qué equipos tendrían chances de llegar |
| **Costo de los errores** | Falso negativo (no detectar a un equipo que sí llega): se subestimaría a un candidato real. Falso positivo (marcar a uno que no llega): una falsa alarma. No hay un costo monetario definido; ambos errores se tratarían con el mismo peso y por eso la métrica principal sería el F1 de la clase «llega» |

### Objetivo general
Construir y evaluar modelos de aprendizaje automático que predigan si un equipo de la NFL llegará a los playoffs usando su rendimiento parcial en la temporada regular, y medir cómo cambia la calidad de la predicción según cuántos partidos se hayan jugado.

### Objetivos específicos
- Armar una tabla por equipo y temporada con variables calculadas en cuatro cortes de la temporada: 4, 6, 9 y 12 partidos jugados.
- Crear variables de rendimiento: porcentaje de victorias, puntos a favor y en contra, rendimiento en los últimos 4 partidos y partidos como local.
- Entrenar y comparar regresión logística, árbol de decisión, KNN y SVM, eligiendo sus hiperparámetros con validación interna.
- Validar respetando el tiempo: para cada temporada entre 2010 y 2025, entrenar con las temporadas anteriores y evaluar en esa temporada una sola vez (*walk-forward*, con temporadas completas).
- Comparar los modelos con precisión, recall, F1, exactitud y matriz de confusión, y contra dos referencias simples: un modelo que siempre predice la clase más frecuente y una regla por porcentaje de victorias.
- Analizar los errores (falsos negativos y falsos positivos) y el efecto de ajustar el umbral de decisión.
- Explicar cómo predice cada modelo y qué corte de la temporada sería el primero, entre los cuatro evaluados, en cumplir un criterio de predicción confiable fijado antes de ver resultados.

### Limitaciones previstas
Las variables usan solo resultados de partidos (sin mariscal de campo, lesiones ni calendario restante); con pocos partidos jugados quedaría mucha temporada por delante, por lo que se esperaría un techo de calidad en los cortes tempranos; y el cambio de 12 a 14 equipos clasificados en 2020 alteraría la proporción de equipos que llegan.

## 3. Origen de los datos

- **Dataset:** `games.csv` del repositorio **nflverse/nfldata** (https://github.com/nflverse/nfldata), con los resultados de todos los partidos de la NFL. Documentación en su `DATASETS.md`, que cita como origen histórico a `leesharpe/nfldata` (Lee Sharpe) y habitatring.com.
- **Fecha de adquisición:** 2 de noviembre de 2026. SHA-256 del archivo crudo: `ab502863ef21813a6ceb2f650b9ad1bed95667a27c6d6a996d8c3ea4b9016a06`.
- **Licencia:** el repositorio de origen no declara ninguna (revisado el 2 de noviembre de 2026). El archivo se usaría solo con fines académicos, citando la fuente.
- **Archivo crudo:** `data/raw/games.csv`, sin modificar (7.548 filas, 46 columnas, temporadas 1999 a 2026). Se usaron las temporadas 2002 a 2025 y solo partidos ya jugados (la temporada 2026, en curso, se dejó afuera de la evaluación).
- **Descripción completa, preprocesamiento y decisiones:** `docs/descripcion_dataset_y_origen.md`. **Diccionario de las 46 variables originales** (con las que se usan y las que se excluyen, y el motivo): `docs/diccionario_datos.md`.
- **Tratamiento de calidad:** sin faltantes en las variables construidas; equipos que cambiaron de ciudad unificados (OAK→LV, SD→LAC, STL→LA); un partido cancelado en 2022; 200 filas elegidas al azar recalculadas desde el dato crudo; sin duplicados por equipo, temporada y corte. Los valores extremos (por ejemplo, partidos con puntajes muy altos) serían resultados reales del juego y no se eliminaron.

### Variables predictoras
Cada modelo usaría una lista fija, definida en `nfl_playoffs/config.py`:

| Corte | Predictores |
|---|---|
| 4 partidos | `pct_victorias`, `puntos_favor_prom`, `puntos_contra_prom`, `partidos_local` |
| 6, 9 y 12 partidos | los mismos más `pct_victorias_ult4` (rendimiento en los últimos 4 partidos del corte) |

Se excluyen los identificadores (`season`, `team`), las constantes dentro de cada corte (`corte`, `partidos`) y las redundantes (`victorias`, `derrotas`, `dif_puntos_prom`). `pct_victorias_ult4` no se usa en el corte de 4 porque sería idéntica a `pct_victorias`.

## 4. Métricas, resultados y conclusiones

### Cómo se evaluó
- **Walk-forward por temporadas completas:** para cada temporada `y` entre 2010 y 2025, se entrena con 2002 hasta `y-1` y se evalúa en `y`, una sola vez (16 tramos, 512 equipos por corte). Las temporadas 2019 a 2025 ya se habían usado como prueba en un trabajo anterior, por lo que se informan por separado y la evaluación se considera **retrospectiva**, no una prueba nueva.
- **Hiperparámetros:** elegidos solo con datos de entrenamiento, con validación interna que usa las últimas 4 temporadas del entrenamiento (nunca se parte una temporada), y verificada automáticamente. La búsqueda está visible en el notebook `2.0` (secciones 3 y 7).
- **Sin filtración:** el escalado y el umbral se ajustan solo con el entrenamiento, dentro de un `Pipeline`.
- **Mismas observaciones y métricas** para todos los modelos y referencias. Métrica principal: **F1 de la clase «llega»**, junto con precisión, recall y exactitud.
- **Referencias:** (1) modelo que siempre responde «no llega» y (2) regla por `pct_victorias` con umbral elegido en el entrenamiento.
- **Criterio de «predicción confiable»** (fijado antes de ver resultados y sin cambios posteriores). Un corte sería suficiente si cumple todo sobre las mismas 16 temporadas: F1 medio ≥ 0,75; mejora ≥ 0,03 sobre la regla por % de victorias; supera a esa regla en al menos 11 de 16 temporadas; precisión media y recall medio ≥ 0,70 cada uno; desvío del F1 entre temporadas ≤ 0,10. La conclusión se referiría al primer corte, entre los cuatro evaluados, que lo cumpla, y no a un mínimo absoluto de partidos.

### F1 medio de la clase «llega», por modelo y corte
| Modelo | 4 partidos | 6 partidos | 9 partidos | 12 partidos |
|---|---|---|---|---|
| Siempre «no llega» | 0,000 | 0,000 | 0,000 | 0,000 |
| Regla por % de victorias | 0,687 | 0,712 | 0,764 | 0,811 |
| Regresión logística | 0,633 | 0,714 | 0,750 | 0,810 |
| Logística con umbral | 0,701 | 0,748 | 0,752 | 0,810 |
| Árbol de decisión | 0,611 | 0,696 | 0,733 | 0,776 |
| KNN | 0,577 | 0,700 | 0,752 | 0,791 |
| SVM (RBF) | 0,658 | 0,700 | 0,737 | 0,813 |

### Mejor modelo por corte
| Corte | Regla por % de victorias (F1) | Mejor modelo | F1 medio | Precisión media | Recall medio | Desvío del F1 |
|---|---|---|---|---|---|---|
| 4 | 0,687 | Logística con umbral | 0,701 | 0,644 | 0,778 | 0,103 |
| 6 | 0,712 | Logística con umbral | 0,748 | 0,712 | 0,795 | 0,086 |
| 9 | 0,764 | Logística con umbral | 0,752 | 0,743 | 0,769 | 0,074 |
| 12 | 0,811 | SVM (RBF) | 0,813 | 0,856 | 0,781 | 0,079 |

### Verificación del criterio (mejor modelo de cada corte)
| Corte | Modelo | F1 ≥ 0,75 | Mejora ≥ 0,03 sobre la regla | Supera a la regla en ≥ 11 de 16 | Precisión ≥ 0,70 | Recall ≥ 0,70 | Desvío ≤ 0,10 | ¿Cumple todo? |
|---|---|---|---|---|---|---|---|---|
| 4 | Logística con umbral | no | no (0,015) | no (10) | no | sí | no | no |
| 6 | Logística con umbral | no | sí (0,035) | sí (11) | sí | sí | sí | no |
| 9 | Logística con umbral | sí | no (-0,013) | no (5) | sí | sí | sí | no |
| 12 | SVM (RBF) | sí | no (0,002) | no (8) | sí | sí | sí | no |

### Modelo final
Como ningún corte cumpliría el criterio completo, el modelo final se eligió con una regla fijada de antemano: el de mayor F1 medio. Resultó **SVM con kernel RBF y 12 partidos** (`{'C': 10, 'gamma': 0.01}`). Sus resultados serían:

| Medida | Valor |
|---|---|
| F1 medio (16 temporadas) | 0,813 |
| Precisión media / recall medio | 0,856 / 0,781 |
| Desvío del F1 entre temporadas | 0,079 |
| F1 medio 2010–2018 / 2019–2025 (ya vistas) | 0,800 / 0,831 |
| F1 de la regla por % de victorias en el mismo corte | 0,811 |

**Matriz de confusión** (suma de las 16 temporadas, 512 equipos) y métricas por clase:

| | Predicho: no llega | Predicho: llega |
|---|---|---|
| **Real: no llega** | 280 | 28 |
| **Real: llega** | 45 | 159 |

| Clase | Precisión | Recall | F1 | Equipos reales |
|---|---|---|---|---|
| 1 (llega) | 0,850 | 0,779 | 0,813 | 204 |
| 0 (no llega) | 0,862 | 0,909 | 0,885 | 308 |

Exactitud global: 0,857. Los errores se repartirían así: 45 falsos negativos (equipos que llegaron y no se detectaron) y 28 falsas alarmas. Habría más falsos negativos que falsos positivos, es decir, el modelo sería algo más cauto que optimista. Las figuras están en `reports/figures/` y en el notebook `2.0`.

### Conclusiones
**Resultados** (con los datos y la evaluación descriptos)
- El F1 medio de los mejores modelos subiría con la cantidad de partidos jugados: de 0,701 con 4 partidos a 0,813 con 12.
- El criterio de confiabilidad **no se cumpliría completo en ningún corte**. Con 12 partidos se cumplirían los umbrales de F1, precisión, recall y desvío, pero no la mejora de 0,03 sobre la regla simple ni las 11 temporadas por encima de ella.
- Los modelos **no superarían de forma clara a la regla por % de victorias**. La única mejora de al menos 0,03 aparecería en el corte de 6 partidos con la logística con umbral (0,035 de diferencia en F1 y mejor que la regla en 11 de 16 temporadas), pero su F1 medio (0,748) quedaría por debajo del 0,75 exigido.
- Con 12 partidos, los resultados de 2010–2018 y de 2019–2025 serían parecidos (0,800 y 0,831).

**Hipótesis (no verificadas)**
- La regla simple sería difícil de superar porque casi toda la información útil de estas variables podría estar resumida en el récord de victorias.
- La mejora con más partidos podría deberse a que el récord parcial se parecería cada vez más al récord final de la temporada.
- La ventaja de la logística con umbral en el corte de 6 podría deberse al ajuste del umbral más que al tipo de modelo.

## 5. Limitaciones, alcance y trabajo futuro

**Limitaciones**
- Evaluación **retrospectiva** con 16 temporadas; las temporadas 2019 a 2025 ya se habían usado como prueba y la exploración inicial usó todas las temporadas. Los resultados no equivalen a una prueba completamente nueva.
- Los cuatro cortes de una misma temporada están correlacionados entre sí, y los equipos dentro de una temporada también.
- Las variables salen solo de resultados de partidos: no hay lesiones, calidad del mariscal de campo ni dificultad del calendario restante.
- Las diferencias entre modelos serían chicas frente a la variabilidad entre temporadas (desvío del F1 cercano a 0,08), por lo que no habría evidencia suficiente para decir que un modelo es mejor que otro.
- Las relaciones encontradas serían asociaciones, no causas.

**Alcance:** orientar con información parcial qué equipos tendrían más chances de llegar; no sería una herramienta para apuestas ni para decisiones con consecuencias económicas.

**Trabajo futuro:** incorporar el calendario restante, el mariscal de campo y las lesiones; evaluar con temporadas futuras (por ejemplo, la 2026 una vez terminada); probar un modelo que prediga la probabilidad calibrada de llegar en vez de solo la clase; y comparar con modelos de otros deportes.

### Uso del modelo guardado con casos nuevos
El modelo final está en `models/modelo_final.joblib` (diccionario con el `Pipeline`, la lista de predictores y el umbral). En el notebook `2.0` (sección 10) se muestra con casos sintéticos y con los equipos de la temporada 2026 en curso (modelo ilustrativo de 6 partidos, `models/modelo_2026_ilustrativo.joblib`). Ejemplo mínimo:

```python
import joblib, pandas as pd
from nfl_playoffs.modelado import predecir

modelo = joblib.load("models/modelo_final.joblib")
casos = pd.DataFrame({
    "pct_victorias": [0.75, 0.33],
    "puntos_favor_prom": [26.0, 17.5],
    "puntos_contra_prom": [19.0, 24.0],
    "partidos_local": [6, 5],
    "pct_victorias_ult4": [0.75, 0.25],
}, index=["equipo_ficticio_A", "equipo_ficticio_B"])
print(predecir(modelo, casos))   # prob_llega (vacía en SVM, que no entrega probabilidades) y prediccion
```

## 6. Estructura del repositorio y orden de lectura

```
├── README.md                 <- este documento
├── requirements.txt          <- dependencias con versiones
├── data/
│   ├── raw/games.csv         <- dato original, sin modificar
│   ├── interim/              <- tabla por equipo y partido
│   ├── processed/            <- variables por corte (4, 6, 9, 12) y archivo combinado
│   └── external/             <- (vacía, no se usaron datos externos)
├── docs/
│   ├── descripcion_dataset_y_origen.md
│   └── diccionario_datos.md  <- las 46 variables originales y las construidas
├── models/                   <- modelo_final.joblib y modelo_2026_ilustrativo.joblib
├── notebooks/
│   ├── 1.0-trg-carga-y-exploracion-de-datos.ipynb
│   └── 2.0-trg-modelado-y-evaluacion.ipynb
├── nfl_playoffs/             <- código reutilizable (config, features, validacion, modelado)
├── references/               <- (vacía)
├── reports/                  <- tablas de resultados (CSV, JSON, Markdown) y figures/
└── video/video.md            <- enlace al video
```

**Orden sugerido:** (1) este README; (2) `docs/descripcion_dataset_y_origen.md` y `docs/diccionario_datos.md`; (3) notebook `1.0` (datos y exploración); (4) notebook `2.0` (modelado, evaluación y conclusiones); (5) `reports/` y `models/`.

## 7. Cómo reproducir

Requiere Python 3.13 (probado con 3.13.18) o una versión reciente compatible con `requirements.txt`.

```bash
python -m venv .venv
source .venv/bin/activate            # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m nfl_playoffs.dataset       # regenera data/interim y data/processed desde data/raw
jupyter nbconvert --to notebook --execute --inplace notebooks/1.0-trg-carga-y-exploracion-de-datos.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/2.0-trg-modelado-y-evaluacion.ipynb
```

El notebook `2.0` tarda alrededor de 2 minutos y regenera `reports/` y `models/`. La semilla es fija (`42`), por lo que los números del README, de los notebooks y del video provienen de la misma ejecución.

## 8. Video

El video de presentación (con subtítulos) estaría en el enlace de `video/video.md`.

**Enlace:** https://youtu.be/3yBZDt3fh5I
