"""Modelos, búsqueda de hiperparámetros y evaluación walk-forward por temporada completa.

Reglas (fijadas antes de ver resultados, ver README):
- Un modelo por corte (4, 6, 9 y 12 partidos), con la lista de predictores de config.PREDICTORES.
- Para cada temporada de evaluación y: se entrena con 2002..y-1 y se evalúa en y UNA sola vez.
- Los hiperparámetros se eligen SOLO con el entrenamiento, con validación interna por temporadas completas.
- El escalado vive dentro de un Pipeline (se ajusta solo con el entrenamiento de cada partición).
"""
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from .config import OBJETIVO, PREDICTORES
from .validacion import particiones_internas, tramos_walk_forward, verificar_particiones

SEMILLA = 42
UMBRALES = np.round(np.arange(0.30, 0.71, 0.05), 2)

# Criterio de "predicción confiable" (fijado antes de ejecutar, no se modifica)
CRITERIO = {
    "f1_medio_min": 0.75,
    "mejora_min_sobre_regla": 0.03,
    "temporadas_mejor_que_regla_min": 11,
    "precision_media_min": 0.70,
    "recall_medio_min": 0.70,
    "desvio_f1_max": 0.10,
}


def modelos():
    """Cada modelo con su preparación propia y su grilla de hiperparámetros."""
    return {
        "logistica": (Pipeline([("esc", StandardScaler()), ("m", LogisticRegression(max_iter=1000))]),
                      {"m__C": [0.01, 0.1, 1, 10, 100]}),
        "arbol": (DecisionTreeClassifier(random_state=SEMILLA),  # no necesita escalado
                  {"max_depth": [2, 3, 4, 5, 6], "min_samples_leaf": [5, 10, 20]}),
        "knn": (Pipeline([("esc", StandardScaler()), ("m", KNeighborsClassifier())]),
                {"m__n_neighbors": [5, 9, 15, 25, 35, 51], "m__weights": ["uniform", "distance"]}),
        "svm": (Pipeline([("esc", StandardScaler()), ("m", SVC(kernel="rbf"))]),
                {"m__C": [0.1, 1, 10], "m__gamma": ["scale", 0.1, 0.01]}),
    }


def metricas(y, pred):
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * p * r / (p + r) if p + r else 0.0
    return {"precision": p, "recall": r, "f1": f1, "exactitud": (tp + tn) / len(y), "VP": tp, "FP": fp, "FN": fn, "VN": tn}


def umbral_regla(df_train, col="pct_victorias"):
    """Regla simple: 'llega' si pct_victorias >= umbral. El umbral se elige solo con el entrenamiento (máx. F1)."""
    cand = np.sort(df_train[col].unique())
    mejor, mejor_f1 = cand[0], -1
    for u in cand:
        f = f1_score(df_train[OBJETIVO], (df_train[col] >= u).astype(int), zero_division=0)
        if f > mejor_f1:
            mejor, mejor_f1 = u, f
    return mejor


def buscar(nombre, df_train, años_train, cols, n_part=4):
    """Elige hiperparámetros con validación interna por temporadas completas (solo entrenamiento)."""
    est, grilla = modelos()[nombre]
    divisiones = particiones_internas(df_train, años_train, n_part)
    verificar_particiones(df_train, divisiones)
    gs = GridSearchCV(est, grilla, scoring="f1", cv=divisiones, n_jobs=1, refit=True)
    gs.fit(df_train[cols], df_train[OBJETIVO])
    return gs, divisiones


def umbral_logistica(gs, df_train, divisiones, cols):
    """Umbral de decisión para la logística, elegido con las predicciones de la validación interna."""
    ps, ys = [], []
    for tr, va in divisiones:
        est = clone(gs.best_estimator_)
        est.fit(df_train.iloc[tr][cols], df_train.iloc[tr][OBJETIVO])
        ps.append(est.predict_proba(df_train.iloc[va][cols])[:, 1]); ys.append(df_train.iloc[va][OBJETIVO].to_numpy())
    p, y = np.concatenate(ps), np.concatenate(ys)
    f = [f1_score(y, (p >= u).astype(int), zero_division=0) for u in UMBRALES]
    return float(UMBRALES[int(np.argmax(f))])



