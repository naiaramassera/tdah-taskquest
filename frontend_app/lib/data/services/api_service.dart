import 'dart:convert';
import 'package:http/http.dart' as http;
import '../../core/constants/api_constants.dart';

class ApiService {

  /// 🔹 Buscar dados da Home (Dashboard)
  Future<Map<String, dynamic>> getHomeData(String token) async {

    final response = await http.get(
      Uri.parse('${ApiConstants.baseUrl}/home'),
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer $token",
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Erro ao carregar dados da Home");
    }
  }

  /// 🔹 Completar tarefa
  Future<void> completeTask(String token, int taskId) async {

    final response = await http.post(
      Uri.parse('${ApiConstants.baseUrl}/tasks/$taskId/complete'),
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer $token",
      },
    );

    if (response.statusCode != 200) {
      throw Exception("Erro ao completar tarefa");
    }
  }

  /// 🔹 Buscar skins desbloqueadas
  Future<List<dynamic>> getUnlockedSkins(String token) async {

    final response = await http.get(
      Uri.parse('${ApiConstants.baseUrl}/skins/unlocked'),
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer $token",
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Erro ao buscar skins");
    }
  }
}