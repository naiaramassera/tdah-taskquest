import 'package:flutter/material.dart';
import '../../data/services/api_service.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {

  final ApiService _apiService = ApiService();

  Map<String, dynamic>? homeData;
  bool isLoading = true;

  // ⚠️ Coloque seu token real aqui por enquanto
  String token = "SEU_TOKEN_AQUI";

  @override
  void initState() {
    super.initState();
    loadHome();
  }

  Future<void> loadHome() async {
    try {
      final data = await _apiService.getHomeData(token);

      setState(() {
        homeData = data;
        isLoading = false;
      });

    } catch (e) {
      print(e);
      setState(() {
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {

    if (isLoading) {
      return const Scaffold(
        body: Center(
          child: CircularProgressIndicator(),
        ),
      );
    }

    if (homeData == null) {
      return const Scaffold(
        body: Center(
          child: Text("Erro ao carregar dados"),
        ),
      );
    }

    int level = homeData!["xp"]["level"];
    int currentXp = homeData!["xp"]["current_level_xp"];
    int nextLevelXp = homeData!["xp"]["next_level_xp"];
    int streak = homeData!["streak"]["current_streak"];
    List tasks = homeData!["tasks"];

    double progress = currentXp / nextLevelXp;

    return Scaffold(
      backgroundColor: const Color(0xFFFFF6EC),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [

              /// 🔥 Topo (Level + Streak)
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    "Nível $level",
                    style: const TextStyle(
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Row(
                    children: [
                      const Icon(Icons.local_fire_department, color: Colors.orange),
                      const SizedBox(width: 4),
                      Text(
                        "$streak dias",
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      )
                    ],
                  )
                ],
              ),

              const SizedBox(height: 16),

              /// 🔥 Barra de XP
              ClipRRect(
                borderRadius: BorderRadius.circular(12),
                child: LinearProgressIndicator(
                  value: progress,
                  minHeight: 12,
                  backgroundColor: Colors.grey.shade300,
                  color: const Color(0xFFFF8C42),
                ),
              ),

              const SizedBox(height: 30),

              /// 🐶 Kiara
              Center(
                child: Column(
                  children: [
                    Image.asset(
                      "assets/images/kiara_base.png",
                      height: 120,
                    ),
                    const SizedBox(height: 8),
                    const Text(
                      "Kiara está orgulhosa de você 💛",
                      style: TextStyle(fontSize: 16),
                    )
                  ],
                ),
              ),

              const SizedBox(height: 30),

              const Text(
                "Tarefas de Hoje",
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),

              const SizedBox(height: 12),

              /// 📋 Lista de tarefas
              Expanded(
                child: ListView.builder(
                  itemCount: tasks.length,
                  itemBuilder: (context, index) {

                    final task = tasks[index];

                    return Card(
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: ListTile(
                        title: Text(task["title"]),
                        trailing: task["completed"]
                            ? const Icon(Icons.check_circle, color: Colors.green)
                            : IconButton(
                                icon: const Icon(Icons.radio_button_unchecked),
                                onPressed: () async {
                                  await _apiService.completeTask(token, task["id"]);
                                  loadHome();
                                },
                              ),
                      ),
                    );
                  },
                ),
              )
            ],
          ),
        ),
      ),
    );
  }
}