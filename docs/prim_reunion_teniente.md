# Primera Reunión con el Teniente

Aquí dejo las notas y el resumen de lo que estuvimos hablando en la primera reunión con el Teniente sobre las necesidades del proyecto.

---

### 1. Objetivo Principal
* Desarrollar una **aplicación móvil (iOS y Android)**.
* La app debe ser capaz de **enviar notificaciones** al dispositivo cada vez que se registre un seísmo.

### 2. Recepción y Manejo de Datos
* Recibiremos la información del seísmo en formato **JSON** con todos los datos necesarios ya incluidos.
* En esta primera fase, nuestra tarea principal consistirá en procesar ese JSON y lanzar la notificación push correspondiente con los detalles del seísmo.
* **Pendiente de definir:** Aún no está 100% confirmado cómo nos llegará esta información, pero lo más probable es que monten un servidor web desde el que podamos extraer los datos.

### 3. Próximos Pasos y Posibles Ampliaciones
* Lo prioritario es dejar funcional el sistema base de alertas por seísmo.
* Si el desarrollo de esta parte principal va bien, se podría hacer algunas ampliaciones (como por ejemplo, **alertas y advertencias de tsunamis**). Esto se irá viendo a medida que avancemos.
