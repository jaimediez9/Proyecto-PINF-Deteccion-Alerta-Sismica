import 'package:flutter/material.dart';

class UpperRow extends StatelessWidget {
  const UpperRow({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 25.0),  //DEJAR ESPACIO POR ARRIBA
      child: Container(
        color: Color.fromARGB(255, 88, 172, 255),
        height: 80,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Image.asset("assets/images/logo_armada.png", height: 70,),
            Text("TEXTO PROVISIONAL"),
          ],
          
        ),
      ),
    );    
  }
}