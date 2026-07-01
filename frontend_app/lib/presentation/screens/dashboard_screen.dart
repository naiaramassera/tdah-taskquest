import 'dart:async';

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../data/services/api_service.dart';
import '../../core/theme/app_colors.dart';
import '../widgets/animated_kiara.dart';
import 'login_screen.dart';
import 'profession_selection_screen.dart';
import 'personal_activities_screen.dart';
import 'achievements_screen.dart';

class DashboardScreen extends StatefulWidget {
  final String token;

  const DashboardScreen({super.key, required this.token});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  final ApiService _apiService = ApiService();

  int _tabIndex = 0;
  bool _loading = true;
  String? _error;

  Map<String, dynamic>? _home;
  List<dynamic> _worlds = [];
  List<dynamic> _routines = [];
  Map<String, dynamic> _missions = {};
  List<dynamic> _skins = [];
  Map<String, dynamic>? _myProfession;

  // Timers por rotina: routineId → segundos restantes
  final Map<int, int> _activeTimers = {};
  final Map<int, Timer> _timerInstances = {};

  int? _focusSessionId;
  int _focusSeconds = 25 * 60;
  Timer? _focusTimer;

  @override
  void initState() {
    super.initState();
    _loadAll();
  }

  @override
  void dispose() {
    _focusTimer?.cancel();
    for (final t in _timerInstances.values) {
      t.cancel();
    }
    super.dispose();
  }

  Future<void> _loadAll() async {
    setState(() {
      _loading = true;
      _error = null;
    });

    try {
      final results = await Future.wait([
        _apiService.getHomeData(widget.token),
        _apiService.getWorlds(widget.token),
        _apiService.getRoutines(widget.token),
        _apiService.getMissions(widget.token),
        _apiService.getSkins(widget.token),
        _apiService.getMyProfession(widget.token),
      ]);

      setState(() {
        _home = results[0] as Map<String, dynamic>;
        _worlds = results[1] as List<dynamic>;
        _routines = results[2] as List<dynamic>;
        _missions = results[3] as Map<String, dynamic>;
        _skins = results[4] as List<dynamic>;
        final profData = results[5] as Map<String, dynamic>;
        _myProfession = profData['profession'] as Map<String, dynamic>?;
      });
    } catch (_) {
      setState(() => _error = 'Nao foi possivel carregar seus dados.');
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  Future<void> _logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('auth_token');
    if (!mounted) return;
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(builder: (_) => const LoginScreen()),
    );
  }

