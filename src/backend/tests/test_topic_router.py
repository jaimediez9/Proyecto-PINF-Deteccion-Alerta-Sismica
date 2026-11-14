"""Pruebas de la lógica pura de enrutado de topics (app/services/topic_router.py).

Se ejecutan sin red ni credenciales: comprueban únicamente la decisión de a qué
topics de FCM publicar dado un seísmo.
"""

import sys
from pathlib import Path

# Permite importar el paquete 'app' al ejecutar pytest desde cualquier carpeta.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.topic_router import (  # noqa: E402
    build_conditions,
    celda,
    compute_topics,
    magnitude_topics,
    zona_topic,
)

# Evento real del servicio del ROA (roa2026whof): lat 37.0959, lon -4.1395.
LAT_REAL, LON_REAL = 37.0959, -4.1395


# --- magnitud ---

def test_ejemplo_del_pdf_magnitud_3_4():
    """Ejemplo de la guía: magnitud 3.4 -> topics 1, 2 y 3."""
    assert magnitude_topics(3.4) == ["mg_mayor_1", "mg_mayor_2", "mg_mayor_3"]


def test_magnitud_intermedia():
    assert magnitude_topics(2.0) == ["mg_mayor_1", "mg_mayor_2"]


def test_magnitud_bajo_el_minimo_no_avisa():
    assert magnitude_topics(0.5) == []


def test_umbral_es_inclusivo():
    """El límite cuenta: magnitud igual al nivel -> se incluye ese nivel."""
    assert magnitude_topics(1.0) == ["mg_mayor_1"]
    assert magnitude_topics(2.999) == ["mg_mayor_1", "mg_mayor_2"]


def test_magnitud_negativa_no_avisa():
    assert magnitude_topics(-1.0) == []


def test_niveles_configurables():
    assert magnitude_topics(5.0, levels=(2, 4)) == ["mg_mayor_2", "mg_mayor_4"]


# --- rejilla de zonas (celda / zona_topic) ---

def test_celda_evento_real():
    assert celda(LAT_REAL, LON_REAL, 0.25) == (148, -17)


def test_zona_topic_evento_real():
    assert zona_topic(LAT_REAL, LON_REAL, 0.25) == "zona_148_-17"


def test_floor_y_no_truncamiento_con_longitud_negativa():
    """Al oeste de Greenwich hay que usar floor, no truncar.

    int(-0.4) == 0, pero la longitud -0.1 está en la celda j = -1.
    """
    assert celda(0.0, -0.1, 0.25) == (0, -1)
    assert int(-0.1 / 0.25) == 0  # lo que daría truncar (mal)


def test_frontera_suroeste_es_inclusiva():
    """La esquina SW pertenece a su propia celda: [i*paso, (i+1)*paso)."""
    assert celda(37.0, -4.25, 0.25) == (148, -17)


def test_frontera_noreste_es_exclusiva():
    """El borde superior entra en la celda siguiente."""
    assert celda(37.25, -4.0, 0.25) == (149, -16)


def test_paso_configurable():
    assert celda(LAT_REAL, LON_REAL, 0.5) == (74, -9)
    assert zona_topic(LAT_REAL, LON_REAL, 0.5) == "zona_74_-9"


# --- compute_topics ---

def test_compute_topics_separado():
    topics = compute_topics(3.4, LAT_REAL, LON_REAL, paso=0.25)
    assert topics == ["mg_mayor_1", "mg_mayor_2", "mg_mayor_3", "zona_148_-17"]


def test_compute_topics_bajo_el_minimo():
    """Por debajo del nivel mínimo no hay topics de magnitud, pero sí de zona."""
    assert compute_topics(0.5, LAT_REAL, LON_REAL, paso=0.25) == ["zona_148_-17"]


def test_compute_topics_combinado():
    topics = compute_topics(3.4, LAT_REAL, LON_REAL, paso=0.25, combined=True)
    assert topics == [
        "mg_mayor_1_zona_148_-17",
        "mg_mayor_2_zona_148_-17",
        "mg_mayor_3_zona_148_-17",
    ]


# --- build_conditions (vía recomendada: AND real con condiciones de FCM) ---

def test_condicion_ejemplo_magnitud_3_4():
    assert build_conditions(3.4, LAT_REAL, LON_REAL, paso=0.25) == [
        "('mg_mayor_1' in topics || 'mg_mayor_2' in topics || 'mg_mayor_3' in topics)"
        " && 'zona_148_-17' in topics"
    ]


def test_condicion_dos_niveles():
    assert build_conditions(2.0, LAT_REAL, LON_REAL, paso=0.25) == [
        "('mg_mayor_1' in topics || 'mg_mayor_2' in topics) && 'zona_148_-17' in topics"
    ]


def test_condicion_un_solo_nivel_sin_parentesis():
    assert build_conditions(1.0, LAT_REAL, LON_REAL, paso=0.25) == [
        "'mg_mayor_1' in topics && 'zona_148_-17' in topics"
    ]


def test_condicion_magnitud_bajo_el_minimo():
    assert build_conditions(0.5, LAT_REAL, LON_REAL, paso=0.25) == []


def test_condicion_se_trocea_al_pasarse_de_max_topics():
    """Con 6 niveles y max_topics=5 -> 4 niveles por tanda -> dos condiciones."""
    condiciones = build_conditions(
        9.9, LAT_REAL, LON_REAL, levels=(1, 2, 3, 4, 5, 6), paso=0.25
    )
    assert condiciones == [
        "('mg_mayor_1' in topics || 'mg_mayor_2' in topics || 'mg_mayor_3' in topics"
        " || 'mg_mayor_4' in topics) && 'zona_148_-17' in topics",
        "('mg_mayor_5' in topics || 'mg_mayor_6' in topics) && 'zona_148_-17' in topics",
    ]


def test_condicion_respeta_max_topics_configurable():
    """Cada condición usa como mucho 'max_topics' topics (niveles + zona)."""
    condiciones = build_conditions(
        9.9, LAT_REAL, LON_REAL, levels=(1, 2, 3, 4, 5), paso=0.25, max_topics=3
    )
    for cond in condiciones:
        assert cond.count("'mg_mayor_") + cond.count("'zona_") <= 3
