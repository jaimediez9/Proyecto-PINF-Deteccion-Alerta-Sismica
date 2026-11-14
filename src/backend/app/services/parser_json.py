"""Parser del JSON del servicio del ROA.

Implementa la clase **`ParserJSON`** del modelo de análisis, que transforma el
JSON del servicio del ROA en objetos :class:`~app.models.terremoto.Terremoto`
(**RD-01**, **RD-03**).

El servicio expone ``/api/ultimo`` (evento completo) y ``/api/ultimo/resumen``
(solo el resumen). Ambos payloads incluyen la clave ``resumen``, así que el mismo
parser sirve para los dos.
"""

from __future__ import annotations

from app.models.terremoto import Terremoto


class ParserJSON:
    """Transforma el JSON del servicio del ROA en objetos ``Terremoto``."""

    def parsear_evento(self, payload: dict) -> Terremoto:
        """Traduce el JSON del servicio del ROA a un :class:`Terremoto`.

        Acepta tanto el payload de ``/api/ultimo`` como el de
        ``/api/ultimo/resumen``: en ambos, los datos del terremoto están en la
        clave ``resumen``.

        Lanza ``ValueError`` si el payload no trae esa clave (respuesta
        inesperada).
        """
        if not isinstance(payload, dict) or "resumen" not in payload:
            raise ValueError("El JSON del ROA no contiene la clave 'resumen'")
        return Terremoto.desde_resumen(payload["resumen"])
