"""Enrutado de avisos FCM: del seísmo a la lista de topics destino.

Cuando el backend detecta un seísmo nuevo (tras consultar el servicio web del
ROA), debe avisar por Firebase Cloud Messaging a los usuarios cuyo umbral de
magnitud mínima y zona de interés lo cubran. FCM reparte por *topic*: publicar
en un topic llega a todos los dispositivos suscritos a él. Este módulo convierte
los datos del seísmo (magnitud, latitud y longitud) en los topics a los que
publicar.

Zonas: el ROA **no usa identificadores de zona**. Una "zona" es una **celda de
una rejilla lat/lon**, así que se deriva de las coordenadas del seísmo con
`zona_topic(lat, lon)`. No se espera ningún campo de zona en el JSON.

Alcance: SOLO la lógica pura de decisión de topics. No habla con Firebase ni con
el ROA; el envío real vive en otro módulo (un *adapter*), de modo que esto se
puede probar sin credenciales ni red.
"""

from __future__ import annotations

import math
from typing import Sequence

# Niveles de magnitud mínima que el usuario puede escoger en ajustes.
# Suscribirse a "mg_mayor_k" equivale a "quiero avisos de seísmos con magnitud >= k".
MAGNITUDE_LEVELS: tuple[int, ...] = (1, 2, 3)

# FCM limita a 5 el número de topics que puede combinar una misma condición.
FCM_MAX_TOPICS_PER_CONDITION = 5

# Lado de la celda de la rejilla de zonas, en grados. 0.25 grados equivalen a
# ~25-28 km en latitud (y menos en longitud, segun el coseno de la latitud).
# Es el tamano "de comarca"; ajustable si en la reunion se decide otro.
PASO_GRADOS = 0.25


def celda(lat: float, lon: float, paso: float = PASO_GRADOS) -> tuple[int, int]:
    """Indices (i, j) de la celda de la rejilla que contiene el punto (lat, lon).

    La celda (i, j) cubre la latitud en [i*paso, (i+1)*paso) y la longitud en
    [j*paso, (j+1)*paso).

    Se usa `math.floor` y NO truncamiento: con longitudes negativas (todo el
    oeste de Greenwich, que es la zona del ROA) truncar meteria el evento en la
    celda de al lado (int(-4.1395/0.25) == -16, pero floor == -17).
    """
    return math.floor(lat / paso), math.floor(lon / paso)


def zona_topic(lat: float, lon: float, paso: float = PASO_GRADOS) -> str:
    """Topic de zona (celda de la rejilla) que contiene el punto (lat, lon)."""
    i, j = celda(lat, lon, paso)
    return f"zona_{i}_{j}"


def magnitude_topics(magnitude: float, levels: Sequence[int] = MAGNITUDE_LEVELS) -> list[str]:
    """Topics de magnitud que cubren un seísmo.

    Un seísmo avisa a todos los niveles cuyo umbral sea menor o igual que su
    magnitud. Así, una magnitud de 3.4 avisa a los suscritos a mg_mayor_1,
    mg_mayor_2 y mg_mayor_3. Si no llega al nivel mínimo más bajo, no avisa a
    nadie (devuelve una lista vacía).
    """
    return [f"mg_mayor_{level}" for level in sorted(levels) if magnitude >= level]


def compute_topics(
    magnitude: float,
    lat: float,
    lon: float,
    *,
    levels: Sequence[int] = MAGNITUDE_LEVELS,
    paso: float = PASO_GRADOS,
    combined: bool = False,
) -> list[str]:
    """Lista de topics a los que publicar para avisar de un seísmo.

    Parámetros:
        magnitude: magnitud del seísmo.
        lat, lon: coordenadas del seísmo (definen la celda de zona).
        levels: niveles de magnitud suscribibles.
        paso: lado de la celda de la rejilla, en grados.
        combined: si es True, genera topics compuestos "mg_mayor_k_zona_ij" con
            semántica de intersección (magnitud Y zona). Si es False (por
            defecto), devuelve los topics de magnitud y el de zona por separado.

    OJO: FCM reparte por OR, no por AND.
    - combined=False -> sencillo, pero un usuario de otra zona con umbral <= M
      también recibe el aviso; habría que filtrar en el cliente, gastando datos
      y batería que la RNF-09 prohíbe. Preferible usar `build_conditions`.
    - combined=True -> semántica correcta "magnitud Y zona", a costa de crear un
      topic por cada combinación nivel x celda.
    """
    zt = zona_topic(lat, lon, paso)
    if combined:
        return [f"mg_mayor_{level}_{zt}" for level in sorted(levels) if magnitude >= level]

    topics = magnitude_topics(magnitude, levels)
    topics.append(zt)
    return topics


def build_conditions(
    magnitude: float,
    lat: float,
    lon: float,
    *,
    levels: Sequence[int] = MAGNITUDE_LEVELS,
    paso: float = PASO_GRADOS,
    max_topics: int = FCM_MAX_TOPICS_PER_CONDITION,
) -> list[str]:
    """Condiciones FCM que avisan de un seísmo a su magnitud Y en su zona.

    FCM no permite combinar topics con un AND directo al publicar, pero sí
    evaluar una *condición* booleana. Se usan dos familias de topics simples
    ('mg_mayor_k' y 'zona_ij') y el AND lo resuelve la condición, evitando crear
    un topic por cada combinación nivel x celda.

    Devuelve UNA cadena de condición, p. ej. para magnitud 3.4 en la celda
    (148, -17):

        ('mg_mayor_1' in topics || 'mg_mayor_2' in topics || 'mg_mayor_3' in topics) && 'zona_148_-17' in topics

    Como FCM admite como máximo `max_topics` topics por condición (5), cuando el
    seísmo alcanza muchos niveles se devuelven VARIAS condiciones (una por
    tanda) y hay que publicar un mensaje por cada una. Devuelve lista vacía si
    la magnitud no alcanza ningún nivel.
    """
    niveles = sorted(level for level in levels if magnitude >= level)
    if not niveles:
        return []

    zona_cond = f"'{zona_topic(lat, lon, paso)}' in topics"

    # Se reserva un hueco de la condición para el topic de zona.
    por_tanda = max(1, max_topics - 1)
    condiciones: list[str] = []
    for i in range(0, len(niveles), por_tanda):
        tanda = niveles[i:i + por_tanda]
        terminos = " || ".join(f"'mg_mayor_{level}' in topics" for level in tanda)
        magnitud_cond = terminos if len(tanda) == 1 else f"({terminos})"
        condiciones.append(f"{magnitud_cond} && {zona_cond}")
    return condiciones