  Future<void> _runAction(Future<void> Function() action) async {
    try {
      await action();
      await _loadAll();
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(error.toString().replaceFirst('Exception: ', ''))),
      );
    }
  }

  void _showRewardPopup({
    required int xp,
    required int coins,
    bool levelUp = false,
    Map<String, dynamic>? combo,
  }) {
    showDialog(
      context: context,
      barrierDismissible: true,
      builder: (_) => _RewardPopup(xp: xp, coins: coins, levelUp: levelUp, combo: combo),
    );
  }

  void _showBossDefeatPopup(Map<String, dynamic> defeat) {
    showDialog(
      context: context,
      barrierDismissible: true,
      builder: (_) => _BossDefeatPopup(defeat: defeat),
    );
  }

  Future<void> _completeRoutine(int routineId) async {
    try {
      final result = await _apiService.completeRoutine(widget.token, routineId);
      _timerInstances[routineId]?.cancel();
      _timerInstances.remove(routineId);
      setState(() => _activeTimers.remove(routineId));

      final xpResult = result['xp_result'] as Map<String, dynamic>?;
      final levelUp = xpResult?['level_up'] == true;
      final xpGained = result['xp_gained'] as int? ?? 0;
      final coinsGained = result['coins_gained'] as int? ?? 0;
      final combo = result['combo'] as Map<String, dynamic>?;
      final bossDefeat = result['boss_defeat'] as Map<String, dynamic>?;

      await _loadAll();
      if (mounted) {
        _showRewardPopup(xp: xpGained, coins: coinsGained, levelUp: levelUp, combo: combo);
        if (bossDefeat != null) {
          await Future.delayed(const Duration(milliseconds: 2400));
          if (mounted) _showBossDefeatPopup(bossDefeat);
        }
      }
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(error.toString().replaceFirst('Exception: ', ''))),
      );
    }
  }

  void _startTimer(int routineId, int minutes) {
    _timerInstances[routineId]?.cancel();
    setState(() => _activeTimers[routineId] = minutes * 60);

    _timerInstances[routineId] = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (!mounted) {
        timer.cancel();
        return;
      }
      final current = _activeTimers[routineId] ?? 0;
      if (current <= 1) {
        timer.cancel();
        setState(() => _activeTimers[routineId] = 0);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('⏰ Tempo esgotado!')),
        );
      } else {
        setState(() => _activeTimers[routineId] = current - 1);
      }
    });
  }

  Future<void> _completeDailyTask(int taskId) async {
    try {
      final result = await _apiService.completeDailyTaskWithResult(widget.token, taskId);
      final xpResult = result['xp_result'] as Map<String, dynamic>?;
      final levelUp = xpResult?['level_up'] == true;
      final xpGained = result['xp_gained'] as int? ?? (xpResult?['xp_gained'] as int?) ?? 10;
      final coinsGained = result['coins_gained'] as int? ?? 10;
      final combo = result['combo'] as Map<String, dynamic>?;

      await _loadAll();
      if (mounted) {
        _showRewardPopup(xp: xpGained, coins: coinsGained, levelUp: levelUp, combo: combo);
      }
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(error.toString().replaceFirst('Exception: ', ''))),
      );
    }
  }

  Future<void> _createWorld({String type = 'custom'}) async {
    final name = TextEditingController();
    final icon = TextEditingController(text: type == 'personal' ? '🏠' : '💼');
    final color = TextEditingController(text: type == 'personal' ? '#22C55E' : '#4F46E5');

    final saved = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(type == 'personal'
            ? 'Mundo Pessoal'
            : type == 'professional'
                ? 'Mundo Profissional'
                : 'Novo mundo'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(controller: name, decoration: const InputDecoration(labelText: 'Nome')),
            TextField(controller: icon, decoration: const InputDecoration(labelText: 'Emoji')),
            TextField(controller: color, decoration: const InputDecoration(labelText: 'Cor #RRGGBB')),
          ],
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('Cancelar')),
          FilledButton(onPressed: () => Navigator.pop(context, true), child: const Text('Salvar')),
        ],
      ),
    );

    if (saved == true && name.text.trim().isNotEmpty) {
      await _runAction(() => _apiService.createWorld(
            widget.token,
            name: name.text.trim(),
            icon: icon.text.trim(),
            color: color.text.trim(),
          ));
    }
  }

  Future<void> _createRoutine(int worldId) async {
    final title = TextEditingController();
    final description = TextEditingController();
    int difficulty = 1;
    int? timeLimitMinutes;
    final timeCtrl = TextEditingController();

    final saved = await showDialog<bool>(
      context: context,
      builder: (context) => StatefulBuilder(
        builder: (context, setDialogState) => AlertDialog(
          title: const Text('Nova atividade'),
          content: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                TextField(
                  controller: title,
                  decoration: const InputDecoration(
                    labelText: 'Nome da atividade',
                    hintText: 'Ex: Arrumar o quarto',
                  ),
                ),
                const SizedBox(height: 12),
                TextField(
                  controller: description,
                  decoration: const InputDecoration(
                    labelText: 'Descrição (opcional)',
                    hintText: 'Ex: Guardar roupas e limpar o pó',
                  ),
                ),
                const SizedBox(height: 16),
                const Text('Dificuldade', style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600)),
                const SizedBox(height: 8),
                SegmentedButton<int>(
                  segments: const [
                    ButtonSegment(value: 1, label: Text('Leve'), icon: Text('😊')),
                    ButtonSegment(value: 2, label: Text('Média'), icon: Text('💪')),
                    ButtonSegment(value: 3, label: Text('Difícil'), icon: Text('🔥')),
                  ],
                  selected: {difficulty},
                  onSelectionChanged: (value) => setDialogState(() => difficulty = value.first),
                ),
                const SizedBox(height: 16),
                TextField(
                  controller: timeCtrl,
                  keyboardType: TextInputType.number,
                  decoration: const InputDecoration(
                    labelText: 'Tempo limite (minutos)',
                    hintText: 'Ex: 30',
                    prefixIcon: Icon(Icons.timer_outlined),
                  ),
                  onChanged: (v) => timeLimitMinutes = int.tryParse(v),
                ),
                const SizedBox(height: 4),
                const Text(
                  'Recompensas aumentam com a dificuldade',
                  style: TextStyle(fontSize: 11, color: AppColors.textSecondary),
                ),
              ],
            ),
          ),
          actions: [
            TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('Cancelar')),
            FilledButton(onPressed: () => Navigator.pop(context, true), child: const Text('Adicionar')),
          ],
        ),
      ),
    );

    if (saved == true && title.text.trim().isNotEmpty) {
      await _runAction(() => _apiService.createRoutine(
            widget.token,
            worldId: worldId,
            title: title.text.trim(),
            difficulty: difficulty,
            timeLimitMinutes: timeLimitMinutes,
            description: description.text.trim().isEmpty ? null : description.text.trim(),
          ));
    }
  }

  Future<void> _startFocus(int taskId) async {
    try {
      final session = await _apiService.startFocus(widget.token, taskId);
      _focusTimer?.cancel();
      setState(() {
        _focusSessionId = session['id'] as int;
        _focusSeconds = 25 * 60;
      });
      _focusTimer = Timer.periodic(const Duration(seconds: 1), (timer) {
        if (!mounted) return;
        if (_focusSeconds <= 1) {
          timer.cancel();
          setState(() => _focusSeconds = 0);
        } else {
          setState(() => _focusSeconds--);
        }
      });
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(error.toString().replaceFirst('Exception: ', ''))),
      );
    }
  }

  Future<void> _finishFocus() async {
    final sessionId = _focusSessionId;
    if (sessionId == null) return;
    await _runAction(() async {
      await _apiService.finishFocus(widget.token, sessionId);
      _focusTimer?.cancel();
      setState(() {
        _focusSessionId = null;
        _focusSeconds = 25 * 60;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    final pages = [
      _buildHome(),
      _buildWorlds(),
      _buildMissions(),
      _buildFocus(),
      _buildStore(),
    ];

    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            const Text('TaskQuest'),
            if (_myProfession != null) ...[
              const SizedBox(width: 8),
              Text(
                _myProfession!['icon'] as String,
                style: const TextStyle(fontSize: 18),
              ),
            ],
          ],
        ),
        actions: [
          if (_myProfession == null)
            TextButton.icon(
              onPressed: () => Navigator.of(context).push(
                MaterialPageRoute(
                  builder: (_) => ProfessionSelectionScreen(token: widget.token),
                ),
              ).then((_) => _loadAll()),
              icon: const Icon(Icons.work_outline, size: 18),
              label: const Text('Profissão'),
            ),
          IconButton(tooltip: 'Atualizar', onPressed: _loadAll, icon: const Icon(Icons.refresh)),
          IconButton(tooltip: 'Sair', onPressed: _logout, icon: const Icon(Icons.logout)),
        ],
      ),
      body: _techSurface(
        _loading
            ? const Center(child: CircularProgressIndicator())
            : _error != null
                ? _buildError()
                : pages[_tabIndex],
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _tabIndex,
        onDestinationSelected: (index) => setState(() => _tabIndex = index),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home_outlined), label: 'Hoje'),
          NavigationDestination(icon: Icon(Icons.public), label: 'Mundos'),
          NavigationDestination(icon: Icon(Icons.flag_outlined), label: 'Missões'),
          NavigationDestination(icon: Icon(Icons.timer_outlined), label: 'Foco'),
          NavigationDestination(icon: Icon(Icons.storefront), label: 'Loja'),
        ],
      ),
    );
  }

  // ─── PAGES ────────────────────────────────────────────────────────────────

  Widget _buildHome() {
    final home = _home!;
    final xp = home['xp'] as Map<String, dynamic>;
    final streak = home['streak'] as Map<String, dynamic>? ?? {};
    final tasks = home['daily_tasks'] as List<dynamic>? ?? [];
    final currentXp = xp['current_level_xp'] as int? ?? 0;
    final nextXp = xp['next_level_xp'] as int? ?? 100;
    final progress = nextXp == 0 ? 0.0 : (currentXp / nextXp).clamp(0.0, 1.0);

    return RefreshIndicator(
      onRefresh: _loadAll,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Kiara card
          Container(
            padding: const EdgeInsets.all(18),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: AppColors.border),
              gradient: const LinearGradient(
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
                colors: [Color(0xFF12192C), Color(0xFF0E1526), Color(0xFF080B14)],
              ),
            ),
            child: Row(
              children: [
                const Expanded(flex: 11, child: AnimatedKiara(size: 210)),
                const SizedBox(width: 12),
                Expanded(
                  flex: 9,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'BEM-VINDA\nDE VOLTA!',
                        style: GoogleFonts.orbitron(
                          fontSize: 16,
                          fontWeight: FontWeight.w900,
                          color: AppColors.primary,
                          letterSpacing: 1,
                          height: 1.3,
                          shadows: [Shadow(color: AppColors.primary.withValues(alpha: 0.5), blurRadius: 10)],
                        ),
                      ),
                      const SizedBox(height: 10),
                      Container(
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: AppColors.surface.withValues(alpha: 0.72),
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(color: AppColors.border),
                        ),
                        child: Text(
                          home['motivation'] as String? ?? 'Um passo por vez.',
                          style: const TextStyle(height: 1.35, fontSize: 13),
                        ),
                      ),
                      const SizedBox(height: 10),
                      _statCard('Nível', '${xp['level'] ?? 1}', Icons.trending_up),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 12),
          // Stats row
          Row(
            children: [
              Expanded(child: _statCard('Sequência', '${streak['current_streak'] ?? 0} dias', Icons.local_fire_department)),
              const SizedBox(width: 8),
              Expanded(child: _statCard('Moedas', '${home['coins'] ?? 0} 🪙', Icons.monetization_on_outlined)),
            ],
          ),
          const SizedBox(height: 12),
          // XP bar
          Card(
            child: Padding(
              padding: const EdgeInsets.all(14),
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text('// XP', style: GoogleFonts.orbitron(fontSize: 11, fontWeight: FontWeight.w700, color: AppColors.primary, letterSpacing: 1.5)),
                      Text('$currentXp / $nextXp', style: GoogleFonts.shareTechMono(color: AppColors.textSecondary, fontSize: 12)),
                    ],
                  ),
                  const SizedBox(height: 10),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(999),
                    child: LinearProgressIndicator(
                      value: progress,
                      minHeight: 14,
                      backgroundColor: AppColors.background,
                      color: AppColors.primary,
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 20),
          // Daily tasks
          Row(
            children: [
              Expanded(
                child: Text(
                  '// TAREFAS DE HOJE',
                  style: GoogleFonts.orbitron(fontSize: 13, fontWeight: FontWeight.w700, color: AppColors.primary, letterSpacing: 1.5),
                ),
              ),
              TextButton.icon(
                onPressed: () => _runAction(() => _apiService.generateDailyTasks(widget.token)),
                icon: const Icon(Icons.auto_awesome),
                label: const Text('Gerar'),
              ),
            ],
          ),
          if (tasks.isEmpty)
            _emptyState('Nenhuma tarefa gerada.', 'Crie atividades em Mundos e toque em Gerar.')
          else
            ...tasks.map((task) => _taskTile(task as Map<String, dynamic>)),
        ],
      ),
    );
  }

  Widget _buildWorlds() {
    final personalWorlds = _worlds.where((w) => w['world_type'] == 'personal').toList();
    final professionalWorlds = _worlds.where((w) => w['world_type'] == 'professional').toList();
    final customWorlds = _worlds.where((w) => !['personal', 'professional'].contains(w['world_type'])).toList();

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        // Mundo Pessoal
        _worldSection(
          title: '🏠 Vida Pessoal',
          subtitle: 'Rotinas do dia a dia',
          color: const Color(0xFF22C55E),
          worlds: personalWorlds,
          onAddWorld: () => _createWorld(type: 'personal'),
          emptyLabel: 'Crie seu mundo pessoal',
          onAddSuggestions: personalWorlds.isEmpty
              ? null
              : () async {
                  final worldId = personalWorlds.first['id'] as int;
                  final result = await Navigator.of(context).push<bool>(
                    MaterialPageRoute(
                      builder: (_) => PersonalActivitiesScreen(
                        token: widget.token,
                        worldId: worldId,
                      ),
                    ),
                  );
                  if (result == true) _loadAll();
                },
        ),
        const SizedBox(height: 20),
        // Mundo Profissional
        _worldSection(
          title: '💼 Vida Profissional',
          subtitle: _myProfession != null
              ? '${_myProfession!['icon']} ${_myProfession!['name']}'
              : 'Selecione sua profissão',
          color: const Color(0xFF4F46E5),
          worlds: professionalWorlds,
          onAddWorld: _myProfession == null
              ? () => Navigator.of(context)
                  .push(MaterialPageRoute(
                    builder: (_) => ProfessionSelectionScreen(token: widget.token),
                  ))
                  .then((_) => _loadAll())
              : null,
          emptyLabel: _myProfession == null
              ? 'Toque em + para selecionar sua profissão'
              : 'Mundo profissional em criação...',
        ),
        // Outros mundos
        if (customWorlds.isNotEmpty) ...[
          const SizedBox(height: 20),
          _worldSection(
            title: '🌍 Outros Mundos',
            subtitle: 'Seus mundos personalizados',
            color: const Color(0xFF8B5CF6),
            worlds: customWorlds,
            onAddWorld: () => _createWorld(),
          ),
        ],
        const SizedBox(height: 16),
        OutlinedButton.icon(
          onPressed: () => _createWorld(),
          icon: const Icon(Icons.add),
          label: const Text('Criar mundo personalizado'),
        ),
      ],
    );
  }

  Widget _worldSection({
    required String title,
    required String subtitle,
    required Color color,
    required List<dynamic> worlds,
    VoidCallback? onAddWorld,
    VoidCallback? onAddSuggestions,
    String? emptyLabel,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Container(
              width: 4,
              height: 28,
              decoration: BoxDecoration(color: color, borderRadius: BorderRadius.circular(2)),
            ),
            const SizedBox(width: 10),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: GoogleFonts.orbitron(
                      fontSize: 13,
                      fontWeight: FontWeight.w800,
                      color: color,
                      letterSpacing: 0.5,
                      shadows: [Shadow(color: color.withValues(alpha: 0.5), blurRadius: 8)],
                    ),
                  ),
                  Text(subtitle, style: GoogleFonts.shareTechMono(fontSize: 11, color: color.withValues(alpha: 0.7))),
                ],
              ),
            ),
            if (onAddSuggestions != null)
              IconButton(
                tooltip: 'Sugestões de atividades',
                onPressed: onAddSuggestions,
                icon: Icon(Icons.auto_awesome, color: color),
              ),
            if (onAddWorld != null)
              IconButton(
                onPressed: onAddWorld,
                icon: Icon(Icons.add_circle_outline, color: color),
              ),
          ],
        ),
        const SizedBox(height: 10),
        if (worlds.isEmpty && emptyLabel != null)
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Row(
                children: [
                  Icon(Icons.info_outline, color: color.withValues(alpha: 0.7)),
                  const SizedBox(width: 12),
                  Expanded(child: Text(emptyLabel, style: const TextStyle(color: AppColors.textSecondary))),
                  if (onAddWorld != null)
                    TextButton(onPressed: onAddWorld, child: const Text('Criar')),
                ],
              ),
            ),
          )
        else
          for (final world in worlds) _worldCard(world, accentColor: color),
      ],
    );
  }

  Widget _worldCard(Map<String, dynamic> world, {Color accentColor = AppColors.primary}) {
    final worldId = world['id'] as int;
    final routines = _routines.where((r) => r['world_id'] == worldId).toList();

    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: Column(
        children: [
          ExpansionTile(
            leading: Text(world['icon'] as String? ?? '🌍', style: const TextStyle(fontSize: 24)),
            title: Text(world['name'] as String, style: const TextStyle(fontWeight: FontWeight.bold)),
            subtitle: Text('${routines.length} atividade${routines.length != 1 ? 's' : ''}'),
            trailing: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                IconButton(
                  tooltip: 'Adicionar atividade',
                  onPressed: () => _createRoutine(worldId),
                  icon: Icon(Icons.add_task, color: accentColor),
                ),
                const Icon(Icons.expand_more),
              ],
            ),
            children: [
              // Boss card dentro do mundo
              _BossCardWidget(token: widget.token, worldId: worldId, accentColor: accentColor),
              if (routines.isEmpty)
                Padding(
                  padding: const EdgeInsets.all(16),
                  child: Row(
                    children: [
                      const Icon(Icons.add_circle_outline, color: AppColors.textSecondary),
                      const SizedBox(width: 8),
                      const Expanded(child: Text('Adicione atividades para este mundo')),
                      TextButton(
                        onPressed: () => _createRoutine(worldId),
                        child: const Text('Adicionar'),
                      ),
                    ],
                  ),
                )
              else
                for (final routine in routines) _routineTile(routine as Map<String, dynamic>, accentColor),
            ],
          ),
        ],
      ),
    );
  }

  Widget _routineTile(Map<String, dynamic> routine, Color accentColor) {
    final routineId = routine['id'] as int;
    final timeLimitMinutes = routine['time_limit_minutes'] as int?;
    final isActive = routine['is_active'] as bool? ?? true;
    final activeSeconds = _activeTimers[routineId];
    final isTimerRunning = activeSeconds != null;

    String? timerLabel;
    if (isTimerRunning) {
      final m = (activeSeconds ~/ 60).toString().padLeft(2, '0');
      final s = (activeSeconds % 60).toString().padLeft(2, '0');
      timerLabel = '$m:$s';
    }

    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(10),
        border: Border.all(
          color: isTimerRunning ? accentColor.withValues(alpha: 0.6) : AppColors.border,
        ),
        color: isTimerRunning ? accentColor.withValues(alpha: 0.07) : null,
      ),
      child: ListTile(
        leading: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              ['', '😊', '💪', '🔥'][routine['difficulty'] as int? ?? 1],
              style: const TextStyle(fontSize: 20),
            ),
          ],
        ),
        title: Text(routine['title'] as String),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (routine['description'] != null)
              Text(routine['description'] as String, style: const TextStyle(fontSize: 12)),
            Row(
              children: [
                Text(
                  '+${routine['coin_reward'] ?? 10} 🪙  +${routine['xp_reward'] ?? 15} XP',
                  style: TextStyle(fontSize: 11, color: accentColor.withValues(alpha: 0.8)),
                ),
                if (timeLimitMinutes != null && !isTimerRunning)
                  Text(
                    '  ⏱ $timeLimitMinutes min',
                    style: const TextStyle(fontSize: 11, color: AppColors.textSecondary),
                  ),
                if (isTimerRunning)
                  Text(
                    '  ⏱ $timerLabel',
                    style: GoogleFonts.shareTechMono(fontSize: 13, color: accentColor, fontWeight: FontWeight.w700),
                  ),
              ],
            ),
          ],
        ),
        isThreeLine: true,
        trailing: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            if (timeLimitMinutes != null && !isTimerRunning && isActive)
              IconButton(
                tooltip: 'Iniciar timer',
                icon: Icon(Icons.play_circle_outline, color: accentColor),
                onPressed: () => _startTimer(routineId, timeLimitMinutes),
              ),
            if (isTimerRunning)
              IconButton(
                tooltip: 'Cancelar timer',
                icon: const Icon(Icons.stop_circle_outlined, color: Colors.red),
                onPressed: () {
                  _timerInstances[routineId]?.cancel();
                  _timerInstances.remove(routineId);
                  setState(() => _activeTimers.remove(routineId));
                },
              ),
            if (isActive)
              IconButton(
                tooltip: 'Concluir',
                icon: Icon(Icons.check_circle_outline, color: accentColor),
                onPressed: () => _completeRoutine(routineId),
              ),
            PopupMenuButton<String>(
              onSelected: (value) {
                if (value == 'toggle') {
                  _runAction(() => _apiService.toggleRoutine(widget.token, routineId));
                } else if (value == 'delete') {
                  _runAction(() => _apiService.deleteRoutine(widget.token, routineId));
                }
              },
              itemBuilder: (_) => [
                PopupMenuItem(
                  value: 'toggle',
                  child: Text(isActive ? 'Desativar' : 'Ativar'),
                ),
                const PopupMenuItem(value: 'delete', child: Text('Remover')),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMissions() {
    final daily = _missions['daily'] as List<dynamic>? ?? [];
    final weekly = _missions['weekly'] as List<dynamic>? ?? [];
    final achievements = _missions['achievements'] as List<dynamic>? ?? [];

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Row(
          children: [
            Expanded(
              child: Text(
                '// MISSÕES',
                style: GoogleFonts.orbitron(fontSize: 13, fontWeight: FontWeight.w700, color: AppColors.primary, letterSpacing: 1.5),
              ),
            ),
            IconButton(
              tooltip: 'Conquistas',
              onPressed: () => Navigator.of(context).push(
                MaterialPageRoute(builder: (_) => AchievementsScreen(token: widget.token)),
              ),
              icon: const Icon(Icons.emoji_events, color: Color(0xFFF59E0B)),
            ),
            TextButton.icon(
              onPressed: () => _runAction(() => _apiService.assignMissions(widget.token)),
              icon: const Icon(Icons.flag_outlined),
              label: const Text('Ativar'),
            ),
          ],
        ),
        _missionGroup('Diárias', daily, Icons.today, const Color(0xFF22C55E)),
        _missionGroup('Semanais', weekly, Icons.date_range, const Color(0xFF3B82F6)),
        _missionGroup('Conquistas', achievements, Icons.emoji_events, const Color(0xFFF59E0B)),
      ],
    );
  }

  Widget _buildFocus() {
    final tasks = (_home?['daily_tasks'] as List<dynamic>? ?? [])
        .where((task) => task['completed'] != true)
        .toList();
    final minutes = (_focusSeconds ~/ 60).toString().padLeft(2, '0');
    final seconds = (_focusSeconds % 60).toString().padLeft(2, '0');

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Text(
          '$minutes:$seconds',
          textAlign: TextAlign.center,
          style: GoogleFonts.orbitron(
            fontSize: 60,
            fontWeight: FontWeight.w900,
            color: AppColors.primary,
            shadows: [Shadow(color: AppColors.primary.withValues(alpha: 0.6), blurRadius: 20)],
          ),
        ),
        const Center(child: AnimatedKiara(size: 170, evolved: true)),
        const SizedBox(height: 12),
        if (_focusSessionId != null)
          FilledButton.icon(
            onPressed: _finishFocus,
            icon: const Icon(Icons.check),
            label: const Text('Concluir foco'),
          ),
        const SizedBox(height: 24),
        Text('// SELECIONE O ALVO', style: GoogleFonts.orbitron(fontSize: 11, fontWeight: FontWeight.w700, color: AppColors.primary, letterSpacing: 1.5)),
        const SizedBox(height: 12),
        if (tasks.isEmpty)
          _emptyState('Sem tarefas pendentes.', 'Gere tarefas ou conclua o dia.')
        else
          ...tasks.map((task) => Card(
                child: ListTile(
                  leading: const Icon(Icons.radio_button_unchecked),
                  title: Text(task['title'] as String),
                  subtitle: Text('${task['xp_reward'] ?? 0} XP'),
                  trailing: FilledButton(
                    onPressed: _focusSessionId == null ? () => _startFocus(task['id'] as int) : null,
                    child: const Text('Focar'),
                  ),
                ),
              )),
      ],
    );
  }

  Widget _buildStore() {
    final equipped = _skins.where((s) => s['equipped'] == true).toList();
    final unlocked = _skins.where((s) => s['unlocked'] == true && s['equipped'] != true).toList();
    final locked = _skins.where((s) => s['unlocked'] != true).toList();

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        // Kiara atual
        Card(
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              children: [
                Text('// KIARA', style: GoogleFonts.orbitron(fontSize: 12, fontWeight: FontWeight.w700, color: AppColors.primary, letterSpacing: 1.5)),
                const SizedBox(height: 12),
                const AnimatedKiara(size: 140, evolved: true),
                const SizedBox(height: 8),
                if (equipped.isNotEmpty)
                  Chip(
                    label: Text('✨ ${equipped.first['skin_name']}'),
                    backgroundColor: AppColors.primary.withValues(alpha: 0.2),
                  )
                else
                  const Text('Visual padrão', style: TextStyle(color: AppColors.textSecondary)),
              ],
            ),
          ),
        ),
        const SizedBox(height: 16),
        if (_skins.isEmpty)
          _emptyState('Loja vazia.', 'Rode o seed para adicionar skins.')
        else ...[
          if (unlocked.isNotEmpty) ...[
            const _SectionHeader(title: '✅ Desbloqueadas', subtitle: 'Prontas para equipar'),
            ...unlocked.map((skin) => _skinTile(skin as Map<String, dynamic>)),
            const SizedBox(height: 12),
          ],
          if (locked.isNotEmpty) ...[
            const _SectionHeader(title: '🔒 Na Loja', subtitle: 'Compre com suas moedas'),
            ...locked.map((skin) => _skinTile(skin as Map<String, dynamic>)),
          ],
        ],
      ],
    );
  }

  // ─── WIDGETS AUXILIARES ────────────────────────────────────────────────────

  Widget _skinTile(Map<String, dynamic> skin) {
    final unlocked = skin['unlocked'] as bool? ?? false;
    final equipped = skin['equipped'] as bool? ?? false;
    final price = skin['price'] as int? ?? 0;
    final coins = _home?['coins'] as int? ?? 0;
    final canBuy = coins >= price;

    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: AnimatedKiara(size: 54, compact: true, evolved: equipped),
        title: Text(skin['skin_name'] as String, style: const TextStyle(fontWeight: FontWeight.bold)),
        subtitle: equipped
            ? const Text('✅ Equipada agora', style: TextStyle(color: Colors.green))
            : unlocked
                ? const Text('Disponível para equipar')
                : Text(
                    '$price 🪙${canBuy ? '' : '  (saldo insuficiente)'}',
                    style: TextStyle(color: canBuy ? AppColors.textSecondary : Colors.red),
                  ),
        trailing: equipped
            ? const Icon(Icons.check_circle, color: Colors.green)
            : unlocked
                ? FilledButton(
                    onPressed: () => _runAction(() => _apiService.equipSkin(widget.token, skin['id'] as int)),
                    child: const Text('Equipar'),
                  )
                : OutlinedButton(
                    onPressed: canBuy
                        ? () => _runAction(() => _apiService.buySkin(widget.token, skin['id'] as int))
                        : null,
                    child: const Text('Comprar'),
                  ),
      ),
    );
  }

  Widget _taskTile(Map<String, dynamic> task) {
    final completed = task['completed'] as bool? ?? false;
    return Card(
      child: ListTile(
        title: Text(task['title'] as String),
        subtitle: Text('${task['xp_reward'] ?? 0} XP'),
        trailing: completed
            ? const Icon(Icons.check_circle, color: Colors.green)
            : IconButton(
                tooltip: 'Concluir',
                icon: const Icon(Icons.check_circle_outline),
                onPressed: () => _completeDailyTask(task['id'] as int),
              ),
      ),
    );
  }

  Widget _missionGroup(String title, List<dynamic> missions, IconData icon, Color color) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: ExpansionTile(
        leading: Icon(icon, color: color),
        initiallyExpanded: missions.isNotEmpty,
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
        subtitle: Text('${missions.length} missão(ões)'),
        children: missions.isEmpty
            ? [const ListTile(title: Text('Nenhuma missão ativa.'))]
            : missions.map((mission) {
                final percentage = (mission['percentage'] as int? ?? 0) / 100;
                return ListTile(
                  title: Text(mission['name'] as String),
                  subtitle: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(mission['description'] as String? ?? ''),
                      const SizedBox(height: 6),
                      ClipRRect(
                        borderRadius: BorderRadius.circular(999),
                        child: LinearProgressIndicator(
                          value: percentage.clamp(0.0, 1.0),
                          minHeight: 8,
                          color: color,
                          backgroundColor: color.withValues(alpha: 0.2),
                        ),
                      ),
                    ],
                  ),
                  trailing: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text('${mission['progress']}/${mission['goal']}',
                          style: const TextStyle(fontWeight: FontWeight.bold)),
                    ],
                  ),
                );
              }).toList(),
      ),
    );
  }

  Widget _statCard(String label, String value, IconData icon) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(12),
        color: AppColors.panel,
        border: Border.all(color: AppColors.border),
        boxShadow: [
          BoxShadow(
            color: AppColors.primary.withValues(alpha: 0.08),
            blurRadius: 12,
            spreadRadius: 0,
          ),
        ],
      ),
      child: Column(
        children: [
          Icon(icon, color: AppColors.primary, size: 20),
          const SizedBox(height: 6),
          Text(
            value,
            style: GoogleFonts.orbitron(
              fontWeight: FontWeight.w700,
              color: AppColors.textPrimary,
              fontSize: 13,
            ),
          ),
          const SizedBox(height: 2),
          Text(label, style: Theme.of(context).textTheme.labelSmall),
        ],
      ),
    );
  }

  Widget _emptyState(String title, String subtitle) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 4),
            Text(subtitle),
          ],
        ),
      ),
    );
  }

  Widget _buildError() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(_error!, textAlign: TextAlign.center),
            const SizedBox(height: 16),
            FilledButton.icon(
              onPressed: _loadAll,
              icon: const Icon(Icons.refresh),
              label: const Text('Tentar novamente'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _techSurface(Widget child) {
    return Container(
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [Color(0xFF070A12), Color(0xFF0A1320), Color(0xFF101827)],
        ),
      ),
      child: Stack(
        children: [
          Positioned.fill(child: CustomPaint(painter: _TechGridPainter())),
          child,
        ],
      ),
    );
  }
}

