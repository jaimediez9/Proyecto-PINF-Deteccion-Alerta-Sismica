import 'package:flutter/material.dart';

class Options extends StatelessWidget {
  const Options({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        SizedBox(height: 2),

        //BOTÓN DE INFORMACIÓN
        Container(
          constraints: BoxConstraints(minHeight: 60),
          decoration: ShapeDecoration(color: Colors.white, shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(0))),
          child: Row(
            children: [
              SizedBox(width: 5),
              Icon(Icons.info_outline),
              SizedBox(width: 5),
              Text("Información"),
              Spacer(),
              Icon(Icons.chevron_right),
              SizedBox(width: 5)
            ],
          )
        ),
        SizedBox(height: 2),

        //BOTÓN DE CONSEJOS
        Container(
          constraints: BoxConstraints(minHeight: 60),
          decoration: ShapeDecoration(color: Colors.white, shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(0))),
          child: Row(
            children: [
              SizedBox(width: 5),
              Icon(Icons.lightbulb_outline),
              SizedBox(width: 5),
              Text("Consejos"),
              Spacer(),
              Icon(Icons.chevron_right),
              SizedBox(width: 5)
            ],
          )
        ),
        SizedBox(height: 2),

        //BOTÓN DE GLOSARIO
        Container(
          constraints: BoxConstraints(minHeight: 60),
          decoration: ShapeDecoration(color: Colors.white, shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(0))),
          child: Row(
            children: [
              SizedBox(width: 5),
              Icon(Icons.book_outlined),
              SizedBox(width: 5),
              Text("Glosario"),
              Spacer(),
              Icon(Icons.chevron_right),
              SizedBox(width: 5)
            ],
          )
        ),
        SizedBox(height: 2),

        //BOTÓN DE AJUSTES
        Container(
          constraints: BoxConstraints(minHeight: 60),
          decoration: ShapeDecoration(color: Colors.white, shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(0))),
          child: Row(
            children: [
              SizedBox(width: 5),
              Icon(Icons.settings),
              SizedBox(width: 5),
              Text("Ajustes"),
              Spacer(),
              Icon(Icons.chevron_right),
              SizedBox(width: 5)
            ],
          )
        )
      ],
    );
  }
}