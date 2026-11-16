
import 'package:flutter/material.dart';
import 'package:frontend/screens/roa_info_screen.dart';

class UpperRow extends StatelessWidget {
  const UpperRow({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 25.0),
      child: Container(
        color: const Color.fromARGB(255, 88, 172, 255),
        height: 80,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            InkWell(
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => const RoaInfoScreen(),
                  ),
                );
              },
              child: Image.asset(
                "assets/images/escudo_roa.png",
                height: 70,
              ),
            ),
            const Text("TEXTO PROVISIONAL"),
          ],
        ),
      ),
    );
  }
}
