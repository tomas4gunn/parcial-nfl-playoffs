"""Parámetros del proyecto."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data" / "raw"
INTERIM = RAIZ / "data" / "interim"
PROCESSED = RAIZ / "data" / "processed"
FIGURAS = RAIZ / "reports" / "figures"

# Temporadas con 32 equipos (desde 2002) y ya terminadas (la 2026 está en curso)
TEMPORADA_MIN = 2002
TEMPORADA_MAX = 2025

# Cortes de la temporada: cantidad de partidos YA jugados por el equipo
CORTES = (4, 6, 9, 12)

# Equipos que cambiaron de ciudad: se unifican bajo el nombre actual
MUDANZAS = {"OAK": "LV", "SD": "LAC", "STL": "LA"}

# --- Selección de predictores por corte (decidida antes de modelar, no se cambia mirando resultados) ---
IDENTIFICADORES = ["season", "team"]          # identifican la fila, no son predictores
OBJETIVO = "llega_playoffs"
# Constantes dentro de un modelo por corte: no distinguen equipos
CONSTANTES_POR_CORTE = ["corte", "partidos"]
# Redundantes: se pueden reconstruir exactamente con los predictores elegidos
REDUNDANTES = ["victorias", "derrotas", "dif_puntos_prom"]
_BASE = ["pct_victorias", "puntos_favor_prom", "puntos_contra_prom", "partidos_local"]
PREDICTORES = {n: _BASE + (["pct_victorias_ult4"] if n > 4 else []) for n in CORTES}

# --- Validación (ver nfl_playoffs/validacion.py) ---
PRIMERA_VALIDACION = 2010   # primer año que se usa para validar en el walk-forward
VISTAS_EN_SEMANA_6 = range(2019, 2026)

MODELOS_DIR = RAIZ / "models"
REPORTES = RAIZ / "reports"
