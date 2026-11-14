# Aplicación móvil de información sísmica del ROA

*(nombre corto propuesto: **SISMO** — Sistema de Información Sísmica y Monitorización
Operativa; pendiente de confirmar con el cliente)*

Aplicación móvil que muestra los terremotos registrados por la red sísmica del **Real
Observatorio de la Armada (ROA)** — Sección de Geofísica, San Fernando (Cádiz) — y avisa
al usuario cuando se publica uno nuevo, **aunque la aplicación esté cerrada**.

Proyecto de **Proyectos Informáticos de Ingeniería — PINF 2026**. Equipo **G5**.

---

## Qué es y qué no es

- **Es** una aplicación **informativa**: muestra los terremotos **ya ocurridos** y avisa
  cuando aparece uno nuevo. Referencia de partida: la app de terremotos del IGN.
- **NO es** un sistema de **alerta temprana**: no puede dar a entender que avisa antes de
  que llegue la sacudida (**RS-01**).

> **Aviso legal** (primera apertura y apartado sobre el ROA, **RS-02**): los datos son
> informativos, pueden ser provisionales y cambiar tras revisarlos, y **no sustituyen** a
> las indicaciones de Protección Civil ni del 112.

## Datos del proyecto

| | |
|---|---|
| **Nombre del proyecto** | Aplicación móvil de información sísmica del ROA |
| **Nombre corto** | Pendiente de acordar con el cliente (propuesta: SISMO) |
| **Cliente** | Real Observatorio de la Armada, Sección de Geofísica (San Fernando, Cádiz) |
| **Contacto del cliente** | David Rodríguez Collantes, Teniente de Navío |
| **Equipo** | Grupo G5, 13 integrantes |
| **Jefe de proyecto** | Francisco Javier Sánchez González |
| **Repositorio** | `github.com/jaimediez9/Proyecto-PINF-Deteccion-Alerta-Sismica` |
| **Inicio del proyecto** | 23/09/2026 |
| **Fecha del pliego** | 30/10/2026 |
| **Entrega final** | Pendiente de acordar con el cliente |

## Equipo y roles (13 personas)

- **Jefe de proyecto (1):** Francisco Javier Sánchez González.
- **Analistas (2):** Hugo Freire del Río, Adrián Bernal Moreno — requisitos, modelado,
  consultas al cliente, planificación y documentación.
- **Diseñadores (3):** Eduardo Carrasco Ahumada, Daniel Rodríguez Sánchez, Emilio Díaz
  Carmona — maquetas, diseño de clases y de la base de datos.
- **Programadores (5):** Jaime Díez Pica, Pablo Moulet Fernández, Carlos Camacho Martín,
  Ángela Escribano Marcos, Laura María Via Alba — **Grupo A (frontend)** y **Grupo B
  (backend)**.
- **Testers (2):** Nadia Kerre, Lucía Zúñiga Sánchez.

## Estructura del repositorio

```
src/backend/     Backend (Python / FastAPI): datos y avisos
src/frontend/    Aplicación móvil (Flutter)
Análisis/        Casos de uso (CU-01 … CU-14) y diagramas
Diseño/          Maquetas de interfaz
Documentación/   Documentación oficial del proyecto (PDFs y actas)
docs/            Documentos de trabajo (pliego, propuestas y preguntas)
```

La documentación oficial sigue la clasificación de `Documentación/Tipos_Documentación.md`:
**gestión**, **requisitos y análisis**, **diseño**, **desarrollo**, **pruebas** y
**entrega**.

## Tecnología

| Parte | Tecnología |
|---|---|
| Backend | Python + **FastAPI**; **SQLite**; avisos con **Firebase Cloud Messaging (FCM)** |
| App móvil | **Flutter** (Android como mínimo; iPhone deseable) |
| Datos | Servicio web **JSON** del ROA (entorno de pruebas durante el desarrollo) |

## Cómo ejecutar

### Backend

```bash
cd src/backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest
```

Hoy el backend es, sobre todo, **lógica y pruebas** (parser del JSON, enrutado de avisos y
adaptador de FCM). El arranque como servicio en `app/main.py` está pendiente de cablear.

### App móvil

```bash
cd src/frontend
flutter pub get
flutter run
```

## El servicio de datos del ROA

Durante el desarrollo se trabaja contra el **entorno de pruebas**; **nunca** se accede a los
sistemas de producción del Observatorio (**RD-02**).

El servicio se autodescribe en `GET /` y expone:

- `GET /api/ultimo` — último terremoto completo (resumen, evento, orígenes con llegadas y
  magnitudes, picks, amplitudes, mecanismos focales).
- `GET /api/ultimo/resumen` — solo el resumen (origen y magnitud preferidos).
- `GET /api/estado` — antigüedad de los datos (`503` si llevan más de 10 min sin
  actualizarse).

Los campos que pide el pliego (**RD-03**) están en `resumen`:
`id`, `time` (UTC ISO-8601), `lat`, `lon`, `depth` (km), `mag`, `mag_type`, `region` y
`updated`. El flag de **revisado** se deduce de `mode`: los eventos `automatic` **no** están
revisados y pueden cambiar o desaparecer (**RS-03**).

> **Pendiente de resolver con el informático del ROA:** el servicio solo expone **el último
> terremoto**; faltan la **lista por periodo con magnitud mínima** y la **lista de
> estaciones** que pide RD-03.

## Zonas y avisos

