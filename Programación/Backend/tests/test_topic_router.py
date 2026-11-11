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
    compute_topics,
    magnitude_topics,
    zone_topic,
)


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


def test_slug_de_zona_quita_acentos_y_espacios():
    assert zone_topic("Golfo de Cádiz") == "zona_golfo_de_cadiz"


def test_compute_topics_separado():
    topics = compute_topics(3.4, "Golfo de Cádiz")
    assert topics == ["mg_mayor_1", "mg_mayor_2", "mg_mayor_3", "zona_golfo_de_cadiz"]


def test_compute_topics_sin_zona():
    assert compute_topics(2.5, None) == ["mg_mayor_1", "mg_mayor_2"]


def test_compute_topics_combinado():
    topics = compute_topics(3.4, "Golfo de Cádiz", combined=True)
    assert topics == [
        "mg_mayor_1_zona_golfo_de_cadiz",
        "mg_mayor_2_zona_golfo_de_cadiz",
        "mg_mayor_3_zona_golfo_de_cadiz",
    ]


def test_combinado_sin_zona_no_avisa():
    assert compute_topics(3.4, None, combined=True) == []


# --- build_conditions (vía recomendada: AND real con condiciones de FCM) ---

def test_condicion_ejemplo_magnitud_3_4():
    assert build_conditions(3.4, "Golfo de Cádiz") == [
        "('mg_mayor_1' in topics || 'mg_mayor_2' in topics || 'mg_mayor_3' in topics)"
        " && 'zona_golfo_de_cadiz' in topics"
    ]


def test_condicion_dos_niveles():
    assert build_conditions(2.0, "Golfo de Cádiz") == [
        "('mg_mayor_1' in topics || 'mg_mayor_2' in topics) && 'zona_golfo_de_cadiz' in topics"
    ]


def test_condicion_un_solo_nivel_sin_parentesis():
    assert build_conditions(1.0, "Golfo de Cádiz") == [
        "'mg_mayor_1' in topics && 'zona_golfo_de_cadiz' in topics"
    ]


def test_condicion_magnitud_bajo_el_minimo():
    assert build_conditions(0.5, "Golfo de Cádiz") == []


def test_condicion_sin_zona():
    assert build_conditions(3.4, None) == []


def test_condicion_se_trocea_al_pasarse_de_max_topics():
    """Con 6 niveles y max_topics=5 -> 4 niveles por tanda -> dos condiciones."""
    condiciones = build_conditions(9.9, "Golfo de Cádiz", levels=(1, 2, 3, 4, 5, 6))
    assert condiciones == [
        "('mg_mayor_1' in topics || 'mg_mayor_2' in topics || 'mg_mayor_3' in topics"
        " || 'mg_mayor_4' in topics) && 'zona_golfo_de_cadiz' in topics",
        "('mg_mayor_5' in topics || 'mg_mayor_6' in topics) && 'zona_golfo_de_cadiz' in topics",
    ]


def test_condicion_respeta_max_topics_configurable():
    """Cada condición usa como mucho 'max_topics' topics (niveles + zona)."""
    condiciones = build_conditions(9.9, "Golfo de Cádiz", levels=(1, 2, 3, 4, 5), max_topics=3)
    for cond in condiciones:
        assert cond.count("'mg_mayor_") + cond.count("'zona_") <= 3
