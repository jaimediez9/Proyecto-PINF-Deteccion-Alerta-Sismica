# Boceto de Diagrama de Clases UML - Sistema de Alertas Sísmicas

Comprobad que no se me haya escapado nada o añadido cosas que pueden ser comprimidas en otras clases.

<img width="870" height="561" alt="image" src="https://github.com/user-attachments/assets/df1f633c-bee1-469f-bdf9-515251a0263a" />


# Responsabilidades

* **Servidor Web:** Contiene los datos en formato JSON.
* **ParserJSON:** Recibe los datos en formato JSON y la interpreta para transformarla en objetos estructurados reutilizables por el sistema.
* **Datos/Seísmo:** Representa la entidad que contiene la información del JSON.
* **GestorAlertas:** Evalúa los seísmos detectados y decide si se debe crear una notificación y/o registrar el evento.
* **Notificación:** Modela el objeto de la alerta que se presentará en la app, almacenando el mensaje formateado listo para ser enviado.
* **GestorNotifs:** Administra y ejecuta el canal de comunicaciones para despachar las notificaciones creadas hacia los dispositivos finales de los usuarios.
* **ServidorNotif:** Es el servidor que distribuirá la notificación a los usuarios. No podemos enviarla nosotros por la RNF-09: Que no gaste batería ni datos a lo tonto: nada de consultar el servidor sin parar en segundo plano. 
* **RegistroSeísmo:** Gestiona la conexión con la base de datos para guardar y consultar el historial de los seísmos procesados y mantiene una pequeña base de datos temporal para la consulta offline.
* **AvisoLegal:** Si acepta el usuario el aviso podrá usar la app.
* **ConfigUsuario:** Recoge la configuración del usuario introducida a través de la interfaz de usuario.
* **GestorApp:** La clase dios del diagrama. Será la que tenga la responsabilidad de dirigir el programa.
