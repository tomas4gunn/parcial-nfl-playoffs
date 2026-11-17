"""Particiones por temporada completa (nunca se parte una temporada entre entrenamiento y validación)."""
import numpy as np

from nfl_playoffs.config import PRIMERA_VALIDACION, TEMPORADA_MAX, TEMPORADA_MIN


def tramos_walk_forward(primera=PRIMERA_VALIDACION, ultima=TEMPORADA_MAX, inicio=TEMPORADA_MIN):
    """Para cada año y: entrena con inicio..y-1 y valida en y. Devuelve [(años_entrenamiento, año_validación)]."""
    return [(list(range(inicio, y)), y) for y in range(primera, ultima + 1)]


def particiones_internas(df, años_entrenamiento, n_particiones=4):
    """Validación cruzada INTERNA para elegir hiperparámetros, armada a partir de los años (no de posiciones).

    Ventana creciente: la validación son las últimas `n_particiones` temporadas del entrenamiento, una por vez,
    y se entrena con todas las anteriores. Devuelve índices de filas de `df`, utilizables como `cv=` en scikit-learn.
    """
    años = sorted(años_entrenamiento)
    assert len(años) > n_particiones, "no alcanzan temporadas para las particiones internas"
    temp = df["season"].to_numpy()
    divisiones = []
    for y in años[-n_particiones:]:
        tr = np.where(np.isin(temp, [a for a in años if a < y]))[0]
        va = np.where(temp == y)[0]
        divisiones.append((tr, va))
    return divisiones


def verificar_particiones(df, divisiones):
    """Comprueba que ninguna temporada aparece a ambos lados y que el entrenamiento es anterior a la validación."""
    temp = df["season"].to_numpy()
    for tr, va in divisiones:
        s_tr, s_va = set(temp[tr]), set(temp[va])
        assert not (s_tr & s_va), f"temporadas en ambos lados: {sorted(s_tr & s_va)}"
        assert max(s_tr) < min(s_va), "el entrenamiento no es anterior a la validación"
    return True
