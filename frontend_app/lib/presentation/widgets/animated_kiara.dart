import 'dart:math' as math;

import 'package:flutter/material.dart';

class AnimatedKiara extends StatefulWidget {
  final double size;
  final bool evolved;
  final bool compact;

  const AnimatedKiara({
    super.key,
    this.size = 150,
    this.evolved = false,
    this.compact = false,
  });

  @override
  State<AnimatedKiara> createState() => _AnimatedKiaraState();
}

class _AnimatedKiaraState extends State<AnimatedKiara>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 2600),
    )..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final image = widget.evolved
        ? 'assets/images/kiara_levelup.png'
        : 'assets/images/kiara_base.png';

    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        final t = _controller.value * math.pi * 2;
        final lift = math.sin(t) * (widget.compact ? 2.5 : 7.0);
        final tilt = math.sin(t * 0.7) * 0.035;
        final scale = 1 + (math.sin(t * 1.2) * 0.025);

        return SizedBox(
          width: widget.size,
          height: widget.size + (widget.compact ? 8 : 34),
          child: Stack(
            alignment: Alignment.center,
            children: [
              Positioned.fill(
                child: CustomPaint(
                  painter: _KiaraAuraPainter(
                    progress: _controller.value,
                    compact: widget.compact,
                  ),
                ),
              ),
              Positioned(
                bottom: widget.compact ? 2 : 8,
                child: Transform.translate(
                  offset: Offset(0, lift),
                  child: Transform.rotate(
                    angle: tilt,
                    child: Transform.scale(
                      scale: scale,
                      child: Image.asset(
                        image,
                        width: widget.size * 0.82,
                        fit: BoxFit.contain,
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}

class _KiaraAuraPainter extends CustomPainter {
  final double progress;
  final bool compact;

  _KiaraAuraPainter({
    required this.progress,
    required this.compact,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final pulse = 0.5 + (math.sin(progress * math.pi * 2) * 0.5);

    final glowPaint = Paint()
      ..shader = RadialGradient(
        colors: [
          const Color(0xFF00F5D4).withValues(alpha: 0.22 + pulse * 0.10),
          const Color(0xFFFFD166).withValues(alpha: 0.08),
          Colors.transparent,
        ],
      ).createShader(Rect.fromCircle(
        center: center,
        radius: size.width * 0.55,
      ));

    canvas.drawCircle(center, size.width * (compact ? 0.34 : 0.43), glowPaint);

    final orbitPaint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.2
      ..color = const Color(0xFF00F5D4).withValues(alpha: compact ? 0.14 : 0.24);

    if (!compact) {
      canvas.drawOval(
        Rect.fromCenter(
          center: center.translate(0, 4),
          width: size.width * 0.82,
          height: size.height * 0.34,
        ),
        orbitPaint,
      );
    }

    final particlePaint = Paint()..style = PaintingStyle.fill;
    final count = compact ? 5 : 9;
    for (var i = 0; i < count; i++) {
      final phase = (progress + i / count) * math.pi * 2;
      final radiusX = size.width * (compact ? 0.34 : 0.42);
      final radiusY = size.height * (compact ? 0.18 : 0.23);
      final position = Offset(
        center.dx + math.cos(phase) * radiusX,
        center.dy + math.sin(phase * 1.15) * radiusY,
      );
      final brightness = 0.45 + math.sin(phase) * 0.35;
      particlePaint.color = (i.isEven
              ? const Color(0xFF00F5D4)
              : const Color(0xFFFFD166))
          .withValues(alpha: brightness.clamp(0.18, 0.8));
      canvas.drawCircle(position, compact ? 2.0 : 3.2, particlePaint);
    }
  }

  @override
  bool shouldRepaint(covariant _KiaraAuraPainter oldDelegate) {
    return oldDelegate.progress != progress || oldDelegate.compact != compact;
  }
}
