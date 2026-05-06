import 'dart:convert';
import 'package:http/http.dart' as http;

class AuthService {
  static const String baseUrl = String.fromEnvironment('API_BASE_URL', defaultValue: 'http://10.0.2.2:8000');

  // ✅ REGISTER USER
  static Future<http.Response> registerUser({
    required String name,
    required String email,
    required String password,
  }) async {
    return await http.post(
      Uri.parse("$baseUrl/api/v1/auth/register"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "name": name,
        "email": email,
        "password": password,
      }),
    );
  }

  // ✅ LOGIN USER
  static Future<http.Response> loginUser(
      String email, String password) async {
    return await http.post(
      Uri.parse("$baseUrl/api/v1/auth/login"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "email": email,
        "password": password,
      }),
    );
  }
}