import 'package:flutter/material.dart';
import 'package:frontend/layout/options.dart';
import 'package:frontend/layout/upper_row.dart';

class Menu extends StatefulWidget {
  const Menu({super.key});

  @override
  State<Menu> createState() => _MenuState();
}

class _MenuState extends State<Menu> {
  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadiusGeometry.circular(25),
        child: Scaffold(
          body: Container(
            constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.67),
            color: Color.fromARGB(255, 221, 224, 226),
            child: Column(
              children: [
                UpperRow(
                  titulo: "MENÚ",
                  icono: Icons.close
                ),
              Options()
              ],
            ),
          )
        )
    );
  }
}