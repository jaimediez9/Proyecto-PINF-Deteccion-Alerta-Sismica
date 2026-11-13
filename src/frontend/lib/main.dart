//Main para ejecutar la aplicacion

import 'package:flutter/material.dart';
import 'package:frontend/layout/upper_row.dart';
//import 'package:frontend/layout/lista_terremotos.dart';

void main() {
  runApp(const MiAplicacion());
}

class MiAplicacion extends StatelessWidget {
  const MiAplicacion({super.key});

  @override
  Widget build(BuildContext context){
    return const MaterialApp(
      home: Scaffold(
        body: UpperRow(), //barra de arriba con logo y ajustes
        //ListaTerremotos(), //Aqui quiero meter una columna para poner la lista de terremotos
      ),
    );
  }
}
