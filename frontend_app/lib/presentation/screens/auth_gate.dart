import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../data/services/api_service.dart';
import 'dashboard_screen.dart';
import 'login_screen.dart';
import 'profession_selection_screen.dart';

class AuthGate extends StatefulWidget {
  const AuthGate({super.key});

  @override
  State<AuthGate> createState() => _AuthGateState();
}

class _AuthGateState extends State<AuthGate> {
  String? _token;
  bool _loading = true;
  bool _needsProfession = false;

  @override
  void initState() {
    super.initState();
    _loadToken();
  }

  Future<void> _loadToken() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('auth_token');

    if (token != null) {
      try {
        final api = ApiService();
        final profData = await api.getMyProfession(token);
        final hasProfession = profData['profession'] != null;
        setState(() {
          _token = token;
          _needsProfession = !hasProfession;
          _loading = false;
        });
        return;
      } catch (_) {
        // Se falhar, vai pro dashboard normalmente
      }
    }

    setState(() {
      _token = token;
      _loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    if (_token == null) {
      return const LoginScreen();
    }

    if (_needsProfession) {
      return ProfessionSelectionScreen(token: _token!);
    }

    return DashboardScreen(token: _token!);
  }
}
