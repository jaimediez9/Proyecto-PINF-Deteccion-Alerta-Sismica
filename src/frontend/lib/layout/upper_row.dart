import 'package:flutter/material.dart';
import 'package:frontend/screens/menu.dart';

class UpperRow extends StatelessWidget {
  const UpperRow({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 25.0), //DEJAR ESPACIO POR ARRIBA
      child: Container(
        color: Color.fromARGB(255, 88, 172, 255),
        height: 80,
        child: Row(
          //mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [

            //ICONO ROA
            Image.asset("assets/images/logo_armada.png", height: 70), 

            //TITULO DE LA PANTALLA
            Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text("SISMO", style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                Text("Real Observatorio de la Armada"),
              ],
            ),
            
            Spacer(),

            //BOTÓN DEL MENÚ
            FloatingActionButton(onPressed: (){
              Navigator.push(
                context,
                PageRouteBuilder(
                  pageBuilder: (context, animation, secondaryAnimation) => Menu(),
                  transitionsBuilder: (context, animation, secondaryAnimation, child){
                    const begin = Offset(1.0, 0.0);
                    const end = Offset.zero;

                    final tween = Tween(begin: begin, end: end);

                    return SlideTransition(
                    position: animation.drive(tween),
                    child: child,
                    );
                  }
                ),
              );
            }, 
            child: Icon(Icons.menu)
            )
            
          ],
        ),
      ),
    );
  }
}
