# Batería de preguntas — Sistema automático de detección y alerta sísmica

**Reunión con la empresa impulsora del proyecto**  
**Interlocutor:** Teniente responsable del encargo  
**Asignatura:** Proyectos Informáticos de Ingeniería

## 1. Objetivo y necesidad operativa

El propósito de este bloque es identificar el problema concreto que justifica el proyecto y los resultados que se esperan obtener.

- ¿Cuál es el problema concreto que se pretende resolver mediante este sistema?
- ¿Qué ha motivado la iniciativa: una experiencia previa, una carencia de los sistemas actuales o una necesidad operativa identificada?
- ¿Quién utilizará el sistema y quién recibirá las alertas?
- ¿Qué decisiones se tomarán a partir de una alerta sísmica?
- ¿Qué consecuencias tendría detectar un terremoto demasiado tarde o emitir una falsa alarma?
- ¿Cómo se gestiona actualmente una posible emergencia sísmica y qué limitaciones presenta el procedimiento?
- ¿Qué resultado tangible se espera obtener al finalizar el proyecto?

**Pregunta clave:** Si tuviéramos que resolver una sola necesidad con este proyecto, ¿cuál sería y cómo mediríamos que la hemos resuelto?

## 2. Alcance y funcionamiento esperado

Es necesario determinar qué se entiende por detección y alerta sísmica, pues estas expresiones pueden referirse a sistemas con objetivos y complejidades muy diferentes.

- ¿Se pretende detectar un terremoto cuando ya está ocurriendo o proporcionar una alerta temprana antes de que lleguen las ondas más destructivas a determinadas ubicaciones?
- ¿Se busca detectar terremotos reales, identificar vibraciones sospechosas o ambas cosas?
- ¿El sistema debe localizar el epicentro, estimar la magnitud o determinar la intensidad esperada?
- ¿Qué área geográfica debe cubrir?
- ¿Qué tipos de eventos sísmicos deben detectarse?
- ¿Se pretende desarrollar un prototipo académico, un demostrador funcional o un sistema destinado a utilizarse en operaciones reales?
- ¿Existen sistemas de referencia cuyo funcionamiento deba igualarse o mejorarse?
- ¿Qué funcionalidades son imprescindibles y cuáles podrían considerarse opcionales?

**Advertencia técnica:** no debe confundirse la alerta temprana con la predicción de terremotos antes de que ocurran. La alerta temprana aprovecha el intervalo entre la detección inicial del evento y la llegada posterior de las ondas sísmicas a otras zonas.

## 3. Sensores, datos e infraestructura

Este bloque permitirá determinar qué recursos existen y qué componentes deberá desarrollar el equipo.

- ¿Disponemos de sensores sísmicos propios o debemos adquirirlos?
- ¿Qué tipo, modelo, precisión, frecuencia de muestreo y rango dinámico tienen?
- ¿Existe una red de sensores o trabajaremos con una única estación?
- ¿Dónde estarán instalados y quién se encargará de su mantenimiento?
- ¿Disponemos de datos históricos de terremotos y de vibraciones no sísmicas?
- ¿Podemos acceder a datos de organismos públicos o redes sismológicas?
- ¿Existe conectividad continua entre los sensores y el sistema central?
- ¿Debe funcionar sin conexión a Internet o ante una interrupción eléctrica?
- ¿Dónde se procesarán los datos: en cada sensor, en un servidor local o en la nube?
- ¿Hay infraestructura informática disponible o debemos diseñarla y desplegarla nosotros?
- ¿Existen restricciones de acceso, confidencialidad o distribución de los datos?

**Cuestión prioritaria:** ¿La empresa proporciona los sensores y los datos, o espera que el equipo resuelva también la adquisición del hardware?

## 4. Requisitos funcionales del software

El objetivo es convertir la idea general en un conjunto de funcionalidades concretas.

- ¿Qué debe hacer exactamente el sistema desde que recibe una señal hasta que emite una alerta?
- ¿Debe mostrar las mediciones en tiempo real mediante un panel de control?
- ¿Es necesario representar las estaciones y los eventos en un mapa?
- ¿Qué canales de comunicación se utilizarán: SMS, correo electrónico, aplicación, sirenas u otros?
- ¿Habrá distintos niveles de alerta según la gravedad o la confianza de la detección?
- ¿Se necesita un registro histórico de eventos, alertas y decisiones?
- ¿Quién podrá consultar, configurar, confirmar o cancelar una alerta?
- ¿Se requiere autenticación, gestión de permisos o integración con otros sistemas?
- ¿Qué información debe incluir cada notificación?
- ¿Qué ocurre cuando dos sensores ofrecen resultados contradictorios?
- ¿Debe existir un mecanismo de confirmación de recepción de las alertas?
- ¿Qué información debe conservarse para analizar posteriormente cada evento?

**Escenario que conviene solicitar:** que el interlocutor describa qué sucede desde que se produce un terremoto hasta que la persona destinataria recibe la alerta y puede actuar en consecuencia.

## 5. Requisitos no funcionales: rendimiento y fiabilidad

