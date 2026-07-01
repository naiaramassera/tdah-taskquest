import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../data/services/api_service.dart';
import '../../core/theme/app_colors.dart';
import '../widgets/animated_kiara.dart';
import 'dashboard_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final ApiService _apiService = ApiService();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  bool _isLoading = false;
  String? _error;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _login() async => _submit(createAccount: false);
  Future<void> _register() async => _submit(createAccount: true);

  Future<void> _submit({required bool createAccount}) async {
    final email = _emailController.text.trim();
    final password = _passwordController.text;

    if (email.isEmpty || password.isEmpty) {
      setState(() => _error = 'Preencha email e senha.');
      return;
    }

    setState(() { _isLoading = true; _error = null; });

    try {
      if (createAccount) await _apiService.register(email, password);
      final token = await _apiService.login(email, password);
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('auth_token', token);

      if (!mounted) return;
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (_) => DashboardScreen(token: token)),
      );
    } catch (_) {
      if (!mounted) return;
      setState(() {
        _error = createAccount ? 'Nao foi possivel criar a conta.' : 'Nao foi possivel entrar.';
      });
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          // Tech grid background
          Container(
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
                colors: [Color(0xFF040608), Color(0xFF070A12), Color(0xFF0A1320)],
              ),
            ),
          ),
          CustomPaint(painter: _GridPainter(), size: Size.infinite),
          // Glow top-right
          Positioned(
            top: -100,
            right: -100,
            child: Container(
              width: 400,
              height: 400,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                boxShadow: [BoxShadow(color: AppColors.primary.withValues(alpha: 0.07), blurRadius: 120, spreadRadius: 40)],
              ),
            ),
          ),
          SafeArea(
            child: Center(
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 420),
                child: SingleChildScrollView(
                  padding: const EdgeInsets.all(24),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const AnimatedKiara(size: 160),
                      const SizedBox(height: 8),
                      // Logo title
                      Text(
                        'TASKQUEST',
                        style: GoogleFonts.orbitron(
                          fontSize: 28,
                          fontWeight: FontWeight.w900,
                          color: AppColors.primary,
                          letterSpacing: 4,
                          shadows: [Shadow(color: AppColors.primary.withValues(alpha: 0.6), blurRadius: 20)],
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        '// sistema de foco para mentes neurodivergentes',
                        style: GoogleFonts.shareTechMono(
                          fontSize: 11,
                          color: AppColors.textSecondary,
                          letterSpacing: 0.5,
                        ),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 28),
                      // Panel
                      Container(
                        padding: const EdgeInsets.all(24),
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(16),
                          color: const Color(0xFF0A0F1C),
                          border: Border.all(color: AppColors.border),
                          boxShadow: [
                            BoxShadow(
                              color: AppColors.primary.withValues(alpha: 0.06),
                              blurRadius: 24,
                              spreadRadius: 0,
                            ),
                          ],
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.stretch,
                          children: [
                            Text(
                              '> ACESSO AO SISTEMA',
                              style: GoogleFonts.shareTechMono(
                                fontSize: 11,
                                color: AppColors.primary.withValues(alpha: 0.6),
                                letterSpacing: 1,
                              ),
                            ),
                            const SizedBox(height: 16),
                            TextField(
                              controller: _emailController,
                              keyboardType: TextInputType.emailAddress,
                              decoration: const InputDecoration(
                                labelText: 'Email',
                                prefixIcon: Icon(Icons.alternate_email),
                              ),
                            ),
                            const SizedBox(height: 12),
                            TextField(
                              controller: _passwordController,
                              obscureText: true,
                              decoration: const InputDecoration(
                                labelText: 'Senha',
                                prefixIcon: Icon(Icons.lock_outline),
                              ),
                            ),
                            if (_error != null) ...[
                              const SizedBox(height: 12),
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                                decoration: BoxDecoration(
                                  borderRadius: BorderRadius.circular(6),
                                  color: AppColors.danger.withValues(alpha: 0.12),
                                  border: Border.all(color: AppColors.danger.withValues(alpha: 0.4)),
                                ),
                                child: Text(
                                  _error!,
                                  style: GoogleFonts.shareTechMono(color: AppColors.danger, fontSize: 12),
                                ),
                              ),
                            ],
                            const SizedBox(height: 20),
                            FilledButton(
                              onPressed: _isLoading ? null : _login,
                              child: Text(_isLoading ? 'CONECTANDO...' : 'ENTRAR'),
                            ),
                            const SizedBox(height: 8),
                            OutlinedButton(
                              onPressed: _isLoading ? null : _register,
                              child: const Text('CRIAR CONTA'),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _GridPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = AppColors.primary.withValues(alpha: 0.03)
      ..strokeWidth = 1;
    const step = 30.0;
    for (var x = 0.0; x < size.width; x += step) {
      canvas.drawLine(Offset(x, 0), Offset(x, size.height), paint);
    }
    for (var y = 0.0; y < size.height; y += step) {
      canvas.drawLine(Offset(0, y), Offset(size.width, y), paint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
