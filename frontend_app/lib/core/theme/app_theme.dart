import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'app_colors.dart';

class AppTheme {
  static ThemeData darkTheme = ThemeData(
    scaffoldBackgroundColor: AppColors.background,
    primaryColor: AppColors.primary,
    brightness: Brightness.dark,
    colorScheme: const ColorScheme.dark(
      primary: AppColors.primary,
      secondary: AppColors.accent,
      surface: AppColors.surface,
      error: AppColors.danger,
    ),
    textTheme: GoogleFonts.shareTechMonoTextTheme(
      const TextTheme(
        bodyLarge: TextStyle(color: AppColors.textPrimary),
        bodyMedium: TextStyle(color: AppColors.textSecondary),
        bodySmall: TextStyle(color: AppColors.textSecondary),
      ),
    ).copyWith(
      displayLarge: GoogleFonts.orbitron(color: AppColors.primary, fontWeight: FontWeight.w900),
      displayMedium: GoogleFonts.orbitron(color: AppColors.primary, fontWeight: FontWeight.w700),
      headlineLarge: GoogleFonts.orbitron(color: AppColors.textPrimary, fontWeight: FontWeight.w800),
      headlineMedium: GoogleFonts.orbitron(color: AppColors.textPrimary, fontWeight: FontWeight.w700),
      titleLarge: GoogleFonts.orbitron(color: AppColors.textPrimary, fontWeight: FontWeight.w700, fontSize: 16),
      titleMedium: GoogleFonts.shareTechMono(color: AppColors.textPrimary, fontWeight: FontWeight.w600),
      labelSmall: GoogleFonts.shareTechMono(color: AppColors.textSecondary, letterSpacing: 1.2),
    ),
    appBarTheme: AppBarTheme(
      backgroundColor: AppColors.background,
      elevation: 0,
      centerTitle: false,
      titleTextStyle: GoogleFonts.orbitron(
        color: AppColors.primary,
        fontSize: 18,
        fontWeight: FontWeight.w800,
        letterSpacing: 2,
        shadows: [
          Shadow(color: AppColors.primary.withValues(alpha: 0.6), blurRadius: 12),
        ],
      ),
      iconTheme: const IconThemeData(color: AppColors.primary),
      actionsIconTheme: const IconThemeData(color: AppColors.primary),
    ),
    cardTheme: CardThemeData(
      color: AppColors.panel.withValues(alpha: 0.85),
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: const BorderSide(color: AppColors.border),
      ),
    ),
    navigationBarTheme: NavigationBarThemeData(
      backgroundColor: const Color(0xFF080C15),
      indicatorColor: AppColors.primary.withValues(alpha: 0.18),
      iconTheme: WidgetStateProperty.resolveWith((states) {
        if (states.contains(WidgetState.selected)) {
          return const IconThemeData(color: AppColors.primary, size: 22);
        }
        return const IconThemeData(color: AppColors.textSecondary, size: 22);
      }),
      labelTextStyle: WidgetStateProperty.resolveWith((states) {
        if (states.contains(WidgetState.selected)) {
          return GoogleFonts.shareTechMono(
            fontSize: 10,
            color: AppColors.primary,
            fontWeight: FontWeight.w600,
            letterSpacing: 0.8,
          );
        }
        return GoogleFonts.shareTechMono(
          fontSize: 10,
          color: AppColors.textSecondary,
          letterSpacing: 0.5,
        );
      }),
    ),
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: const Color(0xFF0A0F1C),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(8),
        borderSide: const BorderSide(color: AppColors.border),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(8),
        borderSide: BorderSide(color: AppColors.border.withValues(alpha: 0.6)),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(8),
        borderSide: BorderSide(
          color: AppColors.primary,
          width: 1.5,
        ),
      ),
      labelStyle: GoogleFonts.shareTechMono(color: AppColors.textSecondary, fontSize: 13),
      hintStyle: GoogleFonts.shareTechMono(color: AppColors.textSecondary.withValues(alpha: 0.5), fontSize: 13),
      prefixIconColor: AppColors.primary.withValues(alpha: 0.7),
    ),
    filledButtonTheme: FilledButtonThemeData(
      style: FilledButton.styleFrom(
        backgroundColor: AppColors.primary,
        foregroundColor: AppColors.background,
        textStyle: GoogleFonts.orbitron(fontWeight: FontWeight.w700, fontSize: 13, letterSpacing: 1),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
        padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 20),
      ),
    ),
    outlinedButtonTheme: OutlinedButtonThemeData(
      style: OutlinedButton.styleFrom(
        foregroundColor: AppColors.primary,
        side: const BorderSide(color: AppColors.primary),
        textStyle: GoogleFonts.orbitron(fontWeight: FontWeight.w600, fontSize: 12, letterSpacing: 0.8),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      ),
    ),
    textButtonTheme: TextButtonThemeData(
      style: TextButton.styleFrom(
        foregroundColor: AppColors.primary,
        textStyle: GoogleFonts.shareTechMono(fontSize: 13, letterSpacing: 0.5),
      ),
    ),
    chipTheme: ChipThemeData(
      backgroundColor: AppColors.panel,
      side: const BorderSide(color: AppColors.border),
      labelStyle: GoogleFonts.shareTechMono(color: AppColors.textPrimary, fontSize: 12),
    ),
    dividerTheme: const DividerThemeData(
      color: AppColors.border,
      thickness: 1,
    ),
    progressIndicatorTheme: const ProgressIndicatorThemeData(
      color: AppColors.primary,
      linearTrackColor: Color(0xFF0D1521),
    ),
    snackBarTheme: SnackBarThemeData(
      backgroundColor: const Color(0xFF0D1521),
      contentTextStyle: GoogleFonts.shareTechMono(color: AppColors.textPrimary),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(8),
        side: const BorderSide(color: AppColors.border),
      ),
      behavior: SnackBarBehavior.floating,
    ),
    popupMenuTheme: PopupMenuThemeData(
      color: const Color(0xFF0D1521),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(10),
        side: const BorderSide(color: AppColors.border),
      ),
      textStyle: GoogleFonts.shareTechMono(color: AppColors.textPrimary, fontSize: 13),
    ),
  );
}
