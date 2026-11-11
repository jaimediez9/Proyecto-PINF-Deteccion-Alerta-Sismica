"""Enrutado de avisos FCM: del seísmo a la lista de topics destino.

Cuando el backend detecta un seísmo nuevo (tras consultar el servicio web del
ROA), debe avisar por Firebase Cloud Messaging a los usuarios cuyo umbral de
magnitud mínima y zona de interés lo cubran. FCM reparte por *topic*: publicar
en un topic llega a todos los dispositivos suscritos a él. Este módulo convierte
los datos del seísmo (magnitud y zona) en la lista de topics a los que publicar.

Alcance: SOLO la lógica pura de decisión de topics. No habla con Firebase ni con
el ROA; el envío real vive en otro módulo (un *adapter*), de modo que esto se
puede probar sin credenciales ni red.

Diseño provisional: los nombres de topic y las zonas definitivas están
pendientes de cerrar con el ROA (ver la batería de dudas del acta de reunión).
"""

from __future__ import annotations

import re
import unicodedata
from typing import Sequence

# Niveles de magnitud mínima que el usuario puede escoger en ajustes.
# Suscribirse a "mg_mayor_k" equivale a "quiero avisos de seísmos con magnitud >= k".
MAGNITUDE_LEVELS: tuple[int, ...] = (1, 2, 3)

# FCM limita a 5 el número de topics que puede combinar una misma condición.
FCM_MAX_TOPICS_PER_CONDITION = 5


def _slug(text: str) -> str:
    """Normaliza texto a un identificador válido como topic de FCM.

    Los topics de FCM solo admiten los caracteres [A-Za-z0-9-_.~%]. Se pasa el
    texto a minúsculas, se eliminan los acentos y cualquier otro carácter se
    sustituye por "_".
    """
    normalizado = unicodedata.normalize("NFKD", text)
    solo_ascii = normalizado.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "_", solo_ascii.lower()).strip("_")


def magnitude_topics(magnitude: float, levels: Sequence[int] = MAGNITUDE_LEVELS) -> list[str]:
    """Topics de magnitud que cubren un seísmo.

    Un seísmo avisa a todos los niveles cuyo umbral sea menor o igual que su
    magnitud. Así, una magnitud de 3.4 avisa a los suscritos a mg_mayor_1,
    mg_mayor_2 y mg_mayor_3. Si no llega al nivel mínimo más bajo, no avisa a
    nadie (devuelve una lista vacía).
    """
    return [f"mg_mayor_{level}" for level in sorted(levels) if magnitude >= level]


def zone_topic(zone: str) -> str:
    """Topic de zona asociado al nombre de zona que venga en el JSON del ROA."""
    return f"zona_{_slug(zone)}"


def compute_topics(
    magnitude: float,
    zone: str | None,
    *,
    levels: Sequence[int] = MAGNITUDE_LEVELS,
    combined: bool = False,
) -> list[str]:
    """Lista de topics a los que publicar para avisar de un seísmo.

    Parámetros:
        magnitude: magnitud del seísmo.
        zone: nombre de la zona del ROA, o None si el JSON no la trae.
        levels: niveles de magnitud suscribibles.
        combined: si es True, genera topics compuestos "mg_mayor_k_zona_x" con
            semántica de intersección (magnitud Y zona). Si es False (por
            defecto), devuelve los topics de magnitud y el de zona por separado.

    OJO (decisión pendiente del equipo): FCM reparte por OR, no por AND.
    - combined=False -> sencillo, pero un usuario de otra zona con umbral <= M
      también recibe el aviso; habría que filtrar en el cliente, gastando datos
      y batería que la RNF-09 prohíbe.
    - combined=True -> semántica correcta "magnitud Y zona", a costa de crear un
      topic por cada combinación nivel x zona.
    """
    if combined:
        if not zone:
            return []
        zt = zone_topic(zone)
        return [f"mg_mayor_{level}_{zt}" for level in sorted(levels) if magnitude >= level]

    topics = magnitude_topics(magnitude, levels)
    if zone:
        topics.append(zone_topic(zone))
    return topics


def build_conditions(
    magnitude: float,
    zone: str | None,
    *,
    levels: Sequence[int] = MAGNITUDE_LEVELS,
    max_topics: int = FCM_MAX_TOPICS_PER_CONDITION,
) -> list[str]:
    """Condiciones FCM que avisan de un seísmo a su magnitud Y en su zona.

    FCM no permite combinar topics con un AND directo al publicar, pero sí
    evaluar una *condición* booleana. Se usan dos familias de topics simples
    ('mg_mayor_k' y 'zona_x') y el AND lo resuelve la condición, evitando crear
    un topic por cada combinación nivel x zona.

    Devuelve UNA cadena de condición, p. ej. para magnitud 3.4 en el Golfo:

        ('mg_mayor_1' in topics || 'mg_mayor_2' in topics || 'mg_mayor_3' in topics) && 'zona_golfo_de_cadiz' in topics

    Como FCM admite como máximo `max_topics` topics por condición (5), cuando el
    seísmo alcanza muchos niveles se devuelven VARIAS condiciones (una por
    tanda) y hay que publicar un mensaje por cada una. Devuelve lista vacía si
    no hay zona o si la magnitud no alcanza ningún nivel.
    """
    if not zone:
        return []
    zona_cond = f"'{zone_topic(zone)}' in topics"
    niveles = sorted(level for level in levels if magnitude >= level)
    if not niveles:
        return []

    # Se reserva un hueco de la condición para el topic de zona.
    por_tanda = max(1, max_topics - 1)
    condiciones: list[str] = []
    for i in range(0, len(niveles), por_tanda):
        tanda = niveles[i:i + por_tanda]
        terminos = " || ".join(f"'mg_mayor_{level}' in topics" for level in tanda)
        magnitud_cond = terminos if len(tanda) == 1 else f"({terminos})"
        condiciones.append(f"{magnitud_cond} && {zona_cond}")
    return condiciones
