import 'package:flutter/material.dart';
import '../../data/services/api_service.dart';
import '../../core/theme/app_colors.dart';

class PersonalActivitiesScreen extends StatefulWidget {
  final String token;
  final int? worldId;

  const PersonalActivitiesScreen({super.key, required this.token, this.worldId});

  @override
  State<PersonalActivitiesScreen> createState() => _PersonalActivitiesScreenState();
}

class _PersonalActivitiesScreenState extends State<PersonalActivitiesScreen> {
  final ApiService _api = ApiService();

  List<dynamic> _categories = [];
  bool _loading = true;
  String? _selectedCategoryId;
  List<dynamic> _activities = [];
  bool _loadingActivities = false;
  final Set<int> _selectedIndices = {};
  bool _saving = false;
  int _addedCount = 0;

  @override
  void initState() {
    super.initState();
    _loadCategories();
  }

  Future<void> _loadCategories() async {
    try {
      final cats = await _api.getPersonalCategories();
      setState(() {
        _categories = cats;
        _loading = false;
      });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  Future<void> _selectCategory(String categoryId) async {
    setState(() {
      _selectedCategoryId = categoryId;
      _selectedIndices.clear();
      _loadingActivities = true;
    });
    try {
      final data = await _api.getPersonalCategoryActivities(categoryId);
      setState(() {
        _activities = (data['activities'] as List<dynamic>? ?? []);
        _loadingActivities = false;
      });
    } catch (_) {
      setState(() => _loadingActivities = false);
    }
  }

  Future<void> _addSelected() async {
    if (_selectedIndices.isEmpty || _selectedCategoryId == null) return;
    setState(() => _saving = true);
    try {
      final indices = _selectedIndices.toList()..sort();
      final result = await _api.addPersonalActivities(
        widget.token,
        categoryId: _selectedCategoryId!,
        activityIndices: indices,
        worldId: widget.worldId,
      );
      final added = (result['added'] as List<dynamic>? ?? []).length;
      setState(() {
        _addedCount += added;
        _selectedIndices.clear();
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('$added atividade(s) adicionada(s)! 🎉'),
            backgroundColor: const Color(0xFF22C55E),
          ),
        );
      }
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(e.toString().replaceFirst('Exception: ', ''))),
      );
    } finally {
      if (mounted) setState(() => _saving = false);
    }
  }

  Color _categoryColor(String colorHex) {
    final hex = colorHex.replaceFirst('#', '');
    return Color(int.parse('FF$hex', radix: 16));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Atividades Pessoais'),
        actions: [
          if (_addedCount > 0)
            Padding(
              padding: const EdgeInsets.only(right: 16),
              child: Center(
                child: Text(
                  '$_addedCount adicionada(s)',
                  style: const TextStyle(color: Color(0xFF22C55E), fontWeight: FontWeight.bold),
                ),
              ),
            ),
        ],
      ),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [Color(0xFF070A12), Color(0xFF0A1320), Color(0xFF101827)],
          ),
        ),
        child: _loading
            ? const Center(child: CircularProgressIndicator())
            : Row(
                children: [
                  // Sidebar de categorias
                  Container(
                    width: 90,
                    color: const Color(0xFF080B14),
                    child: ListView(
                      padding: const EdgeInsets.symmetric(vertical: 8),
                      children: _categories.map((cat) {
                        final isSelected = _selectedCategoryId == cat['id'];
                        final color = _categoryColor(cat['color'] as String);
                        return GestureDetector(
                          onTap: () => _selectCategory(cat['id'] as String),
                          child: AnimatedContainer(
                            duration: const Duration(milliseconds: 150),
                            margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                            padding: const EdgeInsets.symmetric(vertical: 12),
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.circular(10),
                              color: isSelected ? color.withValues(alpha: 0.2) : Colors.transparent,
                              border: isSelected
                                  ? Border.all(color: color.withValues(alpha: 0.6))
                                  : null,
                            ),
                            child: Column(
                              children: [
                                Text(cat['icon'] as String, style: const TextStyle(fontSize: 24)),
                                const SizedBox(height: 4),
                                Text(
                                  cat['name'] as String,
                                  style: TextStyle(
                                    fontSize: 10,
                                    color: isSelected ? color : AppColors.textSecondary,
                                    fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                                  ),
                                  textAlign: TextAlign.center,
                                ),
                              ],
                            ),
                          ),
                        );
                      }).toList(),
                    ),
                  ),
                  // Área de atividades
                  Expanded(
                    child: _selectedCategoryId == null
                        ? const Center(
                            child: Column(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Text('👈', style: TextStyle(fontSize: 48)),
                                SizedBox(height: 12),
                                Text(
                                  'Escolha uma categoria\npara ver as sugestões',
                                  textAlign: TextAlign.center,
                                  style: TextStyle(color: AppColors.textSecondary),
                                ),
                              ],
                            ),
                          )
                        : _loadingActivities
                            ? const Center(child: CircularProgressIndicator())
                            : Column(
                                children: [
                                  Padding(
                                    padding: const EdgeInsets.fromLTRB(16, 12, 16, 4),
                                    child: Row(
                                      children: [
                                        Expanded(
                                          child: Text(
                                            'Selecione as atividades que fazem parte da sua rotina:',
                                            style: TextStyle(
                                              color: AppColors.textSecondary.withValues(alpha: 0.8),
                                              fontSize: 13,
                                            ),
                                          ),
                                        ),
                                        if (_activities.isNotEmpty)
                                          TextButton(
                                            onPressed: () => setState(() {
                                              if (_selectedIndices.length == _activities.length) {
                                                _selectedIndices.clear();
                                              } else {
                                                _selectedIndices.addAll(
                                                  List.generate(_activities.length, (i) => i),
                                                );
                                              }
                                            }),
                                            child: Text(
                                              _selectedIndices.length == _activities.length
                                                  ? 'Desmarcar tudo'
                                                  : 'Selecionar tudo',
                                              style: const TextStyle(fontSize: 12),
                                            ),
                                          ),
                                      ],
                                    ),
                                  ),
                                  Expanded(
                                    child: ListView.builder(
                                      padding: const EdgeInsets.fromLTRB(12, 4, 12, 100),
                                      itemCount: _activities.length,
                                      itemBuilder: (context, index) {
                                        final act = _activities[index] as Map<String, dynamic>;
                                        final selected = _selectedIndices.contains(index);
                                        final diff = act['difficulty'] as int? ?? 1;
                                        final minutes = act['minutes'] as int? ?? 0;
                                        final coinReward = 10 + (diff - 1) * 5;
                                        final xpReward = 15 + (diff - 1) * 10;

                                        return GestureDetector(
                                          onTap: () => setState(() {
                                            if (selected) {
                                              _selectedIndices.remove(index);
                                            } else {
                                              _selectedIndices.add(index);
                                            }
                                          }),
                                          child: AnimatedContainer(
                                            duration: const Duration(milliseconds: 150),
                                            margin: const EdgeInsets.only(bottom: 8),
                                            padding: const EdgeInsets.all(14),
                                            decoration: BoxDecoration(
                                              borderRadius: BorderRadius.circular(12),
                                              border: Border.all(
                                                color: selected
                                                    ? AppColors.primary
                                                    : AppColors.border,
                                                width: selected ? 2 : 1,
                                              ),
                                              color: selected
                                                  ? AppColors.primary.withValues(alpha: 0.1)
                                                  : AppColors.surface.withValues(alpha: 0.4),
                                            ),
                                            child: Row(
                                              children: [
                                                AnimatedContainer(
                                                  duration: const Duration(milliseconds: 150),
                                                  width: 24,
                                                  height: 24,
                                                  decoration: BoxDecoration(
                                                    shape: BoxShape.circle,
                                                    color: selected ? AppColors.primary : Colors.transparent,
                                                    border: Border.all(
                                                      color: selected ? AppColors.primary : AppColors.border,
                                                    ),
                                                  ),
                                                  child: selected
                                                      ? const Icon(Icons.check, size: 14, color: Colors.white)
                                                      : null,
                                                ),
                                                const SizedBox(width: 12),
                                                Expanded(
                                                  child: Column(
                                                    crossAxisAlignment: CrossAxisAlignment.start,
                                                    children: [
                                                      Text(
                                                        act['title'] as String,
                                                        style: const TextStyle(
                                                          fontWeight: FontWeight.w600,
                                                          color: AppColors.textPrimary,
                                                        ),
                                                      ),
                                                      if (act['description'] != null)
                                                        Text(
                                                          act['description'] as String,
                                                          style: const TextStyle(
                                                            fontSize: 12,
                                                            color: AppColors.textSecondary,
                                                          ),
                                                        ),
                                                      const SizedBox(height: 4),
                                                      Row(
                                                        children: [
                                                          Text(
                                                            ['', '😊 Leve', '💪 Média', '🔥 Difícil'][diff],
                                                            style: const TextStyle(fontSize: 11),
                                                          ),
                                                          if (minutes > 0)
                                                            Text(
                                                              '  ⏱ $minutes min',
                                                              style: const TextStyle(
                                                                fontSize: 11,
                                                                color: AppColors.textSecondary,
                                                              ),
                                                            ),
                                                          const Spacer(),
                                                          Text(
                                                            '+$coinReward🪙 +${xpReward}XP',
                                                            style: TextStyle(
                                                              fontSize: 11,
                                                              color: AppColors.primary.withValues(alpha: 0.8),
                                                            ),
                                                          ),
                                                        ],
                                                      ),
                                                    ],
                                                  ),
                                                ),
                                              ],
                                            ),
                                          ),
                                        );
                                      },
                                    ),
                                  ),
                                ],
                              ),
                  ),
                ],
              ),
      ),
      floatingActionButton: _selectedIndices.isNotEmpty
          ? FloatingActionButton.extended(
              onPressed: _saving ? null : _addSelected,
              icon: _saving
                  ? const SizedBox(
                      width: 18,
                      height: 18,
                      child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                    )
                  : const Icon(Icons.add_task),
              label: Text('Adicionar ${_selectedIndices.length} atividade(s)'),
            )
          : null,
      bottomNavigationBar: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: OutlinedButton.icon(
            onPressed: () => Navigator.pop(context, _addedCount > 0),
            icon: const Icon(Icons.check),
            label: Text(_addedCount > 0 ? 'Concluído ($_addedCount adicionada(s))' : 'Fechar'),
          ),
        ),
      ),
    );
  }
}
