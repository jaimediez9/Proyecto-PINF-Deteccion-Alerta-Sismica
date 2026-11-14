"""Pruebas del parser del JSON del ROA (app/services/earthquake_parser.py).

Se ejecutan sin red: el caso principal usa una respuesta REAL del servicio,
grabada en tests/fixtures/ultimo.json.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Permite importar el paquete 'app' al ejecutar pytest desde cualquier carpeta.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.models.seismo import Seismo  # noqa: E402
from app.services.earthquake_parser import parsear_evento  # noqa: E402

FIXTURE = Path(__file__).parent / "fixtures" / "ultimo.json"


def _cargar_fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


# --- contra una respuesta REAL del servicio ---

def test_parsea_el_evento_real():
    """Evento real roa2026whof del servicio del ROA."""
    s = parsear_evento(_cargar_fixture())
    assert isinstance(s, Seismo)
    assert s.id == "roa2026whof"
    assert s.lat == 37.0959
    assert s.lon == -4.1395
    assert s.depth_km == 10.0
    assert s.magnitud == 2.0
    assert s.tipo_magnitud == "M"
    assert s.region == "Spain"


def test_la_hora_es_utc_y_aware():
    s = parsear_evento(_cargar_fixture())
    assert s.time == datetime(2026, 11, 14, 4, 54, 56, 895000, tzinfo=timezone.utc)
    assert s.time.tzinfo is not None
    assert s.actualizado == datetime(2026, 11, 14, 4, 58, 12, tzinfo=timezone.utc)


def test_evento_automatico_no_esta_revisado():
    """mode=automatic -> revisado False (la nota del servicio lo confirma)."""
    fixture = _cargar_fixture()
    assert fixture["resumen"]["mode"] == "automatic"
    assert parsear_evento(fixture).revisado is False


# --- casos de borde (dicts a mano) ---

def test_evento_manual_esta_revisado():
    s = Seismo.desde_resumen({
        "id": "x", "time": "2026-01-01T00:00:00Z", "lat": 1.0, "lon": 2.0,
        "depth": 5.0, "mag": 3.0, "mag_type": "ML", "region": "Spain",
        "mode": "manual", "updated": "2026-01-01T00:01:00Z",
    })
    assert s.revisado is True


def test_campos_opcionales_ausentes():
    """region/mag_type/updated pueden faltar o ser null."""
    s = Seismo.desde_resumen({
        "id": "x", "time": "2026-01-01T00:00:00Z", "lat": 1.0, "lon": 2.0,
        "depth": 5.0, "mag": 3.0, "mag_type": None, "region": None, "mode": None,
        "updated": None,
    })
    assert s.tipo_magnitud is None
    assert s.region is None
    assert s.actualizado is None
    assert s.revisado is False  # sin mode -> no se da por revisado


def test_payload_sin_resumen_lanza_error():
    try:
        parsear_evento({"generated": "2026-01-01T00:00:00Z"})
    except ValueError:
        pass
    else:
        raise AssertionError("esperaba un ValueError si falta la clave 'resumen'")


def test_vale_tanto_para_ultimo_como_para_resumen():
    """Ambos endpoints devuelven la misma clave 'resumen'."""
    fixture = _cargar_fixture()
    solo_resumen = {"generated": fixture["generated"], "resumen": fixture["resumen"]}
    assert parsear_evento(fixture) == parsear_evento(solo_resumen)
