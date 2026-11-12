# Preguntas para el teniente — zonas y sistema de avisos

> Para la reunión de los analistas. **Llevar la pregunta 1 como prioritaria**: es la que
> desbloquea el diseño de los avisos. El resto son de apoyo.

## Contexto (por qué preguntamos)

Estamos montando los avisos con **Firebase Cloud Messaging por *topics***. Cada usuario se
suscribe a un topic según su magnitud mínima (`mg_mayor_k`) y, para filtrar **por zona**,
necesitamos saber cómo identifica el ROA las zonas. Según cómo vengan (texto libre, código,
o delimitación geográfica) elegiremos una técnica u otra.

La lógica de decisión de topics ya está **implementada y probada**: ver
`src/backend/app/services/topic_router.py` y la propuesta en
`docs/propuesta_notificaciones_topics.md`.

## Preguntas

**1. Zonas — lista y nomenclatura (PRIORITARIA)**
- ¿Con qué zonas etiquetáis los terremotos? ¿Nos facilitáis la lista?
- ¿La zona viene en el JSON como **texto** ("Golfo de Cádiz") o como **código/ID**?
- ¿Esas zonas son las mismas que podríamos usar para que el usuario elija la **zona de sus avisos** (RF‑17), o son conceptos distintos?
- *Por qué:* de esto depende cómo filtramos los avisos por zona (topics de zona u otra vía).

**2. JSON de ejemplo**
- Un terremoto de muestra con **todos** los campos.
- Confirmar: cómo llega la **zona**, si hay un flag de **revisado/automático**, y el **tipo del identificador**.
- *Por qué:* necesitamos el esquema real para el *parser* y para el enrutado de avisos.

**3. Valores por defecto** *(el pliego los deja como "pendiente de concretar")*
- Magnitud mínima por defecto de los avisos.
- Límites exactos de la zona de cobertura.

**4. Radio alrededor del usuario (RF‑17)**
- ¿Entra en esta primera fase? ¿Con qué precisión lo queréis (radio exacto o aproximado)?

**5. Delimitación geográfica de las zonas** *(solo si vamos por la vía de zonas)*
- ¿Nos podéis dar los polígonos/coordenadas de cada zona, no solo el nombre?

## No es una pregunta (es para informar, no para preguntar)

El *cómo* enviamos el aviso (FCM + topics/condiciones) es **decisión nuestra**: el pliego
(**RD‑05**) pide que se lo **expliquemos** con ventajas e inconvenientes. Llevarlo como
**propuesta**, no como duda. → Ver `docs/propuesta_notificaciones_topics.md`.
