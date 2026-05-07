import 'dart:convert';
import 'dart:io' show Platform;
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../theme.dart';
import '../widgets/glass_card.dart';
import '../widgets/animated_gradient_button.dart';
import '../config.dart';
import 'home_screen.dart';

class AuthScreen extends StatefulWidget {
  const AuthScreen({Key? key}) : super(key: key);

  @override
  State<AuthScreen> createState() => _AuthScreenState();
}

class _AuthScreenState extends State<AuthScreen> {
  bool _isLogin = true;
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _nameController = TextEditingController();
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _checkLogin();
  }

  // ✅ Check if already logged in
  Future<void> _checkLogin() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('jwt_token');

    if (token != null && token.isNotEmpty) {
      if (!mounted) return;
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => const HomeScreen()),
      );
    }
  }

  // ✅ API URL
  String get apiUrl {
    return '${Config.baseUrl}/api/v1/auth';
  }

  // ✅ 🔥 Get Auth Headers (IMPORTANT)
  Future<Map<String, String>> _getAuthHeaders() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('jwt_token');

    return {
      "Content-Type": "application/json",
      "Authorization": "Bearer $token",
    };
  }

  // ✅ 🔥 Example Protected API Call
  Future<void> fetchPrompts() async {
    final headers = await _getAuthHeaders();

    final response = await http.get(
      Uri.parse("${Config.baseUrl}/api/v1/prompts"),
      headers: headers,
    );

    print("PROMPTS STATUS: ${response.statusCode}");
    print("PROMPTS BODY: ${response.body}");

    if (response.statusCode == 200) {
      _showSuccess("Fetched prompts successfully");
    } else {
      _showError("Unauthorized or failed to fetch prompts");
    }
  }

  // ✅ Submit (Login / Register)
  Future<void> _submit() async {
    setState(() => _isLoading = true);

    try {
      if (_isLogin) {
        // ================= LOGIN =================
        final response = await http.post(
          Uri.parse('$apiUrl/login'),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({
            'email': _emailController.text.trim(),
            'password': _passwordController.text,
          }),
        );

        final data = jsonDecode(response.body);

        print("STATUS: ${response.statusCode}");
        print("BODY: ${response.body}");

        if (response.statusCode == 200) {
          final prefs = await SharedPreferences.getInstance();
          await prefs.setString('jwt_token', data['access_token']);

          // 🔥 TEST protected API
          await fetchPrompts();

          if (!mounted) return;
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (_) => const HomeScreen()),
          );
        } else {
          _showError(data["detail"] ?? "Login failed");
        }
      } else {
        // ================= REGISTER =================
        final response = await http.post(
          Uri.parse('$apiUrl/register'),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({
            'name': _nameController.text.trim(),
            'email': _emailController.text.trim(),
            'password': _passwordController.text,
          }),
        );

        print("REGISTER STATUS: ${response.statusCode}");
        print("REGISTER BODY: ${response.body}");

        if (response.statusCode == 200) {
          _showSuccess("✅ Registration successful! Check your email to verify.");

          setState(() {
            _isLogin = true;
          });
        } else {
          final data = jsonDecode(response.body);
          _showError(data["detail"] ?? "Registration failed");
        }
      }
    } catch (e) {
      print("ERROR: $e");
      _showError('Could not connect to server.');
    }

    setState(() => _isLoading = false);
  }

  // ✅ Error UI
  void _showError(String msg) {
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(msg),
        backgroundColor: Colors.red,
      ),
    );
  }

  // ✅ Success UI
  void _showSuccess(String msg) {
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(msg),
        backgroundColor: Colors.green,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          Container(
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
                colors: [AppTheme.backgroundDark, AppTheme.backgroundMid],
              ),
            ),
          ),
          SafeArea(
            child: Center(
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(24.0),
                child: GlassCard(
                  padding: const EdgeInsets.all(24),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        _isLogin ? 'Welcome Back' : 'Create Account',
                        style: const TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                      ),
                      const SizedBox(height: 20),

                      if (!_isLogin)
                        TextField(
                          controller: _nameController,
                          style: const TextStyle(color: Colors.white),
                          decoration: const InputDecoration(labelText: 'Name'),
                        ),

                      const SizedBox(height: 10),

                      TextField(
                        controller: _emailController,
                        style: const TextStyle(color: Colors.white),
                        decoration: const InputDecoration(labelText: 'Email'),
                      ),

                      const SizedBox(height: 10),

                      TextField(
                        controller: _passwordController,
                        style: const TextStyle(color: Colors.white),
                        decoration: const InputDecoration(labelText: 'Password'),
                        obscureText: true,
                      ),

                      const SizedBox(height: 24),

                      _isLoading
                          ? const CircularProgressIndicator(
                              color: AppTheme.accentNeonBlue,
                            )
                          : AnimatedGradientButton(
                              text: _isLogin ? 'Login' : 'Sign Up',
                              onPressed: _submit,
                            ),

                      TextButton(
                        onPressed: () {
                          setState(() {
                            _isLogin = !_isLogin;
                          });
                        },
                        child: Text(
                          _isLogin
                              ? "Don't have an account? Sign up"
                              : 'Already have an account? Login',
                          style:
                              const TextStyle(color: AppTheme.textSecondary),
                        ),
                      )
                    ],
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}