En un sistema de alerta no basta con que el software funcione en condiciones normales. También debe comportarse adecuadamente ante situaciones adversas.

| Aspecto | Pregunta que debe resolverse |
|---|---|
| Latencia | ¿Cuánto tiempo máximo puede transcurrir desde la recepción de los datos hasta la emisión de una alerta? |
| Disponibilidad | ¿Qué porcentaje de tiempo debe estar operativo el sistema? |
| Detección | ¿Qué proporción de eventos sísmicos relevantes debe identificar correctamente? |
| Falsas alarmas | ¿Cuántas alertas erróneas serían aceptables durante un periodo determinado? |
| Omisiones | ¿Qué proporción de eventos relevantes puede dejar de detectar? |
| Escalabilidad | ¿Cuántos sensores, usuarios y eventos simultáneos debe soportar? |
| Resiliencia | ¿Cómo debe actuar ante fallos de sensores, red, alimentación o servidor? |
| Seguridad | ¿Cómo se evitarán la manipulación de mediciones y la emisión fraudulenta de alertas? |
| Trazabilidad | ¿Deben conservarse los datos y las decisiones que originaron cada alerta? |

Deben evitarse expresiones imprecisas como «debe ser rápido», «muy fiable» o «tener gran precisión». Es preferible acordar valores medibles, aunque inicialmente sean provisionales.

Los objetivos definitivos de rendimiento deberán justificarse en función del uso previsto, los datos disponibles y el riesgo asumido.

## 6. Validación y criterios de aceptación

Este bloque permite determinar cómo se comprobará que el sistema satisface las necesidades de la empresa.

- ¿Cómo se determinará que el sistema cumple los requisitos?
- ¿Disponemos de registros sísmicos etiquetados para evaluar los algoritmos?
- ¿Podremos realizar pruebas con señales reales reproducidas, simulaciones y ruido ambiental?
- ¿Quién validará los resultados: la empresa, personal técnico especializado u otro organismo?
- ¿Qué umbrales de detección, falsas alarmas y latencia permitirán aceptar el proyecto?
- ¿Se exige una demostración en tiempo real?
- ¿Qué condiciones deben cumplirse para considerar finalizado el proyecto?
- ¿Quién tendrá la última palabra sobre la aceptación del entregable?
- ¿Se requiere documentación de las pruebas y de sus resultados?
- ¿Se evaluará el funcionamiento ante fallos de sensores, comunicaciones o alimentación?

Las pruebas deben incluir tanto eventos sísmicos como fuentes de vibración que puedan confundirse con ellos. Además, los datos empleados para evaluar el rendimiento no deberían limitarse a aquellos utilizados para ajustar los algoritmos.

## 7. Restricciones, planificación y recursos

El objetivo es identificar las limitaciones que condicionarán el desarrollo y la planificación del proyecto.

- ¿Cuál es la fecha límite de entrega?
- ¿Existe un presupuesto máximo?
- ¿Qué recursos humanos, materiales e informáticos proporciona la empresa?
- ¿Cuántas personas integrarán el equipo y qué responsabilidades asumirá cada una?
- ¿Hay tecnologías, lenguajes, plataformas o proveedores obligatorios?
- ¿Se requiere software libre, licencias comerciales o alguna política concreta de propiedad intelectual?
- ¿Qué documentación debe entregarse además del software?
- ¿Se espera una instalación real o basta con un entorno de demostración?
- ¿Quién mantendrá el sistema una vez concluido el proyecto?
- ¿Qué dependencias externas pueden poner en riesgo la planificación?
- ¿Es posible reducir el alcance si aparecen dificultades técnicas o falta de recursos?

Debe aclararse expresamente si el alcance es negociable. En un proyecto académico, poder priorizar las funcionalidades esenciales puede marcar la diferencia entre completar un prototipo verificable y presentar una colección incompleta de módulos.

## 8. Responsabilidad, seguridad y uso real

Dado que una alerta sísmica puede desencadenar decisiones de emergencia, es necesario aclarar el contexto de utilización del sistema.

- ¿Las alertas tendrán carácter informativo, experimental u operativo?
- ¿Quién está autorizado a emitir una alerta oficial?
- ¿Qué procedimiento se seguirá si el sistema emite una falsa alarma?
- ¿Qué ocurrirá si no detecta un terremoto relevante?
- ¿Debe existir validación humana antes de difundir determinados avisos?
- ¿Qué medidas impedirán que un usuario no autorizado altere las mediciones o genere alertas?
- ¿Hay requisitos legales, institucionales o de interoperabilidad que debamos cumplir?
- ¿Qué organismo será responsable del sistema si se despliega en un entorno real?
- ¿Existen protocolos de actuación que deban seguirse cuando se emita una alerta?
- ¿Qué mecanismos permitirán auditar las decisiones y reconstruir los incidentes?

Debe distinguirse entre un prototipo académico y un producto utilizado para proteger a la población. Las exigencias de validación, seguridad y responsabilidad son sustancialmente diferentes.