// ─── REWARD POPUP ─────────────────────────────────────────────────────────────

class _RewardPopup extends StatefulWidget {
  final int xp;
  final int coins;
  final bool levelUp;
  final Map<String, dynamic>? combo;

  const _RewardPopup({required this.xp, required this.coins, this.levelUp = false, this.combo});

  @override
  State<_RewardPopup> createState() => _RewardPopupState();
}

class _RewardPopupState extends State<_RewardPopup> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scale;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: const Duration(milliseconds: 400));
    _scale = CurvedAnimation(parent: _controller, curve: Curves.elasticOut);
    _controller.forward();

    Future.delayed(const Duration(seconds: 2), () {
      if (mounted) Navigator.of(context, rootNavigator: true).pop();
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      backgroundColor: Colors.transparent,
      child: ScaleTransition(
        scale: _scale,
        child: Container(
          padding: const EdgeInsets.all(28),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(20),
            gradient: const LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [Color(0xFF12192C), Color(0xFF0E1526)],
            ),
            border: Border.all(color: AppColors.primary.withValues(alpha: 0.5), width: 1.5),
            boxShadow: [
              BoxShadow(
                color: AppColors.primary.withValues(alpha: 0.3),
                blurRadius: 32,
                spreadRadius: 4,
              ),
            ],
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                widget.levelUp ? '🎉 Level Up!' : '✅ Concluído!',
                style: const TextStyle(fontSize: 24, fontWeight: FontWeight.w900, color: AppColors.textPrimary),
              ),
              const SizedBox(height: 16),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  _RewardBadge(label: '+${widget.xp} XP', emoji: '⚡', color: const Color(0xFF3B82F6)),
                  _RewardBadge(label: '+${widget.coins} moedas', emoji: '🪙', color: const Color(0xFFF59E0B)),
                ],
              ),
              if (widget.levelUp) ...[
                const SizedBox(height: 12),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  decoration: BoxDecoration(
                    color: AppColors.primary.withValues(alpha: 0.15),
                    borderRadius: BorderRadius.circular(999),
                    border: Border.all(color: AppColors.primary.withValues(alpha: 0.4)),
                  ),
                  child: const Text(
                    '🌟 Você subiu de nível! Continue assim!',
                    style: TextStyle(color: AppColors.primary, fontWeight: FontWeight.bold, fontSize: 13),
                  ),
                ),
              ],
              if (widget.combo != null && (widget.combo!['is_combo'] as bool? ?? false)) ...[
                const SizedBox(height: 12),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  decoration: BoxDecoration(
                    color: const Color(0xFFF59E0B).withValues(alpha: 0.15),
                    borderRadius: BorderRadius.circular(999),
                    border: Border.all(color: const Color(0xFFF59E0B).withValues(alpha: 0.5)),
                  ),
                  child: Text(
                    '${widget.combo!['label']}  x${widget.combo!['multiplier']}  (${widget.combo!['combo_count']} seguidas)',
                    style: const TextStyle(
                      color: Color(0xFFF59E0B),
                      fontWeight: FontWeight.bold,
                      fontSize: 13,
                    ),
                  ),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}

