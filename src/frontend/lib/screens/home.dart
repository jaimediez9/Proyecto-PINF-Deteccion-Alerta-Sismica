import 'package:flutter/material.dart';
import 'package:frontend/layout/upper_row.dart';
import 'package:frontend/layout/banner_home.dart';

class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          UpperRow(),
          Spacer(),
          BannerHome(),
          SizedBox(height: 20)
        ]
      )
    );
  }
}