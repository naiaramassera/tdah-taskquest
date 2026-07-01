import 'package:flutter/material.dart';
import '../../data/services/api_service.dart';
import '../../core/theme/app_colors.dart';

class AchievementsScreen extends StatefulWidget {
  final String token;

  const AchievementsScreen({super.key, required this.token});

  @override
  State<AchievementsScreen> createState() => _AchievementsScreenState();
}

class _AchievementsScreenState extends State<AchievementsScreen> {
  final ApiService _api = ApiService();
  List<dynamic> _achievements = [];
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final data = await _api.getAchievements(widget.token);
      setState(() {
        _achievements = data;
        _loading = false;
      });
    } catch (_) {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final unlocked = _achievements.where((a) => a['unlocked'] == true).toList();
    final locked = _achievements.where((a) => a['unlocked'] != true).toList();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Conquistas'),
        actions: [
          if (!_loading)
            Padding(
              padding: const EdgeInsets.only(right: 16),
              child: Center(
                child: Text(
                  '${unlocked.length}/${_achievements.length}',
                  style: const TextStyle(fontWeight: FontWeight.bold, color: AppColors.primary),
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
            : RefreshIndicator(
                onRefresh: _load,
                child: ListView(
                  padding: const EdgeInsets.all(16),
                  children: [
                    // Progresso geral
                    _ProgressHeader(unlocked: unlocked.length, total: _achievements.length),
                    const SizedBox(height: 20),

                    if (unlocked.isNotEmpty) ...[
                      const _SectionTitle(title: '🏆 Desbloqueadas'),
                      const SizedBox(height: 10),
                      ...unlocked.map((a) => _AchievementCard(achievement: a)),
                      const SizedBox(height: 20),
                    ],

                    if (locked.isNotEmpty) ...[
                      const _SectionTitle(title: '🔒 Em progresso'),
                      const SizedBox(height: 10),
                      ...locked.map((a) => _AchievementCard(achievement: a)),
                    ],
                  ],
                ),
              ),
      ),
    );
  }
}

class _ProgressHeader extends StatelessWidget {
  final int unlocked;
  final int total;

  const _ProgressHeader({required this.unlocked, required this.total});

  @override
  Widget build(BuildContext context) {
    final progress = total == 0 ? 0.0 : unlocked / total;
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(16),
        gradient: LinearGradient(
          colors: [
            AppColors.primary.withValues(alpha: 0.3),
            AppColors.primary.withValues(alpha: 0.1),
          ],
        ),
        border: Border.all(color: AppColors.primary.withValues(alpha: 0.4)),
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text('🏆', style: TextStyle(fontSize: 32)),
              const SizedBox(width: 12),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    '$unlocked de $total conquistas',
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.w900,
                      color: AppColors.textPrimary,
                    ),
                  ),
                  Text(
                    '${(progress * 100).toStringAsFixed(0)}% completo',
                    style: TextStyle(color: AppColors.primary.withValues(alpha: 0.8)),
                  ),
                ],
              ),
            ],
          ),
          const SizedBox(height: 16),
          ClipRRect(
            borderRadius: BorderRadius.circular(999),
            child: LinearProgressIndicator(
              value: progress,
              minHeight: 12,
              backgroundColor: AppColors.background,
              color: AppColors.primary,
            ),
          ),
        ],
      ),
    );
  }
}

class _SectionTitle extends StatelessWidget {
  final String title;
  const _SectionTitle({required this.title});

  @override
  Widget build(BuildContext context) {
    return Text(title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold));
  }
}

class _AchievementCard extends StatelessWidget {
  final Map<String, dynamic> achievement;
  const _AchievementCard({required this.achievement});

  static const _rarityConfig = {
    'common': (label: 'Comum', emoji: '⚪', color: Color(0xFF9CA3AF)),
    'rare': (label: 'Raro', emoji: '🔵', color: Color(0xFF3B82F6)),
    'epic': (label: 'Épico', emoji: '🟣', color: Color(0xFF8B5CF6)),
    'legendary': (label: 'Lendário', emoji: '🟡', color: Color(0xFFF59E0B)),
  };

  @override
  Widget build(BuildContext context) {
    final rarity = achievement['rarity'] as String? ?? 'common';
    final config = _rarityConfig[rarity] ?? _rarityConfig['common']!;
    final unlocked = achievement['unlocked'] as bool? ?? false;
    final progress = achievement['progress'] as int? ?? 0;
    final goal = achievement['goal'] as int? ?? 1;
    final xpReward = achievement['xp_reward'] as int? ?? 0;
    final fraction = goal == 0 ? 0.0 : (progress / goal).clamp(0.0, 1.0);

    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(14),
        border: Border.all(
          color: unlocked ? config.color.withValues(alpha: 0.6) : AppColors.border,
          width: unlocked ? 1.5 : 1,
        ),
        color: unlocked
            ? config.color.withValues(alpha: 0.08)
            : AppColors.surface.withValues(alpha: 0.3),
      ),
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: Row(
          children: [
            // Ícone / troféu
            Container(
              width: 52,
              height: 52,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: unlocked
                    ? config.color.withValues(alpha: 0.2)
                    : AppColors.surface.withValues(alpha: 0.5),
                border: Border.all(
                  color: unlocked ? config.color.withValues(alpha: 0.5) : AppColors.border,
                ),
              ),
              child: Center(
                child: Text(
                  unlocked ? config.emoji : '🔒',
                  style: const TextStyle(fontSize: 24),
                ),
              ),
            ),
            const SizedBox(width: 14),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Expanded(
                        child: Text(
                          achievement['name'] as String,
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            color: unlocked ? AppColors.textPrimary : AppColors.textSecondary,
                          ),
                        ),
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                        decoration: BoxDecoration(
                          color: config.color.withValues(alpha: 0.15),
                          borderRadius: BorderRadius.circular(999),
                          border: Border.all(color: config.color.withValues(alpha: 0.4)),
                        ),
                        child: Text(
                          config.label,
                          style: TextStyle(
                            fontSize: 10,
                            color: config.color,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 2),
                  Text(
                    achievement['description'] as String? ?? '',
                    style: const TextStyle(fontSize: 12, color: AppColors.textSecondary),
                  ),
                  const SizedBox(height: 8),
                  if (!unlocked) ...[
                    Row(
                      children: [
                        Expanded(
                          child: ClipRRect(
                            borderRadius: BorderRadius.circular(999),
                            child: LinearProgressIndicator(
                              value: fraction,
                              minHeight: 6,
                              backgroundColor: AppColors.background,
                              color: config.color,
                            ),
                          ),
                        ),
                        const SizedBox(width: 8),
                        Text(
                          '$progress/$goal',
                          style: TextStyle(
                            fontSize: 11,
                            color: config.color,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 4),
                  ],
                  Text(
                    '+$xpReward XP',
                    style: TextStyle(
                      fontSize: 11,
                      color: unlocked ? config.color : AppColors.textSecondary,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
