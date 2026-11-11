//Main para ejecutar la aplicacion

import 'package:flutter/material.dart';
//import 'terremoto.dart';

void main() {
  runApp(const MiAplicacion());
}

class MiAplicacion extends StatelessWidget {
  const MiAplicacion({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: PantallaListaTerremotos(), //llamamos a nuestra pantalla
    );
  }
}

class PantallaListaTerremotos extends StatelessWidget {
  const PantallaListaTerremotos({super.key});

  @override
  Widget build(BuildContext context){
    return Scaffold(
      body: Center(
        child: Text('Hola'),
      ),
    );
  }
}