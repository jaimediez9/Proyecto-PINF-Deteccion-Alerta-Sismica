"""Adapter de envío de avisos a Firebase Cloud Messaging (HTTP v1).

Une la lógica de decisión de topics (`topic_router`) con el envío real a FCM.
Se usa la API **HTTP v1** (la legacy, con la clave de servidor, está obsoleta):
cada mensaje se manda a una *condición* de topics y se autentica con una cuenta
de servicio.

La credencial **NUNCA** va en el repo (**RNF-16**): se lee de una variable de
entorno que apunta al JSON de la cuenta de servicio (ver `.env.example`).

Sin proyecto Firebase todavía, el desarrollo y los tests usan
:class:`EnviadorFCMFalso`, que no toca la red.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import timezone
from typing import Protocol

from app.models.seismo import Seismo
from app.services.topic_router import MAGNITUDE_LEVELS, PASO_GRADOS, build_conditions

URL_BASE = "https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"
SCOPES = ("https://www.googleapis.com/auth/firebase.messaging",)
TIEMPO_MAXIMO_S = 15


@dataclass(frozen=True)
class ConfiguracionFCM:
    """Datos de acceso al proyecto Firebase (fuera del repo, ver RNF-16)."""

    project_id: str
    ruta_credenciales: str

    @classmethod
    def desde_entorno(cls, entorno: dict | None = None) -> "ConfiguracionFCM":
        """Lee la configuración de las variables de entorno (no de ficheros del repo)."""
        fuente = entorno if entorno is not None else os.environ
        project_id = fuente.get("FIREBASE_PROJECT_ID")
        ruta = fuente.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not project_id or not ruta:
            raise RuntimeError(
                "Faltan FIREBASE_PROJECT_ID y/o GOOGLE_APPLICATION_CREDENTIALS "
                "(ver src/backend/.env.example)"
            )
        return cls(project_id=project_id, ruta_credenciales=ruta)


def construir_mensaje(
    condicion: str,
    seismo: Seismo,
    *,
    titulo: str | None = None,
    cuerpo: str | None = None,
) -> dict:
    """Construye el cuerpo del mensaje FCM (HTTP v1) para un seísmo.

    El aviso lleva magnitud, zona y hora (**RF-19**) y todos los datos del
    terremoto, que FCM exige como cadenas. El título es factual y en pasado:
    nada puede sugerir que la app se adelanta al terremoto (**RS-01**).
    """
    if not condicion:
        raise ValueError("La condición de topics no puede estar vacía")

    instante = seismo.time.astimezone(timezone.utc)
    return {
        "message": {
            "condition": condicion,
            "notification": {
                "title": titulo or "Terremoto registrado",
                "body": cuerpo
                or f"M{seismo.magnitud} en {seismo.region or 'zona sin especificar'}"
                f" · {instante.strftime('%Y-%m-%d %H:%M')} UTC",
            },
            "data": {
                "id": seismo.id,
                "tiempo_utc": instante.isoformat(),
                "lat": str(seismo.lat),
                "lon": str(seismo.lon),
                "profundidad_km": str(seismo.depth_km),
                "magnitud": str(seismo.magnitud),
                "tipo_magnitud": seismo.tipo_magnitud or "",
                "region": seismo.region or "",
                "revisado": "true" if seismo.revisado else "false",
            },
        }
    }


class EnviadorFCM(Protocol):
    """Cualquier cosa capaz de enviar un mensaje ya construido a FCM."""

    def enviar(self, mensaje: dict) -> str:
        """Envía el mensaje y devuelve su identificador (o cadena vacía)."""
        ...


class EnviadorFCMFalso:
    """Enviador de mentira: guarda los mensajes en vez de mandarlos.

    Para desarrollo (aún no hay proyecto Firebase) y para los tests, sin tocar
    la red.
    """

    def __init__(self) -> None:
        self.enviados: list[dict] = []

    def enviar(self, mensaje: dict) -> str:
        self.enviados.append(mensaje)
        return f"falso-{len(self.enviados)}"


@dataclass
class EnviadorFCMHttp:
    """Enviador real: API HTTP v1 de FCM autenticada con una cuenta de servicio."""

    configuracion: ConfiguracionFCM

    def enviar(self, mensaje: dict) -> str:
        import httpx  # import perezoso: los tests no necesitan la red

        url = URL_BASE.format(project_id=self.configuracion.project_id)
        cabeceras = {"Authorization": f"Bearer {self._token_de_acceso()}"}
        respuesta = httpx.post(url, json=mensaje, headers=cabeceras, timeout=TIEMPO_MAXIMO_S)
        respuesta.raise_for_status()
        return respuesta.json().get("name", "")

    def _token_de_acceso(self) -> str:
        # Import perezoso: google-auth solo hace falta para el envío real.
        from google.auth.transport.requests import Request as PeticionGoogle
        from google.oauth2 import service_account

        credenciales = service_account.Credentials.from_service_account_file(
            self.configuracion.ruta_credenciales, scopes=list(SCOPES)
        )
        credenciales.refresh(PeticionGoogle())
        return credenciales.token


def avisar_de(
    seismo: Seismo,
    enviador: EnviadorFCM,
    *,
    levels: tuple[int, ...] = MAGNITUDE_LEVELS,
    paso: float = PASO_GRADOS,
) -> list[str]:
    """Avisa de un seísmo: calcula sus condiciones y manda un mensaje por cada una.

    Devuelve los identificadores devueltos por el enviador. Nota: el control de
    "no reavisar el mismo terremoto salvo cambio apreciable de magnitud"
    (**RF-20**) necesita estado (la base de datos) y no vive aquí.
    """
    condiciones = build_conditions(seismo.magnitud, seismo.lat, seismo.lon, levels=levels, paso=paso)
    return [enviador.enviar(construir_mensaje(condicion, seismo)) for condicion in condiciones]
