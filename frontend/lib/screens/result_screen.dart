import 'dart:convert';
import 'dart:io' show Platform;
import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../theme.dart';
import '../widgets/glass_card.dart';
import '../config.dart';

class ResultScreen extends StatefulWidget {
  final String rawIdea;

  const ResultScreen({Key? key, required this.rawIdea}) : super(key: key);

  @override
  State<ResultScreen> createState() => _ResultScreenState();
}

class _ResultScreenState extends State<ResultScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;

  bool _isLoading = true;
  String _category = '';
  int _score = 0;
  Map<String, String> _prompts = {};
  String _errorMessage = '';
  String _historyId = '';
  bool _feedbackSubmitted = false;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
    _fetchPrompts();
  }

  String get apiUrl {
    return '${Config.baseUrl}/api/v1/prompts/generate';
  }

  String get feedbackUrl {
    return '${Config.baseUrl}/api/v1/analytics/feedback';
  }

  Future<void> _fetchPrompts() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('jwt_token') ?? '';
      
      final response = await http.post(
        Uri.parse(apiUrl),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
        body: jsonEncode({'raw_idea': widget.rawIdea}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (!mounted) return;
        setState(() {
          _historyId = data['id'] ?? '';
          _category = data['category'] ?? 'General';
          _score = data['score'] ?? 0;
          _prompts = {
            'Basic': data['prompts']['Basic'] ?? '',
            'Advanced': data['prompts']['Advanced'] ?? '',
            'Developer': data['prompts']['Developer'] ?? '',
          };
          _isLoading = false;
        });
      } else {
        if (!mounted) return;
        setState(() {
          _errorMessage = 'Failed to generate prompts. Error ${response.statusCode}';
          _isLoading = false;
        });
      }
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _errorMessage = 'Could not connect to server. Ensure backend is running.';
        _isLoading = false;
      });
    }
  }

  void _copyToClipboard(String text) {
    Clipboard.setData(ClipboardData(text: text));
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Copied to clipboard!'),
        backgroundColor: AppTheme.accentPurple,
      ),
    );
  }

  Future<void> _submitFeedback(bool isHelpful) async {
    if (_historyId.isEmpty || _feedbackSubmitted) return;
    
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('jwt_token') ?? '';
      
      await http.post(
        Uri.parse(feedbackUrl),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
        body: jsonEncode({
          'history_id': _historyId,
          'is_helpful': isHelpful,
        }),
      );
      
      setState(() => _feedbackSubmitted = true);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Thanks for the feedback!'), backgroundColor: Colors.green),
      );
    } catch (e) {
      // Ignore error for feedback
    }
  }

  void _exportToTxt() {
    final text = 'PromptGenie Export\n\n'
        'Raw Idea: ${widget.rawIdea}\n'
        'Category: $_category\n'
        'Score: $_score\n\n'
        '--- Basic Prompt ---\n${_prompts["Basic"]}\n\n'
        '--- Advanced Prompt ---\n${_prompts["Advanced"]}\n\n'
        '--- Developer Prompt ---\n${_prompts["Developer"]}';
        
    _copyToClipboard(text);
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Full export copied to clipboard!'), backgroundColor: AppTheme.accentNeonBlue),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: const Text('Generated Prompts'),
        actions: [
          IconButton(
            icon: const Icon(Icons.file_download, color: Colors.white),
            tooltip: 'Export All',
            onPressed: _exportToTxt,
          ),
        ],
      ),
      extendBodyBehindAppBar: true,
      body: Stack(
        children: [
          // Background Gradient
          Container(
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topRight,
                end: Alignment.bottomLeft,
                colors: [
                  AppTheme.backgroundMid,
                  AppTheme.backgroundDark,
                ],
              ),
            ),
          ),
          SafeArea(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator(color: AppTheme.accentNeonBlue))
                : _errorMessage.isNotEmpty
                    ? Center(child: Text(_errorMessage, style: const TextStyle(color: Colors.redAccent, fontSize: 16)))
                    : Padding(
                        padding: const EdgeInsets.all(20.0),
                        child: Column(
                          children: [
                            GlassCard(
                              padding: const EdgeInsets.all(16),
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                children: [
                                  Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Text(
                                        'Category Detected',
                                        style: TextStyle(color: AppTheme.textSecondary, fontSize: 12),
                                      ),
                                      const SizedBox(height: 4),
                                      Text(
                                        _category,
                                        style: const TextStyle(color: AppTheme.accentNeonBlue, fontWeight: FontWeight.bold),
                                      ),
                                    ],
                                  ),
                                  _buildScoreMeter(_score),
                                ],
                              ),
                            ),
                            const SizedBox(height: 20),
                            TabBar(
                              controller: _tabController,
                              indicatorColor: AppTheme.accentNeonBlue,
                              labelColor: AppTheme.accentNeonBlue,
                              unselectedLabelColor: AppTheme.textSecondary,
                              tabs: const [
                                Tab(text: 'Basic'),
                                Tab(text: 'Advanced'),
                                Tab(text: 'Developer'),
                              ],
                            ),
                            const SizedBox(height: 20),
                            Expanded(
                              child: TabBarView(
                                controller: _tabController,
                                children: [
                                  _buildPromptTab('Basic'),
                                  _buildPromptTab('Advanced'),
                                  _buildPromptTab('Developer'),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ),
          ),
        ],
      ),
    );
  }

  Widget _buildScoreMeter(int score) {
    return Stack(
      alignment: Alignment.center,
      children: [
        SizedBox(
          width: 50,
          height: 50,
          child: CircularProgressIndicator(
            value: score / 100,
            strokeWidth: 4,
            backgroundColor: Colors.white.withOpacity(0.1),
            valueColor: const AlwaysStoppedAnimation<Color>(AppTheme.accentPurple),
          ),
        ),
        Text(
          '$score',
          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
        ),
      ],
    );
  }

  Widget _buildPromptTab(String type) {
    final promptText = _prompts[type] ?? 'No prompt generated.';
    return SingleChildScrollView(
      child: GlassCard(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  '$type Prompt',
                  style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
                IconButton(
                  icon: const Icon(Icons.copy, color: AppTheme.textSecondary),
                  onPressed: () => _copyToClipboard(promptText),
                ),
              ],
            ),
            const Divider(color: Colors.white24),
            const SizedBox(height: 10),
            Text(
              promptText,
              style: const TextStyle(height: 1.5, fontSize: 16),
            ),
            const SizedBox(height: 20),
            _buildAnalyticsDummy(),
          ],
        ),
      ),
    );
  }

  Widget _buildAnalyticsDummy() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Prompt Analytics & Feedback',
          style: TextStyle(color: AppTheme.textSecondary, fontSize: 14),
        ),
        const SizedBox(height: 10),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            _statBadge('Clarity', 'High'),
            _statBadge('Specificity', '94%'),
            _statBadge('Est. Tokens', '~120'),
          ],
        ),
        const SizedBox(height: 16),
        if (!_feedbackSubmitted && _historyId.isNotEmpty)
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text('Was this helpful?', style: TextStyle(color: Colors.white70)),
              const SizedBox(width: 10),
              IconButton(
                icon: const Icon(Icons.thumb_up_alt_outlined, color: Colors.green),
                onPressed: () => _submitFeedback(true),
              ),
              IconButton(
                icon: const Icon(Icons.thumb_down_alt_outlined, color: Colors.red),
                onPressed: () => _submitFeedback(false),
              ),
            ],
          ),
      ],
    );
  }

  Widget _statBadge(String label, String value) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.05),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        children: [
          Text(label, style: const TextStyle(color: AppTheme.textSecondary, fontSize: 10)),
          const SizedBox(height: 4),
          Text(value, style: const TextStyle(color: AppTheme.accentNeonBlue, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }
}
