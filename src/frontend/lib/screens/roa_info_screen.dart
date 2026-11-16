
import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
//Todo esto es con información provisional. Cuando nos den los textos los pego aquí
class RoaInfoScreen extends StatelessWidget {
  const RoaInfoScreen({super.key});

  // Funcion para abrir paginas web
  Future<void> abrirWeb(String url) async {
    final Uri uri = Uri.parse(url);

    if (!await launchUrl(
      uri,
      mode: LaunchMode.externalApplication,
    )) {
      throw Exception('No se pudo abrir la pagina');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Información del ROA'),
        backgroundColor: const Color.fromARGB(255, 88, 172, 255),
      ),

      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [

            // Escudos
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                Image.asset(
                  'assets/images/escudo_roa.png',
                  height: 120,
                  width: 120,
                  fit: BoxFit.contain,
                ),

                Image.asset(
                  'assets/images/logo_armada.png',
                  height: 120,
                  width: 120,
                  fit: BoxFit.contain,
                ),
              ],
            ),

            const SizedBox(height: 25),

            // Titulo
            const Text(
              'Real Instituto y Observatorio de la Armada',
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 20),

            // Informacion
            const Text(
              'El Real Instituto y Observatorio de la Armada '
              '(ROA) es un centro científico de la Armada Española '
              'situado en San Fernando (Cádiz).\n\n'
              'Fundado en 1753 por iniciativa de Jorge Juan, '
              'sus orígenes están relacionados con la necesidad '
              'de formar a los oficiales de Marina en astronomía, '
              'una disciplina fundamental para la navegación.\n\n'
              'Actualmente desarrolla actividades de investigación '
              'en astronomía, geofísica, geodesia y otras ciencias '
              'físico-matemáticas de interés para la Armada.\n\n'
              'Además, es responsable de mantener y difundir '
              'la hora oficial de España.',
              textAlign: TextAlign.justify,
              style: TextStyle(
                fontSize: 16,
                height: 1.5,
              ),
            ),

            const SizedBox(height: 30),

            // Enlaces
            const Align(
              alignment: Alignment.centerLeft,
              child: Text(
                'Enlaces de interés',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),

            const SizedBox(height: 10),

            ListTile(
              leading: const Icon(Icons.public),
              title: const Text('Página oficial del ROA'),
              trailing: const Icon(Icons.open_in_new),
              onTap: () => abrirWeb(
                'https://armada.defensa.gob.es/ArmadaPortal/page/Portal/ArmadaEspannola/cienciaobservatorio/prefLang-es/02InfoGeneral--02Misiones-es',
              ),
            ),

            ListTile(
              leading: const Icon(Icons.language),
              title: const Text('Página oficial de la Armada'),
              trailing: const Icon(Icons.open_in_new),
              onTap: () => abrirWeb(
                'https://armada.defensa.gob.es/',
              ),
            ),
          ],
        ),
      ),
    );
  }
}
