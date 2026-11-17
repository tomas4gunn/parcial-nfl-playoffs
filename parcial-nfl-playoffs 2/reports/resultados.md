# Resultados (generado por el notebook 2.0)

| Corte | F1 regla % victorias | Mejor modelo | F1 medio | Precisión | Recall | Desvío del F1 |
|---|---|---|---|---|---|---|
| 4 | 0.687 | Logística con umbral | 0.701 | 0.644 | 0.778 | 0.103 |
| 6 | 0.712 | Logística con umbral | 0.748 | 0.712 | 0.795 | 0.086 |
| 9 | 0.764 | Logística con umbral | 0.752 | 0.743 | 0.769 | 0.074 |
| 12 | 0.811 | SVM (RBF) | 0.813 | 0.856 | 0.781 | 0.079 |

**Resultados (con los datos y la evaluación descriptos)**
- El modelo final sería **SVM (RBF)** con el corte de **12 partidos**: F1 medio 0.813, precisión media 0.856, recall medio 0.781 y desvío del F1 entre temporadas 0.079. La regla por % de victorias obtendría 0.811 en ese corte.
- El criterio de confiabilidad no se cumpliría completo en ningún corte; los valores se informan tal cual.
- En 2010 a 2018 el F1 medio del modelo final sería 0.800 y en 2019 a 2025 (ya vistas) 0.831.
- Cortes en que el mejor modelo superaría a la regla en al menos 0.03 de F1: 6.

**Hipótesis (no verificadas)**
- La mejora sobre la regla por % de victorias aparecería solo en el corte indicado y con la variante de logística con umbral, por lo que podría deberse al ajuste del umbral más que al tipo de modelo; con 16 temporadas no alcanzaría para afirmarlo.
- Una parte de la mejora entre cortes podría deberse a que, con más partidos jugados, el récord se parecería más al resultado final de la temporada.

**Limitaciones**
- Evaluación retrospectiva, con 16 temporadas (512 equipos por corte) y los cuatro cortes correlacionados entre sí.
- Las temporadas 2019 a 2025 ya se habían usado como prueba y la exploración usó todas las temporadas.
- Las variables solo salen de resultados de partidos (sin lesiones, mariscal de campo ni calendario restante).
- La predicción en un tramo no probaría que la regla elegida funcione en el futuro, y las asociaciones no serían causas.