- **Zonas:** el ROA describe las zonas como una **cuadrícula de intervalos de latitud y
  longitud**, **sin identificadores** de zona (formato exacto pendiente de aclarar). Por
  tanto, la zona se **deriva de las coordenadas** del terremoto (rejilla de `0.25°`,
  ~25-28 km).
- **Avisos:** por **Firebase Cloud Messaging**, con *topics*. El usuario se suscribe a su
  umbral de magnitud (`mg_mayor_k`) y a su celda de zona (`zona_i_j`); cada aviso se publica
  a una **condición** que combina ambas (magnitud **Y** zona). El pliego exige además la
  **zona** de los avisos (RF-17), que un topic por magnitud no cubre; las alternativas
  valoradas están en `docs/propuesta_notificaciones_topics.md`.

## Retención de datos

- Los terremotos se registran en la aplicación durante **7 días**.
- Pasado ese plazo se puede conservar solo **latitud y longitud** (opcionalmente, para
  mapas de calor de seísmos).
- El ROA facilitará una base de datos con los terremotos de **2026**, a partir de la cual se
  preparará una base propia de estructura similar.

## Requisitos y prioridades

El cliente **prioriza una aplicación sencilla que funcione** frente a una muy completa que
falle. Clasificación del pliego:

- **Imprescindible:** lista (RF-01 a RF-05), ficha (RF-11, RF-12, RF-14), avisos (RF-16 a
  RF-19), imagen corporativa (RF-28, RNF-01 a RNF-05), datos (RD-01 a RD-03, RD-05, RD-06),
  restricciones (RS-01 a RS-03) y privacidad (RNF-13 a RNF-16).
- **Importante:** mapa (RF-07, RF-08), filtros (RF-06), zona de los avisos (RF-17),
  información y consejos (RF-24, RF-25), compartir (RF-15) y ajustes (RF-27).
- **Deseable:** *«¿Lo has sentido?»* (RF-21 a RF-23), estaciones en el mapa (RF-10),
  ubicación del usuario (RF-09, RF-13), RF-20, glosario (RF-26), tema oscuro (RNF-06),
  iPhone (RNF-07) e inglés (RNF-12).
- **Fuera del encargo:** alerta sísmica temprana, datos de otras agencias (RS-04) y
  publicación en tiendas sin autorización del ROA (RS-05).

El detalle numerado está en `docs/Pliego_requisitos_app_sismica_ROA.pdf` y en
`Documentación/Documentación de Requisitos y Análisis/Documento_Requisitos_Análisis.pdf`.

## Modelo de análisis

- **14 casos de uso (CU-01 … CU-14):** consultar lista, filtrar, actualizar, mapa, ficha,
  estaciones, compartir, configurar avisos, recibir aviso, *«¿Lo has sentido?»*, información
  del ROA, recomendaciones, glosario y preferencias.
- **Clases principales:** `Terremoto`, `EstacionSismica`, `RespuestaSentido`,
  `ConfigUsuario`, `FiltroTerremotos`, `AvisoLegal`, `GestorApp`, `ParserJSON`,
  `RegistroTerremotos`, `ServicioWebROA`, `GestorAlertas`, `GestorNotifs` y `Notificacion`.

Los diagramas (casos de uso y clases) están en
`Documentación/Documentación de Requisitos y Análisis/`.

## Planificación y entregas

| N.º | Entrega | Fecha |
|---|---|---|
| 1 | Análisis de requisitos y planificación | 13/11/2026 |
| 2 | Maquetas | Semana 6 |
| 3 | Versión intermedia | Semana 8 |
| 4 | Versión final | Semana 12 |
| 5 | Código y documentación | Semana 12 |

La planificación temporal (Gantt), el reparto semanal de tareas y el seguimiento están en
`Documentación/Documentación de Gestión del Proyecto/Documento_Gestión_Proyecto_01.pdf`.

## Privacidad y seguridad

- La **ubicación** del usuario se usa **solo en el móvil** (filtrar y calcular distancias);
  únicamente se envía al responder a *«¿Lo has sentido?»* y con su permiso (**RNF-13**).
- **No se recogen datos personales**; hay una política de privacidad acorde con el **RGPD**.
- En la versión final, todas las comunicaciones van **cifradas (HTTPS)**.
- **Ninguna contraseña ni clave** del ROA puede quedar escrita en el código ni en el
  repositorio (**RNF-16**): las credenciales van en `.env` (ver `src/backend/.env.example`).

## Identidad visual

- Paleta basada principalmente en **azul y blanco**, tomando como referencia los colores de
  la web del **Ministerio de Defensa**.
- Se incorporarán los **logotipos del ROA y de la Armada** cuando los facilite el cliente
  (pendientes de recibir).

## Reuniones y próximos pasos

Las actas están en `Documentación/Actas de Reunión/`. Destacado:

- El servicio solo da el último terremoto → **pedir lista por periodo y estaciones**.
- El cuestionario *«¿Lo has sentido?»* se remitirá por **correo electrónico** (dirección por
  confirmar).
- **Reunión técnica con el informático del ROA** para aclarar el JSON, las zonas, la base de
  datos de 2026 y el envío del cuestionario.
- El equipo puede plantear dudas al teniente por correo o WhatsApp.

## Contribuir

- **Ramas por funcionalidad** y **pull requests** hacia `master`.
- Respetad el ámbito asignado: cada rol toca lo suyo.
- Nada de `push --force` sobre `master`.

---

*Documentos de trabajo en `docs/`: propuesta de avisos, preguntas para el cliente y el
pliego de requisitos.*
