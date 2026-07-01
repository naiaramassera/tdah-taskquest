import 'dart:convert';

import 'package:http/http.dart' as http;

import '../../core/constants/api_constants.dart';

class ApiService {
  Map<String, String> _jsonHeaders(String token) => {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      };

  dynamic _decode(http.Response response) {
    if (response.body.isEmpty) return null;
    return jsonDecode(utf8.decode(response.bodyBytes));
  }

  void _ensureSuccess(http.Response response, String message) {
    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw Exception(message);
    }
  }

  Future<String> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('${ApiConstants.baseUrl}/auth/login'),
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: {'username': email, 'password': password},
    );

    _ensureSuccess(response, 'Erro ao entrar');
    final data = _decode(response) as Map<String, dynamic>;
    return data['access_token'] as String;
  }

  Future<void> register(String email, String password) async {
    final response = await http.post(
      Uri.parse('${ApiConstants.baseUrl}/auth/register'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );

    _ensureSuccess(response, 'Erro ao criar conta');
  }

  Future<Map<String, dynamic>> getHomeData(String token) async {
    final response = await http.get(
      Uri.parse('${ApiConstants.baseUrl}/home/'),
      headers: _jsonHeaders(token),
    );

    _ensureSuccess(response, 'Erro ao carregar dados da Home');
    return _decode(response) as Map<String, dynamic>;
  }

  Future<void> generateDailyTasks(String token) async {
    final response = await http.post(
      Uri.parse('${ApiConstants.baseUrl}/daily/generate'),
      headers: _jsonHeaders(token),
    );

    _ensureSuccess(response, 'Erro ao gerar tarefas de hoje');
  }

  Future<void> completeDailyTask(String token, int taskId) async {
    final response = await http.post(
      Uri.parse('${ApiConstants.baseUrl}/daily/complete/$taskId'),
      headers: _jsonHeaders(token),
    );

    _ensureSuccess(response, 'Erro ao completar tarefa');
  }

  Future<Map<String, dynamic>> completeDailyTaskWithResult(String token, int taskId) async {
    final response = await http.post(
      Uri.parse('${ApiConstants.baseUrl}/daily/complete/$taskId'),
      headers: _jsonHeaders(token),
    );

    _ensureSuccess(response, 'Erro ao completar tarefa');
    return (_decode(response) as Map<String, dynamic>?) ?? {};
  }

  Future<List<dynamic>> getWorlds(String token) async {
    final response = await http.get(
      Uri.parse('${ApiConstants.baseUrl}/worlds/'),
      headers: _jsonHeaders(token),
    );

    _ensureSuccess(response, 'Erro ao buscar mundos');
    return _decode(response) as List<dynamic>;
  }

  Future<void> createWorld(
    String token, {
    required String name,
    required String icon,
    required String color,
  }) async {
    final uri = Uri.parse('${ApiConstants.baseUrl}/worlds/').replace(
      queryParameters: {'name': name, 'icon': icon, 'color': color},
    );
    final response = await http.post(uri, headers: _jsonHeaders(token));

    _ensureSuccess(response, 'Erro ao criar mundo');
  }

  Future<List<dynamic>> getRoutines(String token) async {
    final response = await http.get(
      Uri.parse('${ApiConstants.baseUrl}/routines/'),
      headers: _jsonHeaders(token),
    );

    _ensureSuccess(response, 'Erro ao buscar rotinas');
    return _decode(response) as List<dynamic>;
  }

  Future<void> createRoutine(
    String token, {
    required int worldId,
    required String title,
    required int difficulty,
    int? timeLimitMinutes,
    String? description,
  }) async {
    final params = <String, String>{
      'title': title,
      'difficulty': difficulty.toString(),
    };
    if (timeLimitMinutes != null) params['time_limit_minutes'] = timeLimitMinutes.toString();
    if (description != null && description.isNotEmpty) params['description'] = description;

    final uri = Uri.parse('${ApiConstants.baseUrl}/routines/$worldId').replace(
      queryParameters: params,
    );
    final response = await http.post(uri, headers: _jsonHeaders(token));

    _ensureSuccess(response, 'Erro ao criar rotina');
  }

  Future<Map<String, dynamic>> completeRoutine(String token, int routineId) async {
    final response = await http.post(
      Uri.parse('${ApiConstants.baseUrl}/routines/$routineId/complete'),
      headers: _jsonHeaders(token),
    );

    _ensureSuccess(response, 'Erro ao completar rotina');
    return _decode(response) as Map<String, dynamic>;
  }

  Future<void> toggleRoutine(String token, int routineId) async {
    final response = await http.patch(
      Uri.parse('${ApiConstants.baseUrl}/routines/$routineId/toggle'),
      headers: _jsonHeaders(token),
    );

    _ensureSuccess(response, 'Erro ao alterar rotina');
  }

  Future<void> deleteRoutine(String token, int routineId) async {
    final response = await http.delete(
      Uri.parse('${ApiConstants.baseUrl}/routines/$routineId'),
      headers: _jsonHeaders(token),
    );

    _ensureSuccess(response, 'Erro ao remover rotina');
  }

  Future<Map<String, dynamic>> getMissions(String token) async {
    final response = await http.get(
      Uri.parse('${ApiConstants.baseUrl}/missions/'),
      headers: _jsonHeaders(token),
    );

    _ensureSuccess(response, 'Erro ao buscar missoes');
    return _decode(response) as Map<String, dynamic>;
  }

  Future<void> assignMissions(String token) async {
    final response = await http.post(
      Uri.parse('${ApiConstants.baseUrl}/missions/assign'),
      headers: _jsonHeaders(token),
    );

    _ensureSuccess(response, 'Erro ao ativar missoes');
  }

  Future<Map<String, dynamic>> startFocus(String token, int taskId) async {
    final response = await http.post(
      Uri.parse('${ApiConstants.baseUrl}/focus/start/$taskId'),
      headers: _jsonHeaders(token),
    );

    _ensureSuccess(response, 'Erro ao iniciar foco');
    return _decode(response) as Map<String, dynamic>;
  }

  Future<void> finishFocus(String token, int sessionId) async {
    final response = await http.post(
      Uri.parse('${ApiConstants.baseUrl}/focus/finish/$sessionId'),
      headers: _jsonHeaders(token),
    );

    _ensureSuccess(response, 'Erro ao concluir foco');
  }

  Future<List<dynamic>> getSkins(String token) async {
    final response = await http.get(
      Uri.parse('${ApiConstants.baseUrl}/skins/'),
      headers: _jsonHeaders(token),
    );

    _ensureSuccess(response, 'Erro ao buscar skins');
    return _decode(response) as List<dynamic>;
  }

  Future<List<dynamic>> getStoreSkins() async {
    final response = await http.get(
      Uri.parse('${ApiConstants.baseUrl}/store/skins'),
    );

    _ensureSuccess(response, 'Erro ao buscar loja');
    return _decode(response) as List<dynamic>;
  }

  Future<void> buySkin(String token, int skinId) async {
    final response = await http.post(
      Uri.parse('${ApiConstants.baseUrl}/skins/buy/$skinId'),
      headers: _jsonHeaders(token),
    );

    _ensureSuccess(response, 'Erro ao comprar skin');
  }

  Future<void> equipSkin(String token, int skinId) async {
    final response = await http.post(
      Uri.parse('${ApiConstants.baseUrl}/skins/equip/$skinId'),
      headers: _jsonHeaders(token),
    );

    _ensureSuccess(response, 'Erro ao equipar skin');
  }

  Future<List<dynamic>> getProfessions() async {
    final response = await http.get(
      Uri.parse('${ApiConstants.baseUrl}/professions/'),
    );

    _ensureSuccess(response, 'Erro ao buscar profissões');
    return _decode(response) as List<dynamic>;
  }

  Future<Map<String, dynamic>> selectProfession(String token, int professionId) async {
    final response = await http.post(
      Uri.parse('${ApiConstants.baseUrl}/professions/select/$professionId'),
      headers: _jsonHeaders(token),
    );

    _ensureSuccess(response, 'Erro ao selecionar profissão');
    return _decode(response) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> getMyProfession(String token) async {
    final response = await http.get(
      Uri.parse('${ApiConstants.baseUrl}/professions/me'),
      headers: _jsonHeaders(token),
    );

    _ensureSuccess(response, 'Erro ao buscar profissão');
    return _decode(response) as Map<String, dynamic>;
  }

  Future<List<dynamic>> getProfessionMissions(int professionId) async {
    final response = await http.get(
      Uri.parse('${ApiConstants.baseUrl}/professions/$professionId/missions'),
    );

    _ensureSuccess(response, 'Erro ao buscar missões da profissão');
    final data = _decode(response) as Map<String, dynamic>;
    return data['missions'] as List<dynamic>;
  }

  // ── Personal World ─────────────────────────────────────────────────────────

  Future<List<dynamic>> getPersonalCategories() async {
    final response = await http.get(
      Uri.parse('${ApiConstants.baseUrl}/personal/categories'),
    );
    _ensureSuccess(response, 'Erro ao buscar categorias');
    return _decode(response) as List<dynamic>;
  }

  Future<Map<String, dynamic>> getPersonalCategoryActivities(String categoryId) async {
    final response = await http.get(
      Uri.parse('${ApiConstants.baseUrl}/personal/categories/$categoryId'),
    );
    _ensureSuccess(response, 'Erro ao buscar atividades');
    return _decode(response) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> addPersonalActivities(
    String token, {
    required String categoryId,
    required List<int> activityIndices,
    int? worldId,
  }) async {
    final params = <String, String>{
      'category_id': categoryId,
      'activity_ids': activityIndices.join(','),
    };
    if (worldId != null) params['world_id'] = worldId.toString();

    final uri = Uri.parse('${ApiConstants.baseUrl}/personal/add-activities')
        .replace(queryParameters: params);
    final response = await http.post(uri, headers: _jsonHeaders(token));
    _ensureSuccess(response, 'Erro ao adicionar atividades');
    return _decode(response) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> setupPersonalWorld(String token) async {
    final response = await http.post(
      Uri.parse('${ApiConstants.baseUrl}/personal/setup'),
      headers: _jsonHeaders(token),
    );
    _ensureSuccess(response, 'Erro ao criar mundo pessoal');
    return _decode(response) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> getWorldBoss(String token, int worldId) async {
    final response = await http.get(
      Uri.parse('${ApiConstants.baseUrl}/worlds/$worldId/boss'),
      headers: _jsonHeaders(token),
    );
    _ensureSuccess(response, 'Erro ao buscar chefão');
    return _decode(response) as Map<String, dynamic>;
  }

  // ── Achievements ────────────────────────────────────────────────────────────

  Future<List<dynamic>> getAchievements(String token) async {
    final response = await http.get(
      Uri.parse('${ApiConstants.baseUrl}/achievements/me'),
      headers: _jsonHeaders(token),
    );
    _ensureSuccess(response, 'Erro ao buscar conquistas');
    return _decode(response) as List<dynamic>;
  }
}
