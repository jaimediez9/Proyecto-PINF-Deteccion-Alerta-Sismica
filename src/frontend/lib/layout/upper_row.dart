import 'package:flutter/material.dart';
import 'package:frontend/screens/menu.dart';

class UpperRow extends StatelessWidget {
  final String titulo;
  final IconData icono;
  const UpperRow({
    super.key,
    this.titulo = "SISMO",
    this.icono = Icons.menu
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 25.0), //DEJAR ESPACIO POR ARRIBA
      child: Container(
        color: Color.fromARGB(255, 8, 58, 108),
        height: 80,
        child: Row(
          //mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [

            //ICONO ROA
            if(icono==Icons.menu)
              Image.asset("assets/images/logo_armada.png", height: 70), 
              
            if(icono!=Icons.menu)
              SizedBox(width: 70),
            SizedBox(width: 8),

            //TITULO DE LA PANTALLA
            Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(titulo, style: TextStyle(fontSize: 19, fontWeight: FontWeight.bold, color: Colors.white)),
                if(icono==Icons.menu)
                  Text("Real Observatorio de la Armada", style: TextStyle(color: Colors.white)),
              ],
            ),
            
            Spacer(),

            //BOTÓN DEL MENÚ
            FloatingActionButton(onPressed: (){
              if(icono==Icons.menu){
                Navigator.push(
                context,
                PageRouteBuilder(
                  opaque: false,
                  pageBuilder: (context, animation, secondaryAnimation) => Menu(),
                  transitionsBuilder: (context, animation, secondaryAnimation, child){
                    const begin = Offset(1.0, 0.0);
                    const end = Offset(0.33, 0.0);

                    final tween = Tween(begin: begin, end: end);

                    return SlideTransition(
                    position: animation.drive(tween),
                    child: child,
                    );
                  }
                ),
                );
              }else{
                Navigator.pop(context);
              }
            }, 
            backgroundColor: Color.fromARGB(255, 64, 97, 148),
            foregroundColor: Colors.white,
            elevation: 0,
            heroTag: null,
            child: Icon(icono)
            )
            
          ],
        ),
      ),
    );
  }
}
