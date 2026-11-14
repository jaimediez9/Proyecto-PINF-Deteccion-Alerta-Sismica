"""Pruebas del parser del JSON del ROA (app/services/parser_json.py).

Se ejecutan sin red: el caso principal usa una respuesta REAL del servicio,
grabada en tests/fixtures/ultimo.json.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Permite importar el paquete 'app' al ejecutar pytest desde cualquier carpeta.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.models.terremoto import Terremoto  # noqa: E402
from app.services.parser_json import ParserJSON  # noqa: E402

FIXTURE = Path(__file__).parent / "fixtures" / "ultimo.json"


def _cargar_fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


# --- contra una respuesta REAL del servicio ---

def test_parsea_el_evento_real():
    """Evento real roa2026whof del servicio del ROA."""
    t = ParserJSON().parsear_evento(_cargar_fixture())
    assert isinstance(t, Terremoto)
    assert t.identificador == "roa2026whof"
    assert t.latitud == 37.0959
    assert t.longitud == -4.1395
    assert t.profundidad == 10.0
    assert t.magnitud == 2.0
    assert t.tipoMagnitud == "M"
    assert t.zona == "Spain"


def test_la_hora_es_utc_y_aware():
    t = ParserJSON().parsear_evento(_cargar_fixture())
    assert t.fechaHoraUTC == datetime(2026, 11, 14, 4, 54, 56, 895000, tzinfo=timezone.utc)
    assert t.fechaHoraUTC.tzinfo is not None
    assert t.ultimaModificacion == datetime(2026, 11, 14, 4, 58, 12, tzinfo=timezone.utc)


def test_evento_automatico_no_esta_revisado():
    """mode=automatic -> revisado False (la nota del servicio lo confirma)."""
    fixture = _cargar_fixture()
    assert fixture["resumen"]["mode"] == "automatic"
    assert ParserJSON().parsear_evento(fixture).revisado is False


# --- casos de borde (dicts a mano) ---

def test_evento_manual_esta_revisado():
    t = Terremoto.desde_resumen({
        "id": "x", "time": "2026-01-01T00:00:00Z", "lat": 1.0, "lon": 2.0,
        "depth": 5.0, "mag": 3.0, "mag_type": "ML", "region": "Spain",
        "mode": "manual", "updated": "2026-01-01T00:01:00Z",
    })
    assert t.revisado is True


def test_campos_opcionales_ausentes():
    """zona/tipoMagnitud/ultimaModificacion pueden faltar o ser null."""
    t = Terremoto.desde_resumen({
        "id": "x", "time": "2026-01-01T00:00:00Z", "lat": 1.0, "lon": 2.0,
        "depth": 5.0, "mag": 3.0, "mag_type": None, "region": None, "mode": None,
        "updated": None,
    })
    assert t.tipoMagnitud is None
    assert t.zona is None
    assert t.ultimaModificacion is None
    assert t.revisado is False  # sin mode -> no se da por revisado


def test_payload_sin_resumen_lanza_error():
    try:
        ParserJSON().parsear_evento({"generated": "2026-01-01T00:00:00Z"})
    except ValueError:
        pass
    else:
        raise AssertionError("esperaba un ValueError si falta la clave 'resumen'")


def test_vale_tanto_para_ultimo_como_para_resumen():
    """Ambos endpoints devuelven la misma clave 'resumen'."""
    parser = ParserJSON()
    fixture = _cargar_fixture()
    solo_resumen = {"generated": fixture["generated"], "resumen": fixture["resumen"]}
    assert parser.parsear_evento(fixture) == parser.parsear_evento(solo_resumen)
