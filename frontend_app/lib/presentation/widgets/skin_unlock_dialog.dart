import 'package:flutter/material.dart';
import '../../core/theme/app_colors.dart';

class SkinUnlockDialog extends StatelessWidget {
  final String skinName;

  const SkinUnlockDialog({super.key, required this.skinName});

  @override
  Widget build(BuildContext context) {
    return Dialog(
      backgroundColor: AppColors.surface,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(20),
      ),
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text(
              "✨ Nova Skin Desbloqueada! ✨",
              style: TextStyle(
                fontSize: 20,
                color: AppColors.textPrimary,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 20),
            Text(
              skinName,
              style: const TextStyle(
                fontSize: 18,
                color: AppColors.primary,
              ),
            ),
            const SizedBox(height: 30),
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.primary,
              ),
              onPressed: () => Navigator.pop(context),
              child: const Text("Ver Kiara 🐶"),
            )
          ],
        ),
      ),
    );
  }
}