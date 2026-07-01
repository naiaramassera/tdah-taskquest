import 'package:flutter/material.dart';
import '../../data/services/api_service.dart';
import '../../core/theme/app_colors.dart';
import 'dashboard_screen.dart';

class ProfessionSelectionScreen extends StatefulWidget {
  final String token;

  const ProfessionSelectionScreen({super.key, required this.token});

  @override
  State<ProfessionSelectionScreen> createState() => _ProfessionSelectionScreenState();
}

class _ProfessionSelectionScreenState extends State<ProfessionSelectionScreen> {
  final ApiService _api = ApiService();
  List<dynamic> _professions = [];
  bool _loading = true;
  int? _selectedId;
  bool _saving = false;

  final Map<String, String> _categoryLabels = {
    'saude': '🏥 Saúde',
    'negocios': '💼 Negócios',
    'tecnologia': '💡 Tecnologia',
    'educacao': '📚 Educação',
    'outros': '🌟 Outros',
  };

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final professions = await _api.getProfessions();
      setState(() {
        _professions = professions;
        _loading = false;
      });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  Future<void> _confirm() async {
    if (_selectedId == null) return;
    setState(() => _saving = true);
    try {
      await _api.selectProfession(widget.token, _selectedId!);
      if (!mounted) return;
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (_) => DashboardScreen(token: widget.token)),
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(e.toString().replaceFirst('Exception: ', ''))),
      );
    } finally {
      if (mounted) setState(() => _saving = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final grouped = <String, List<dynamic>>{};
    for (final p in _professions) {
      final cat = p['category'] as String;
      grouped.putIfAbsent(cat, () => []).add(p);
    }

    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [Color(0xFF070A12), Color(0xFF0A1320), Color(0xFF101827)],
          ),
        ),
        child: SafeArea(
          child: Column(
            children: [
              const SizedBox(height: 32),
              const Text(
                '👩‍💼 Qual é a sua profissão?',
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.w900,
                  color: AppColors.textPrimary,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 8),
              const Padding(
                padding: EdgeInsets.symmetric(horizontal: 32),
                child: Text(
                  'Vamos montar missões personalizadas para o seu trabalho!',
                  style: TextStyle(color: AppColors.textSecondary),
                  textAlign: TextAlign.center,
                ),
              ),
              const SizedBox(height: 24),
              Expanded(
                child: _loading
                    ? const Center(child: CircularProgressIndicator())
                    : ListView(
                        padding: const EdgeInsets.symmetric(horizontal: 16),
                        children: [
                          for (final cat in _categoryLabels.keys)
                            if (grouped[cat] != null) ...[
                              Padding(
                                padding: const EdgeInsets.fromLTRB(4, 16, 4, 8),
                                child: Text(
                                  _categoryLabels[cat]!,
                                  style: const TextStyle(
                                    fontWeight: FontWeight.bold,
                                    color: AppColors.textSecondary,
                                    fontSize: 13,
                                    letterSpacing: 0.8,
                                  ),
                                ),
                              ),
                              Wrap(
                                spacing: 10,
                                runSpacing: 10,
                                children: [
                                  for (final p in grouped[cat]!)
                                    _ProfessionChip(
                                      icon: p['icon'] as String,
                                      name: p['name'] as String,
                                      selected: _selectedId == p['id'],
                                      onTap: () => setState(() => _selectedId = p['id'] as int),
                                    ),
                                ],
                              ),
                            ],
                          const SizedBox(height: 100),
                        ],
                      ),
              ),
            ],
          ),
        ),
      ),
      bottomNavigationBar: SafeArea(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(24, 8, 24, 16),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              if (_selectedId != null)
                Text(
                  'Profissão selecionada: ${_professions.firstWhere((p) => p['id'] == _selectedId)['icon']} ${_professions.firstWhere((p) => p['id'] == _selectedId)['name']}',
                  style: const TextStyle(color: AppColors.textSecondary, fontSize: 13),
                ),
              const SizedBox(height: 8),
              SizedBox(
                width: double.infinity,
                child: FilledButton.icon(
                  onPressed: _selectedId == null || _saving ? null : _confirm,
                  icon: _saving
                      ? const SizedBox(
                          width: 18,
                          height: 18,
                          child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                        )
                      : const Icon(Icons.check),
                  label: const Text('Confirmar e começar!'),
                  style: FilledButton.styleFrom(padding: const EdgeInsets.symmetric(vertical: 16)),
                ),
              ),
              TextButton(
                onPressed: () => Navigator.of(context).pushReplacement(
                  MaterialPageRoute(builder: (_) => DashboardScreen(token: widget.token)),
                ),
                child: const Text('Pular por enquanto'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _ProfessionChip extends StatelessWidget {
  final String icon;
  final String name;
  final bool selected;
  final VoidCallback onTap;

  const _ProfessionChip({
    required this.icon,
    required this.name,
    required this.selected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 180),
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: selected ? AppColors.primary : AppColors.border,
            width: selected ? 2 : 1,
          ),
          color: selected
              ? AppColors.primary.withValues(alpha: 0.15)
              : AppColors.surface.withValues(alpha: 0.5),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(icon, style: const TextStyle(fontSize: 20)),
            const SizedBox(width: 8),
            Text(
              name,
              style: TextStyle(
                color: selected ? AppColors.primary : AppColors.textPrimary,
                fontWeight: selected ? FontWeight.bold : FontWeight.normal,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
