# Bocetos de Diagramas - Sistema de Alertas Sísmicas

# Diagrama de Casos de Uso

Actores: Usuario, Servidor del ROA, Servidor de Notificaciones y el Sistema.
Subsistemas del problema:
* Consulta y Visualización: Todo lo que sea consultar datos (mapa, magnitud, distancia...), ya sea con conexión u offline.
* Configuración y Recepción de Avisos: Muestra el aviso legal, recoge permisos, la configuración de cada usuario personalizada, poder activar o desactivar el sonido, vibración o directamente la notificación completa y poder abrir los datos de la notificación a través de su alerta sin estar en la app (o entrar en la app para consultar la notificación).
* Gestión de Datos: Recolecta de datos del servidor, sincronización con la base de datos y caché local, comprobación de configuración del usuario para las notificaciones correspondientes y almacenamiento de datos (en caso de no estar ya registrado el seísmo).

<img width="1142" height="600" alt="image" src="https://github.com/user-attachments/assets/e66a8ee3-4a28-4bc3-9712-cda6030d186d" />

**ALGUNAS RELACIONES ENTRE CASOS DE USO**

* C2 extensión de C1.
* C5 incluido en C1 y C2.
* C7 extensión de C6.
* C9 extensión de C8.
* C1 incluye a C10.
* C11 incluye a C12 y C13.

# Diagrama de Clases - Imprescindible

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
