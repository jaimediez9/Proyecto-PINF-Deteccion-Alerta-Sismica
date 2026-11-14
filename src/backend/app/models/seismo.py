"""Modelo de datos de un seísmo, tal como lo publica el servicio del ROA.

El servicio (SeisComP3) entrega un objeto ``resumen`` con los campos que pide el
pliego (**RD-03**). Esta dataclass es el modelo interno del backend: se construye
a partir del JSON y aísla al resto del código del formato crudo del servicio.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


def _parsear_utc(texto: str | None) -> datetime | None:
    """Convierte un instante ISO-8601 del ROA (p. ej. ``...Z``) a datetime UTC.

    El servicio usa el sufijo ``Z``; se normaliza a ``+00:00`` porque
    ``datetime.fromisoformat`` solo acepta ``Z`` a partir de Python 3.11.
    """
    if not texto:
        return None
    return datetime.fromisoformat(texto.replace("Z", "+00:00")).astimezone(timezone.utc)


def _parsear_utc_obligatorio(texto: str) -> datetime:
    """Como :func:`_parsear_utc` pero para instantes que no pueden faltar."""
    instante = _parsear_utc(texto)
    if instante is None:
        raise ValueError("El resumen del ROA no trae el instante obligatorio")
    return instante


@dataclass(frozen=True)
class Seismo:
    """Un terremoto publicado por el ROA (a partir del objeto ``resumen``).

    Las horas están siempre en UTC (el servicio las da en UTC y así se guardan).
    La zona no es un campo: se deriva de ``lat``/``lon`` con la rejilla
    (ver ``app.services.topic_router.zona_topic``).
    """

    id: str
    time: datetime                 # instante del terremoto, en UTC
    lat: float
    lon: float
    depth_km: float
    magnitud: float
    tipo_magnitud: str | None
    region: str | None
    revisado: bool                 # False si el evento es automático (mode=automatic)
    actualizado: datetime | None   # última modificación, en UTC
    agencia: str | None = None
    autor: str | None = None

    @classmethod
    def desde_resumen(cls, resumen: dict) -> "Seismo":
        """Construye un ``Seismo`` a partir del objeto ``resumen`` del servicio.

        El flag de "revisado" se deduce de ``mode``: el servicio marca como no
        revisados los eventos automáticos (``mode=automatic``) y avisa de que
        pueden cambiar o desaparecer.
        """
        modo = (resumen.get("mode") or "").lower()
        return cls(
            id=resumen["id"],
            time=_parsear_utc_obligatorio(resumen["time"]),
            lat=float(resumen["lat"]),
            lon=float(resumen["lon"]),
            depth_km=float(resumen["depth"]),
            magnitud=float(resumen["mag"]),
            tipo_magnitud=resumen.get("mag_type"),
            region=resumen.get("region"),
            revisado=(modo == "manual"),
            actualizado=_parsear_utc(resumen.get("updated")),
            agencia=resumen.get("agency"),
            autor=resumen.get("author"),
        )
