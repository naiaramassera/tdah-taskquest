import 'package:flutter/material.dart';
import 'package:audioplayers/audioplayers.dart';
import 'package:vibration/vibration.dart';
import 'dart:math';
import '../../core/theme/app_colors.dart';

class KiaraUnlockAnimation extends StatefulWidget {
  final String skinName;

  const KiaraUnlockAnimation({super.key, required this.skinName});

  @override
  State<KiaraUnlockAnimation> createState() =>
      _KiaraUnlockAnimationState();
}

class _KiaraUnlockAnimationState extends State<KiaraUnlockAnimation>
    with SingleTickerProviderStateMixin {

  late AnimationController _controller;
  final player = AudioPlayer();

  @override
void initState() {
  super.initState();
  loadData();
}

Future<void> loadData() async {
  try {
    final data = await _apiService.getHomeData(token);
    setState(() {
      homeData = data;
      isLoading = false;
    });
  } catch (e) {
    print(e);
  }
}

  void _playEffects() async {
    if (await Vibration.hasVibrator() ?? false) {
      Vibration.vibrate(duration: 200);
    }

    await player.play(AssetSource('sounds/reward.mp3'));
  }

  @override
  void dispose() {
    _controller.dispose();
    player.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      backgroundColor: Colors.transparent,
      child: AnimatedBuilder(
        animation: _controller,
        builder: (context, child) {
          return Stack(
            alignment: Alignment.center,
            children: [
              // Fundo mágico
              Container(
                decoration: const BoxDecoration(
                  gradient: RadialGradient(
                    colors: [
                      Color(0xFF1E1B4B),
                      Colors.black,
                    ],
                  ),
                ),
              ),

              // Partículas
              ...List.generate(20, (index) {
                return Positioned(
                  top: Random().nextDouble() * 400,
                  left: Random().nextDouble() * 300,
                  child: Opacity(
                    opacity: _controller.value,
                    child: const Icon(
                      Icons.star,
                      size: 12,
                      color: Colors.amber,
                    ),
                  ),
                );
              }),

              Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  // Brilho circular
                  Container(
                    width: 250 + (_controller.value * 50),
                    height: 250 + (_controller.value * 50),
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: AppColors.primary
                          .withOpacity(0.2 * (1 - _controller.value)),
                    ),
                  ),

                  const SizedBox(height: 20),

                  // Kiara real
                  Image.asset(
                    "assets/images/kiara_levelup.png",
                    height: 150,
                  ),

                  const SizedBox(height: 20),

                  const Text(
                    "✨ Kiara evoluiu! ✨",
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                    ),
                  ),

                  const SizedBox(height: 10),

                  Text(
                    widget.skinName,
                    style: const TextStyle(
                      color: Colors.amber,
                      fontSize: 18,
                    ),
                  ),

                  const SizedBox(height: 30),

                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.primary,
                    ),
                    onPressed: () => Navigator.pop(context),
                    child: const Text("Continuar"),
                  )
                ],
              ),
            ],
          );
        },
      ),
    );
  }
}