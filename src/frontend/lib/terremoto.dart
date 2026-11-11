class Terremoto {

  final String id;
  final String zona;
  final double magnitud;
  final DateTime fecha;
  final DateTime hora;

  Terremoto({                    //obligatorio pasar estos 3 datos
    required this.id,
    required this.zona,
    required this.magnitud,
    required this.fecha,
    required this.hora,
  });

  factory Terremoto.fromJson(Map<String, dynamic> json){
    final props = json['propiedades'] ?? json;
    
    // Extraemos los milisegundos de la fecha/hora
    final int timestamp = props['time'] ?? 0;
    final fechaCompleta = DateTime.fromMillisecondsSinceEpoch(timestamp);

    return Terremoto(   //cuando tengamos los json hay que revisar esto que las variables me las he inventado
      id: json['id'] ?? 'sin_id',
      zona: props['zona'] ?? 'Zona desconocida',
      magnitud: (props['mag'] ?? 0).toDouble(),
      fecha: fechaCompleta, // En Dart, DateTime incluye tanto la fecha como la hora
      hora: fechaCompleta
    );
  }
}