class _RewardBadge extends StatelessWidget {
  final String label;
  final String emoji;
  final Color color;

  const _RewardBadge({required this.label, required this.emoji, required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.15),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color.withValues(alpha: 0.4)),
      ),
      child: Column(
        children: [
          Text(emoji, style: const TextStyle(fontSize: 28)),
          const SizedBox(height: 4),
          Text(label, style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 15)),
        ],
      ),
    );
  }
}

class _SectionHeader extends StatelessWidget {
  final String title;
  final String subtitle;

  const _SectionHeader({required this.title, required this.subtitle});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(4, 8, 4, 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
          Text(subtitle, style: const TextStyle(fontSize: 12, color: AppColors.textSecondary)),
        ],
      ),
    );
  }
}

// ─── BOSS CARD ────────────────────────────────────────────────────────────────

class _BossCardWidget extends StatefulWidget {
  final String token;
  final int worldId;
  final Color accentColor;

  const _BossCardWidget({
    required this.token,
    required this.worldId,
    required this.accentColor,
  });

  @override
  State<_BossCardWidget> createState() => _BossCardWidgetState();
}

class _BossCardWidgetState extends State<_BossCardWidget> {
  Map<String, dynamic>? _boss;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final data = await ApiService().getWorldBoss(widget.token, widget.worldId);
      if (mounted) setState(() { _boss = data; _loading = false; });
    } catch (_) {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return const Padding(
        padding: EdgeInsets.all(12),
        child: LinearProgressIndicator(),
      );
    }
    if (_boss == null) return const SizedBox.shrink();

    final boss = _boss!['boss'] as Map<String, dynamic>;
    final hpPercent = (_boss!['hp_percent'] as num).toDouble();
    final tasksInStage = _boss!['tasks_in_stage'] as int;
    final requiredTasks = _boss!['required_tasks'] as int;
    final totalDefeated = _boss!['total_defeated'] as int;
    final stage = _boss!['stage'] as int;

    final hpColor = hpPercent > 0.6
        ? const Color(0xFF22C55E)
        : hpPercent > 0.3
            ? const Color(0xFFF59E0B)
            : const Color(0xFFEF4444);

    return Container(
      margin: const EdgeInsets.fromLTRB(12, 4, 12, 8),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: hpColor.withValues(alpha: 0.4)),
        color: hpColor.withValues(alpha: 0.05),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Text(boss['emoji'] as String, style: const TextStyle(fontSize: 28)),
              const SizedBox(width: 10),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Text(
                          boss['name'] as String,
                          style: const TextStyle(fontWeight: FontWeight.bold, color: AppColors.textPrimary),
                        ),
                        const SizedBox(width: 8),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                          decoration: BoxDecoration(
                            color: widget.accentColor.withValues(alpha: 0.2),
                            borderRadius: BorderRadius.circular(999),
                          ),
                          child: Text(
                            'Estágio $stage',
                            style: TextStyle(fontSize: 10, color: widget.accentColor, fontWeight: FontWeight.bold),
                          ),
                        ),
                      ],
                    ),
                    Text(
                      boss['description'] as String,
                      style: const TextStyle(fontSize: 12, color: AppColors.textSecondary),
                    ),
                  ],
                ),
              ),
              if (totalDefeated > 0)
                Column(
                  children: [
                    const Text('💀', style: TextStyle(fontSize: 16)),
                    Text('$totalDefeated', style: const TextStyle(fontSize: 10, color: AppColors.textSecondary)),
                  ],
                ),
            ],
          ),
          const SizedBox(height: 10),
          Row(
            children: [
              const Text('❤️', style: TextStyle(fontSize: 14)),
              const SizedBox(width: 6),
              Expanded(
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(999),
                  child: LinearProgressIndicator(
                    value: hpPercent,
                    minHeight: 10,
                    backgroundColor: const Color(0xFF1F2937),
                    color: hpColor,
                  ),
                ),
              ),
              const SizedBox(width: 8),
              Text(
                '$tasksInStage/$requiredTasks',
                style: TextStyle(fontSize: 11, color: hpColor, fontWeight: FontWeight.bold),
              ),
            ],
          ),
          const SizedBox(height: 6),
          Row(
            children: [
              Text('Recompensa: ', style: TextStyle(fontSize: 11, color: AppColors.textSecondary.withValues(alpha: 0.7))),
              Text('${boss['coin_reward']}🪙 ', style: const TextStyle(fontSize: 11, color: Color(0xFFF59E0B))),
              Text('+${boss['xp_reward']} XP', style: TextStyle(fontSize: 11, color: widget.accentColor)),
              if (boss['skin_reward'] != null) ...[
                const Text('  ', style: TextStyle(fontSize: 11)),
                Text('✨ ${boss['skin_reward']}', style: const TextStyle(fontSize: 11, color: Color(0xFF8B5CF6))),
              ],
            ],
          ),
        ],
      ),
    );
  }
}

