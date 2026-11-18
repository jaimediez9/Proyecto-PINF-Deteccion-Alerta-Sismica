import 'package:flutter/material.dart';

class BannerHome extends StatelessWidget {
  const BannerHome({super.key});

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.end,
      children: [  
        FloatingActionButton.extended(
          onPressed: (){},
          shape: StadiumBorder(),
          isExtended: true, 
          backgroundColor: Color.fromARGB(255, 72, 109, 233),
          foregroundColor: Color.fromARGB(255, 255, 255, 255),
          icon: Icon(Icons.map),
          label: Text("Mapa", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18))
        ),
        SizedBox(width: 10)
      ],
    );
  }
}