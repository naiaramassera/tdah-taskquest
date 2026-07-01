class ApiConstants {
  // Para Web (localhost): http://127.0.0.1:8000
  // Para Android físico/iOS: use o IP da sua rede, ex: http://192.168.1.105:8000
  // Para emulador Android: http://10.0.2.2:8000
  static const String baseUrl = String.fromEnvironment(
    'API_URL',
    defaultValue: 'http://127.0.0.1:8000',
  );
}