def evaluar_corte(tabla, corte, primera=2010, ultima=2025):
    """Walk-forward para un corte. Devuelve (metricas por temporada y modelo, hiperparámetros elegidos)."""
    cols = PREDICTORES[corte]
    filas, hp = [], []
    for años_tr, y in tramos_walk_forward(primera, ultima):
        tr = tabla[tabla.season.isin(años_tr)].reset_index(drop=True)
        te = tabla[tabla.season == y]
        assert not set(tr.season) & set(te.season)
        # referencias simples
        d = DummyClassifier(strategy="most_frequent").fit(tr[cols], tr[OBJETIVO])
        filas.append({"corte": corte, "season": y, "modelo": "siempre_no_llega", **metricas(te[OBJETIVO], d.predict(te[cols]))})
        u = umbral_regla(tr)
        filas.append({"corte": corte, "season": y, "modelo": "regla_pct_victorias",
                      **metricas(te[OBJETIVO], (te.pct_victorias >= u).astype(int))})
        hp.append({"corte": corte, "season": y, "modelo": "regla_pct_victorias", "hiperparametros": f"umbral={u:.3f}"})
        for nombre in modelos():
            gs, div = buscar(nombre, tr, años_tr, cols)
            filas.append({"corte": corte, "season": y, "modelo": nombre, **metricas(te[OBJETIVO], gs.predict(te[cols]))})
            hp.append({"corte": corte, "season": y, "modelo": nombre, "hiperparametros": str(gs.best_params_)})
            if nombre == "logistica":
                um = umbral_logistica(gs, tr, div, cols)
                pr = (gs.predict_proba(te[cols])[:, 1] >= um).astype(int)
                filas.append({"corte": corte, "season": y, "modelo": "logistica_umbral", **metricas(te[OBJETIVO], pr)})
                hp.append({"corte": corte, "season": y, "modelo": "logistica_umbral",
                           "hiperparametros": f"{gs.best_params_}, umbral={um}"})
    return pd.DataFrame(filas), pd.DataFrame(hp)


def resumir(met):
    """Promedios y desvío del F1 entre temporadas, por corte y modelo (todas, 2010-2018 y 2019-2025)."""
    def agg(d):
        return pd.Series({"precision_media": d.precision.mean(), "recall_medio": d.recall.mean(), "f1_medio": d.f1.mean(),
                          "f1_desvio": d.f1.std(ddof=1), "exactitud_media": d.exactitud.mean()})
    out = met.groupby(["corte", "modelo"]).apply(agg, include_groups=False)
    out["f1_2010_2018"] = met[met.season < 2019].groupby(["corte", "modelo"]).f1.mean()
    out["f1_2019_2025"] = met[met.season >= 2019].groupby(["corte", "modelo"]).f1.mean()
    return out.reset_index()


def aplicar_criterio(met, res):
    """Evalúa el criterio fijado de antemano para cada corte y modelo (contra la regla por % de victorias)."""
    filas = []
    for (corte, modelo), r in res.set_index(["corte", "modelo"]).iterrows():
        if modelo in ("siempre_no_llega", "regla_pct_victorias"):
            continue
        regla = met[(met.corte == corte) & (met.modelo == "regla_pct_victorias")].set_index("season").f1
        m = met[(met.corte == corte) & (met.modelo == modelo)].set_index("season").f1
        regla_media = regla.mean()
        c = {
            "f1_medio": r.f1_medio >= CRITERIO["f1_medio_min"],
            "mejora_sobre_regla": (r.f1_medio - regla_media) >= CRITERIO["mejora_min_sobre_regla"],
            "temporadas_mejor": int((m > regla).sum()) >= CRITERIO["temporadas_mejor_que_regla_min"],
            "precision": r.precision_media >= CRITERIO["precision_media_min"],
            "recall": r.recall_medio >= CRITERIO["recall_medio_min"],
            "desvio": r.f1_desvio <= CRITERIO["desvio_f1_max"],
        }
        filas.append({"corte": corte, "modelo": modelo, "f1_medio": r.f1_medio, "f1_regla": regla_media,
                      "mejora_vs_regla": r.f1_medio - regla_media, "temporadas_mejor_que_regla": int((m > regla).sum()),
                      **{f"cumple_{k}": v for k, v in c.items()}, "cumple_todo": all(c.values())})
    return pd.DataFrame(filas)


def ajustar_final(nombre, tabla, corte, ultimas=4):
    """Ajuste del modelo definitivo con TODAS las temporadas (2002-2025).

    Los hiperparámetros se eligen con validación interna por temporadas completas (últimas `ultimas` temporadas).
    Devuelve un diccionario listo para guardar con joblib y para predecir casos nuevos.
    """
    cols = PREDICTORES[corte]
    años = sorted(tabla.season.unique())
    base = "logistica" if nombre == "logistica_umbral" else nombre
    gs, div = buscar(base, tabla.reset_index(drop=True), años, cols, n_part=ultimas)
    umbral = umbral_logistica(gs, tabla.reset_index(drop=True), div, cols) if nombre == "logistica_umbral" else None
    return {"modelo": nombre, "corte": corte, "predictores": cols, "pipeline": gs.best_estimator_,
            "umbral": umbral, "hiperparametros": gs.best_params_}


def predecir(m, casos):
    """Aplica el pipeline YA ajustado a casos nuevos (mismas columnas; no se recalculan escalas)."""
    X = casos[m["predictores"]]
    est = m["pipeline"]
    if hasattr(est, "predict_proba"):
        p = est.predict_proba(X)[:, 1]
        clase = (p >= (m["umbral"] if m["umbral"] is not None else 0.5)).astype(int)
    else:
        p, clase = np.full(len(X), np.nan), est.predict(X)
    return pd.DataFrame({"prob_llega": p, "prediccion": clase}, index=casos.index)
