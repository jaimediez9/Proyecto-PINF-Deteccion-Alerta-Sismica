# Boceto de Diagrama de Clases UML - Sistema de Alertas Sísmicas

Comprobad que no se me haya escapado nada o añadido cosas que pueden ser comprimidas en otras clases.

<img width="1052" height="557" alt="Captura de pantalla 2026-10-25 161950" src="https://github.com/user-attachments/assets/b565ee60-1a5b-4783-93bf-45f7664fb520" />

# Responsabilidades

* **Servidor Web:** Contiene los datos en formato JSON.
* **ParserJSON:** Recibe los datos en formato JSON y la interpreta para transformarla en objetos estructurados reutilizables por el sistema.
* **Datos/Seísmo:** Representa la entidad que contiene la información del JSON.
* **GestorAlertas:** Evalúa los seísmos detectados, aplica los filtros de umbral y decide si se debe crear una notificación o registrar el evento.
* **Notificación:** Modela el objeto de la alerta que se presentará en la app, almacenando el mensaje formateado listo para ser enviado.
* **GestorNotifs:** Administra y ejecuta el canal de comunicaciones para despachar las notificaciones creadas hacia los dispositivos finales de los usuarios.
* **Dispositivo:** Representa la aplicación móvil del usuario en iOS o Android y mantiene la información de conexión necesaria para recibir los avisos.
* **RegistroSeísmo:** Gestiona la conexión con la base de datos para guardar y consultar el historial de los seísmos procesados.
