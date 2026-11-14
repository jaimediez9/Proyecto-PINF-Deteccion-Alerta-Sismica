"""Pruebas del adapter de FCM (app/services/fcm.py).

No tocan la red ni Firebase: usan el enviador falso.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.fcm import (  # noqa: E402
    ConfiguracionFCM,
    EnviadorFCMFalso,
    avisar_de,
    construir_mensaje,
)
from app.services.parser_json import ParserJSON  # noqa: E402
from app.services.topic_router import build_conditions  # noqa: E402

FIXTURE = Path(__file__).parent / "fixtures" / "ultimo.json"


def _terremoto_real():
    return ParserJSON().parsear_evento(json.loads(FIXTURE.read_text(encoding="utf-8")))


# --- construcción del mensaje ---

def test_el_mensaje_lleva_la_condicion():
    terremoto = _terremoto_real()
    mensaje = construir_mensaje("'mg_mayor_2' in topics && 'zona_148_-17' in topics", terremoto)
    assert mensaje["message"]["condition"] == "'mg_mayor_2' in topics && 'zona_148_-17' in topics"


def test_el_aviso_dice_magnitud_zona_y_hora():
    """RF-19: el aviso incluye magnitud, zona y hora."""
    mensaje = construir_mensaje("c", _terremoto_real())
    cuerpo = mensaje["message"]["notification"]["body"]
    assert "M2.0" in cuerpo
    assert "Spain" in cuerpo          # la zona (region del ROA)
    assert "UTC" in cuerpo


def test_el_titulo_no_sugiere_alerta_temprana():
    """RS-01: nada puede dar a entender que la app se adelanta al terremoto."""
    mensaje = construir_mensaje("c", _terremoto_real())
    titulo = mensaje["message"]["notification"]["title"]
    for palabra in ("temprana", "aviso previo", "antes", "predic"):
        assert palabra not in titulo.lower()


def test_los_data_son_cadenas_y_usan_los_nombres_del_modelo():
    """FCM exige que todos los valores de 'data' sean cadenas."""
    data = construir_mensaje("c", _terremoto_real())["message"]["data"]
    assert data["identificador"] == "roa2026whof"
    assert data["magnitud"] == "2.0"
    assert data["revisado"] == "false"
    assert all(isinstance(v, str) for v in data.values())


def test_condicion_vacia_lanza_error():
    try:
        construir_mensaje("", _terremoto_real())
    except ValueError:
        pass
    else:
        raise AssertionError("esperaba ValueError con la condición vacía")


# --- envío (con el enviador falso) ---

def test_enviador_falso_guarda_los_mensajes():
    enviador = EnviadorFCMFalso()
    assert enviador.enviar({"message": {"condition": "x"}}) == "falso-1"
    assert enviador.enviar({"message": {"condition": "y"}}) == "falso-2"
    assert len(enviador.enviados) == 2


def test_avisar_de_manda_las_condiciones_del_terremoto():
    terremoto = _terremoto_real()
    enviador = EnviadorFCMFalso()
    ids = avisar_de(terremoto, enviador)

    esperadas = build_conditions(terremoto.magnitud, terremoto.latitud, terremoto.longitud)
    assert len(ids) == len(esperadas) == len(enviador.enviados)
    condiciones = [m["message"]["condition"] for m in enviador.enviados]
    assert condiciones == esperadas
    assert condiciones == [
        "('mg_mayor_1' in topics || 'mg_mayor_2' in topics) && 'zona_148_-17' in topics"
    ]


# --- configuración ---

def test_configuracion_desde_entorno():
    cfg = ConfiguracionFCM.desde_entorno(
        {"FIREBASE_PROJECT_ID": "p", "GOOGLE_APPLICATION_CREDENTIALS": "/ruta.json"}
    )
    assert cfg.project_id == "p"
    assert cfg.ruta_credenciales == "/ruta.json"


def test_configuracion_falla_si_faltan_variables():
    try:
        ConfiguracionFCM.desde_entorno({})
    except RuntimeError:
        pass
    else:
        raise AssertionError("esperaba RuntimeError sin variables de entorno")
