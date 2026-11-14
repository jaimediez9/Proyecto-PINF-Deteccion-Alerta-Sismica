"""Modelo de datos de un terremoto publicado por el servicio del ROA.

Corresponde a la clase **`Terremoto`** del diagrama de clases del equipo
(Documentación de Requisitos y Análisis, §8.2.1) y a los campos que pide el
pliego (**RD-03**). Se construye a partir del JSON del servicio y aísla al resto
del código de su formato crudo.

Las horas están siempre en UTC. La **zona** se corresponde con el campo `region`
del servicio; el ROA no usa identificadores de zona (se deriva de las
coordenadas, ver `app.services.topic_router`).
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
class Terremoto:
    """Un terremoto publicado por el ROA (a partir del objeto ``resumen``).

    Los nombres de los campos son los de la clase homónima del modelo de análisis.
    """

    identificador: str                # identificador del evento
    fechaHoraUTC: datetime            # instante del terremoto, en UTC
    latitud: float
    longitud: float
    profundidad: float               # en km
    magnitud: float
    tipoMagnitud: str | None
    zona: str | None                 # campo `region` del servicio
    revisado: bool                   # False si el evento es automático
    ultimaModificacion: datetime | None  # última modificación, en UTC

    @classmethod
    def desde_resumen(cls, resumen: dict) -> "Terremoto":
        """Construye un ``Terremoto`` a partir del objeto ``resumen`` del servicio.

        El flag de **revisado** se deduce de `mode`: el servicio marca como no
        revisados los eventos automáticos (`mode=automatic`) y avisa de que
        pueden cambiar o desaparecer (**RS-03**).
        """
        modo = (resumen.get("mode") or "").lower()
        return cls(
            identificador=resumen["id"],
            fechaHoraUTC=_parsear_utc_obligatorio(resumen["time"]),
            latitud=float(resumen["lat"]),
            longitud=float(resumen["lon"]),
            profundidad=float(resumen["depth"]),
            magnitud=float(resumen["mag"]),
            tipoMagnitud=resumen.get("mag_type"),
            zona=resumen.get("region"),
            revisado=(modo == "manual"),
            ultimaModificacion=_parsear_utc(resumen.get("updated")),
        )