// ─── BOSS DEFEAT POPUP ────────────────────────────────────────────────────────

class _BossDefeatPopup extends StatefulWidget {
  final Map<String, dynamic> defeat;
  const _BossDefeatPopup({required this.defeat});

  @override
  State<_BossDefeatPopup> createState() => _BossDefeatPopupState();
}

class _BossDefeatPopupState extends State<_BossDefeatPopup>
    with SingleTickerProviderStateMixin {
  late AnimationController _ctrl;
  late Animation<double> _scale;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(vsync: this, duration: const Duration(milliseconds: 500));
    _scale = CurvedAnimation(parent: _ctrl, curve: Curves.elasticOut);
    _ctrl.forward();
    Future.delayed(const Duration(seconds: 4), () {
      if (mounted) Navigator.of(context, rootNavigator: true).pop();
    });
  }

  @override
  void dispose() { _ctrl.dispose(); super.dispose(); }

  @override
  Widget build(BuildContext context) {
    final skinReward = widget.defeat['skin_reward'] as String?;
    return Dialog(
      backgroundColor: Colors.transparent,
      child: ScaleTransition(
        scale: _scale,
        child: Container(
          padding: const EdgeInsets.all(28),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(20),
            gradient: const LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [Color(0xFF1A0A00), Color(0xFF2D0F00)],
            ),
            border: Border.all(color: const Color(0xFFF59E0B).withValues(alpha: 0.7), width: 2),
            boxShadow: [
              BoxShadow(
                color: const Color(0xFFF59E0B).withValues(alpha: 0.4),
                blurRadius: 40,
                spreadRadius: 6,
              ),
            ],
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                widget.defeat['boss_emoji'] as String,
                style: const TextStyle(fontSize: 56),
              ),
              const SizedBox(height: 8),
              const Text(
                '⚔️ CHEFÃO DERROTADO!',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.w900,
                  color: Color(0xFFF59E0B),
                  letterSpacing: 1.2,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 4),
              Text(
                widget.defeat['boss_name'] as String,
                style: const TextStyle(color: AppColors.textSecondary, fontSize: 14),
              ),
              const SizedBox(height: 20),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  _RewardBadge(
                    label: '+${widget.defeat['coin_reward']}',
                    emoji: '🪙',
                    color: const Color(0xFFF59E0B),
                  ),
                  _RewardBadge(
                    label: '+${widget.defeat['xp_reward']} XP',
                    emoji: '⚡',
                    color: const Color(0xFF3B82F6),
                  ),
                ],
              ),
              if (skinReward != null) ...[
                const SizedBox(height: 16),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                  decoration: BoxDecoration(
                    color: const Color(0xFF8B5CF6).withValues(alpha: 0.2),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: const Color(0xFF8B5CF6).withValues(alpha: 0.5)),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Text('✨', style: TextStyle(fontSize: 20)),
                      const SizedBox(width: 8),
                      Text(
                        'Skin desbloqueada: $skinReward',
                        style: const TextStyle(
                          color: Color(0xFF8B5CF6),
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
              const SizedBox(height: 16),
              Text(
                'Próximo estágio: ${widget.defeat['next_stage']}',
                style: const TextStyle(fontSize: 12, color: AppColors.textSecondary),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _TechGridPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final gridPaint = Paint()
      ..color = AppColors.primary.withValues(alpha: 0.035)
      ..strokeWidth = 1;

    const spacing = 28.0;
    for (var x = 0.0; x < size.width; x += spacing) {
      canvas.drawLine(Offset(x, 0), Offset(x, size.height), gridPaint);
    }
    for (var y = 0.0; y < size.height; y += spacing) {
      canvas.drawLine(Offset(0, y), Offset(size.width, y), gridPaint);
    }

    final glow = Paint()
      ..shader = RadialGradient(
        colors: [AppColors.primary.withValues(alpha: 0.12), Colors.transparent],
      ).createShader(Rect.fromCircle(
        center: Offset(size.width * 0.85, size.height * 0.08),
        radius: size.width * 0.55,
      ));
    canvas.drawRect(Offset.zero & size, glow);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