## 9. Las doce preguntas prioritarias

Si la reunión fuese breve y solo pudieran resolverse las cuestiones más determinantes, convendría priorizar las siguientes:

1. ¿Qué necesidad operativa concreta pretende resolver el sistema?
2. ¿Se busca detectar actividad sísmica o proporcionar alerta temprana antes de que lleguen las ondas más destructivas?
3. ¿Quién utilizará el sistema y qué decisiones tomará a partir de las alertas?
4. ¿Qué área geográfica y qué tipos de eventos debe cubrir?
5. ¿Qué sensores, datos históricos e infraestructura están disponibles?
6. ¿Qué funcionalidades son imprescindibles y cuáles son opcionales?
7. ¿Qué latencia máxima y qué tasas de detección, falsas alarmas y omisiones se consideran aceptables?
8. ¿Debe funcionar sin Internet o ante fallos de alimentación y comunicaciones?
9. ¿Cómo se probará el sistema y qué condiciones determinarán su aceptación?
10. ¿Qué presupuesto, calendario, recursos humanos y restricciones tecnológicas existen?
11. ¿El resultado esperado es un prototipo académico o un sistema destinado a uso operativo real?
12. ¿Quién será responsable de validar, mantener y autorizar el uso del sistema?

## 10. Documentación que conviene solicitar

Además de las respuestas verbales, es recomendable preguntar si la empresa puede facilitar documentación que permita fundamentar las decisiones de diseño.

- Requisitos operativos o especificaciones preliminares.
- Documentación técnica de los sensores disponibles.
- Registros sísmicos y conjuntos de datos de prueba.
- Diagramas de la infraestructura existente.
- Protocolos de actuación ante emergencias.
- Restricciones de seguridad y acceso a los sistemas.
- Presupuesto estimado y planificación temporal.
- Documentación de sistemas similares que sirvan como referencia.

## 11. Tratamiento de las respuestas después de la reunión

Las respuestas deben convertirse en un documento de requisitos iniciales que distinga claramente entre:

- **Requisitos confirmados:** decisiones expresamente acordadas con la empresa.
- **Supuestos de trabajo:** cuestiones que el equipo necesita dar provisionalmente por ciertas.
- **Restricciones:** límites de presupuesto, plazo, tecnología o infraestructura.
- **Riesgos:** incertidumbres que pueden comprometer el proyecto.
- **Cuestiones abiertas:** decisiones que requieren información adicional o la intervención de un especialista.

Cada requisito importante debería contar, en la medida de lo posible, con un criterio de aceptación verificable.

## 12. Conclusión

La primera decisión que debe resolverse es qué entiende la empresa por un «sistema automático de detección y alerta sísmica».

La respuesta puede transformar un proyecto centrado en procesamiento de señales y notificaciones en otro que requiera una red de sensores distribuida, estimación de parámetros sísmicos y garantías de disponibilidad mucho más exigentes.

Por tanto, antes de decidir tecnologías, algoritmos o arquitectura, el equipo debe comprender la necesidad operativa, delimitar el alcance, identificar los recursos disponibles y acordar cómo se medirá el éxito del proyecto.

# 13. Mi selección

## INICIO
- ¿Cuál es el problema concreto que se pretende resolver mediante este sistema?

## FUNCIONAMIENTO GENERAL
- ¿Cómo y quién recibirá las alertas?
- ¿Qué decisiones se tomarán a partir de una alerta sísmica?
- ¿Qué información debe incluir cada notificación?
- ¿Habrá distintos niveles de alerta según la gravedad o la confianza de la detección?

## FUNCIONAMIENTO CONCRETO
- ¿Qué tipos de eventos sísmicos deben detectarse?
- ¿Se necesita un registro histórico de eventos, alertas y decisiones? ¿Qué información debe conservarse?
- ¿Se requiere autenticación, gestión de permisos o integración con otros sistemas?
- ¿Qué elementos clave visuales deben destacar al entrar al sistema? ¿Sismogramas, mapa...?
- ¿Se busca detectar terremotos reales, identificar vibraciones sospechosas o ambas cosas?
- ¿Se necesitará más de un punto de detección para garantizar que se trate de un sismo?

## DUDAS IMPORTANTES
- ¿Existen sistemas de referencia cuyo funcionamiento deba igualarse o mejorarse?
- ¿De dónde obtenemos los datos, de sensores, APIs...?
- ¿Disponemos de datos históricos de terremotos y de vibraciones no sísmicas?
- ¿Podremos realizar pruebas con señales reales reproducidas, simulaciones y ruido ambiental?

## DOCUMENTACIÓN (si tienen)
- Pedir fórmulas y procedimientos de análisis necesarios para procesar los datos de actividad sísmica y poder crear un modelo de detección y alarma coherente y con error mínimo

## DUDAS FINALES
- ¿Qué funcionalidades son imprescindibles y cuáles podrían considerarse opcionales? ¿Es posible reducir el alcance si aparecen dificultades técnicas o falta de recursos?
- ¿Qué resultado tangible se espera obtener al finalizar el proyecto?
