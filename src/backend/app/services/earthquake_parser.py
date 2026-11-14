"""Parser del JSON del servicio del ROA.

El servicio expone ``/api/ultimo`` (evento completo) y ``/api/ultimo/resumen``
(solo el resumen). Ambos payloads incluyen la clave ``resumen``, así que un mismo
parser sirve para los dos.
"""

from __future__ import annotations

from app.models.seismo import Seismo


def parsear_evento(payload: dict) -> Seismo:
    """Traduce el JSON del servicio del ROA a un :class:`Seismo`.

    Acepta tanto el payload de ``/api/ultimo`` como el de
    ``/api/ultimo/resumen``: en ambos, los datos del terremoto están en la clave
    ``resumen``.

    Lanza ``ValueError`` si el payload no trae esa clave (respuesta inesperada).
    """
    if not isinstance(payload, dict) or "resumen" not in payload:
        raise ValueError("El JSON del ROA no contiene la clave 'resumen'")
    return Seismo.desde_resumen(payload["resumen"])
