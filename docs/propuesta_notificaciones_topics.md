# Propuesta provisional — Gestión de topics para los avisos (FCM)

> Documento de trabajo para revisar **en equipo** antes de la próxima reunión con el ROA.
> Cubre el "cómo pensamos detectar los terremotos nuevos y hacer llegar el aviso" que
> pide el pliego (**RD-05**). Estado de la implementación: ver sección 6.

## 1. Contexto y por qué

Los avisos son la parte que el ROA considera más importante (**RF-16 a RF-19**) y no
pueden depender de que la app esté abierta (**RD-05**), así que van por *push*
(**Firebase Cloud Messaging**) y no por consultas periódicas del móvil — esto último
chocaría con **RNF-09** (no gastar batería ni datos).

El usuario configura (en ajustes, **RF-17**) una **magnitud mínima** y una **zona**
(toda la zona del ROA, una región concreta o un radio alrededor de donde está).
FCM reparte por **topic**: publicar en un topic llega a *todos* los dispositivos
suscritos a él. Necesitamos que un aviso llegue **solo** a quien cumple magnitud **y**
zona.

## 2. El problema: FCM reparte por OR, no por AND

Si usamos dos familias de topics y publicamos en ambas por separado, FCM hace **OR**:
un usuario de otra zona con umbral ≤ M también recibe el aviso. Filtrar eso en el
cliente gasta datos y batería (contra **RNF-09**) y muestra avisos irrelevantes.

## 3. Alternativas valoradas

Denotamos: niveles de magnitud suscribibles `mg_mayor_k` (k = 1, 2, 3…), zonas `zona_x`.

| # | Vía | Semántica | Ventajas | Inconvenientes |
|---|-----|-----------|----------|----------------|
| A | **Topics compuestos** `mg_mayor_k_zona_x` | AND correcto | Publicación trivial; sin lógica booleana | N.º de topics = niveles × zonas; re-suscribir al cambiar de zona; más que mantener |
| B | **Topics separados + filtro en cliente** | OR (incorrecto) | Sencillo de publicar | Avisa a otras zonas; filtrar en el móvil gasta datos/batería (**RNF-09**). ❌ Descartada |
| C | **Topics simples + condiciones FCM** | AND correcto | Sin combinatoria; topics simples; AND lo resuelve FCM | Límite de 5 topics por condición; el *radio* no es expresable como topic estático |

## 4. Recomendación

**Opción C — condiciones de FCM.** Se mantienen dos familias de topics simples y el AND
vive en una *condición* booleana que FCM evalúa:

```
('mg_mayor_1' in topics || 'mg_mayor_2' in topics || 'mg_mayor_3' in topics) && 'zona_golfo_de_cadiz' in topics
```

- La app suscribe al usuario a **dos topics**: su umbral `mg_mayor_k` y su `zona_x`.
- El backend publica **un mensaje por zona afectada**, con esa condición.
- Resultado: semántica **magnitud Y zona** exacta, sin la explosión de topics de la
  opción A y sin el gasto de la opción B.

## 5. Reglas de gestión de topics

1. **Taxonomía de fuente única.** El esquema de niveles y zonas se define una vez en el
   backend y se replica en la app; si divergen, hay avisos silenciosamente muertos.
   Debe escribirse como contrato compartido app ↔ backend.
2. **Ciclo de vida.** FCM **crea los topics automáticamente** (existen al primer
   *subscribe*/envío); no hay que pre-crearlos. Al cambiar ajustes, la app **desuscribe**
   el topic antiguo y **suscribe** el nuevo.
3. **Zonas finitas y nombradas.** Las zonas deben ser una **lista cerrada** definida por
   el ROA (no texto libre del JSON). → Ver pregunta abierta 7.1.
4. **Límite de 5 topics por condición.** Con 3 niveles + 1 zona = 4, cabe. Si los niveles
   crecen por encima de 4, el envío se **trocea** en varias condiciones (ya implementado).
5. **Lo que esta vía NO cubre:** el *radio alrededor del usuario* (**RF-17**, prioridad
   *importante*, no imprescindible) no se puede expresar como topic estático. Opciones
   futuras: filtrar en cliente, o pasar a **envío por token** desde el backend.

## 6. Estado de la implementación

Ya implementado y probado (lógica pura, sin red ni credenciales):

- `src/backend/app/services/topic_router.py`
  - `magnitude_topics(magnitude)` → niveles cubiertos.
  - `zone_topic(zona)` → normaliza el nombre de zona a un topic válido de FCM.
  - `compute_topics(magnitude, zona, combined=…)` → topics separados o compuestos (A/B).
  - `build_conditions(magnitude, zona)` → condiciones FCM de la opción C, con troceo
    automático al pasar de 5 topics.
- `src/backend/tests/test_topic_router.py` → 18 pruebas (`pytest`).

**Pendiente:** el *adapter* de envío real a FCM (credencial en `.env`, jamás en el repo
por **RNF-16**) — bloqueado hasta tener proyecto Firebase y el esquema del JSON del ROA.

## 7. Preguntas abiertas para la reunión

1. **Lista cerrada de zonas** de la red del ROA y su nomenclatura.
2. **Niveles de magnitud** definitivos (¿1, 2, 3…? ¿con qué magnitud mínima por defecto?).
3. ¿Entra el **radio alrededor del usuario** en esta fase, o se deja para más adelante?
4. **Qué campos** trae exactamente el JSON (¿la zona viene como texto? ¿un código?).

---

*Referencias:* RF-16 a RF-19 (avisos), RF-17 (zona/radio), RF-20 (no re-avisar salvo
cambio de magnitud), RD-05 (explicar el mecanismo de aviso), RNF-09 (no gastar
batería/datos), RNF-16 (sin claves en el repo).
