# PromptGenie 🚀

**AI-powered prompt generation and optimization platform**

Generate, optimize, and manage intelligent prompts for any AI task using advanced NLP and machine learning.

[![Status](https://img.shields.io/badge/Status-Ready%20for%20Deployment-green)]()
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)]()
[![Flutter](https://img.shields.io/badge/Flutter-3.7%2B-blue)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

---

## ✨ Features

### 🔐 Authentication & Security
- **Email Verification**: Users must verify email before access
- **JWT Authentication**: Secure token-based authentication (7-day expiration)
- **Password Hashing**: bcrypt-based password security
- **Protected Routes**: All core features require authentication

### 🧠 Prompt Generation
- **AI-Powered Optimization**: Leverages Google Gemini API for prompt enhancement
- **Category Classification**: Automatic categorization of prompts
- **Quality Scoring**: Built-in prompt quality assessment
- **History Management**: Full prompt generation history per user

### 📊 Analytics
- **Feedback Tracking**: User feedback on generated prompts
- **Usage Statistics**: Aggregated analytics on prompt generation
- **Category Analytics**: Track popular prompt categories
- **User Metrics**: Monitor platform-wide usage

### 🎨 User Interface
- **Flutter Web**: Beautiful, responsive web interface
- **Glass Morphism Design**: Modern UI with gradient backgrounds
- **Real-time Feedback**: Instant prompt generation results
- **Mobile-Friendly**: Works on all devices

---

## 🏗️ Project Structure

```
PromptGenie/
├── backend/                      # FastAPI Backend
│   ├── main.py                   # FastAPI app with Swagger
│   ├── requirements.txt          # Python dependencies
│   ├── database/
│   │   └── db.py                # MongoDB connection
│   ├── routes/
│   │   ├── auth_routes.py        # Authentication endpoints
│   │   ├── prompt_routes.py      # Prompt generation (JWT protected)
│   │   └── analytics_routes.py   # Analytics endpoints
│   ├── services/
│   │   ├── auth_service.py       # JWT & password hashing
│   │   ├── email_service.py      # Email verification
│   │   └── prompt_service.py     # Prompt optimization
│   ├── models/
│   │   ├── user_schemas.py       # User data models
│   │   └── schemas.py            # Prompt models
│   └── ml/
│       ├── classifier.py         # Category classification
│       └── train_model.py        # Model training
│
├── frontend/                     # Flutter Web App
│   ├── lib/
│   │   ├── main.dart             # App entry point
│   │   ├── config.dart           # API configuration
│   │   ├── screens/
│   │   │   ├── auth_screen.dart   # Login/Register
│   │   │   ├── home_screen.dart   # Main app
│   │   │   ├── result_screen.dart # Prompt results
│   │   │   └── history_screen.dart# User history
│   │   ├── widgets/
│   │   └── theme.dart            # UI themes
│   ├── pubspec.yaml              # Flutter dependencies
│   └── Dockerfile                # Docker build config
│
├── render.yaml                   # Render deployment blueprint
├── DEPLOYMENT.md                 # Detailed deployment guide
└── README.md                     # This file
```

---

## 🚀 Quick Start

### Local Development

#### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your settings
echo MONGO_URI=your_mongodb_uri > .env
echo SECRET_KEY=your_32_char_secret_key >> .env
echo EMAIL_USER=your@gmail.com >> .env
echo EMAIL_PASS=your_gmail_app_password >> .env
echo BASE_URL=http://localhost:8000 >> .env
echo GEMINI_API_KEY=your_gemini_key >> .env

# Run development server
python main.py

# API docs available at: http://localhost:8000/docs
```

#### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Get dependencies
flutter pub get

# Run web app
flutter run -d web

# Build for production
flutter build web --release --dart-define=API_BASE_URL=https://your-backend-url.onrender.com
```

---

## 📋 Prerequisites

### Backend Requirements
- Python 3.11+
- MongoDB Atlas account (free tier available)
- Gmail account with app password
- Google Gemini API key
- Render account (for deployment)

### Frontend Requirements
- Flutter 3.7+
- Modern web browser (Chrome, Firefox, Safari, Edge)

---

## 🔑 Environment Variables

### Backend (.env)
```env
# MongoDB
MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/dbname

# Security
SECRET_KEY=your-32-character-minimum-secret-key

# Email Service
EMAIL_USER=your.email@gmail.com
EMAIL_PASS=your-gmail-app-password

# API Configuration
BASE_URL=https://your-backend-url.onrender.com

# AI API
GEMINI_API_KEY=your-google-gemini-api-key
```

### Frontend (build-time)
```dart
API_BASE_URL=https://your-backend-url.onrender.com
```

---

## 🚢 Deployment

### Automatic Deployment on Render

The `render.yaml` file enables one-click deployment:

1. **Push code to GitHub**
2. **Connect GitHub to Render**
3. **Select this repository**
4. **Render automatically detects render.yaml**
5. **Deploy both services simultaneously**

**[See DEPLOYMENT.md for detailed steps →](./DEPLOYMENT.md)**

### Manual Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for:
- Step-by-step MongoDB setup
- Gmail app password configuration
- Individual service deployment
- Testing & troubleshooting
- Production checklist

---

## 📚 API Documentation

### Authentication Endpoints

**POST `/api/v1/auth/register`**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}
```
Response: User object + verification email sent

**GET `/api/v1/auth/verify-email?token=...`**
Verifies user email and enables login

**POST `/api/v1/auth/login`**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```
Response: JWT access token

### Protected Endpoints (Require JWT Token)

**POST `/api/v1/prompts/generate`** ⚠️ JWT Required
```json
{
  "raw_idea": "Create a prompt for ChatGPT about machine learning"
}
```

**GET `/api/v1/prompts/history`** ⚠️ JWT Required
Returns user's prompt generation history

### Public Endpoints

**GET `/health`**
Health check for deployment monitoring

**GET `/docs`**
Interactive Swagger UI with OAuth support

---

## 🧪 Testing the API

### Using Swagger UI

1. Visit: `https://your-backend-url/docs`
2. Click "Authorize" button
3. Login to get JWT token
4. Token is automatically used for protected endpoints

### Using cURL

```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123!","name":"Test"}'

# Verify email (check email for token)
curl http://localhost:8000/api/v1/auth/verify-email?token=YOUR_TOKEN

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123!"}'

# Generate prompt (with JWT token from login)
curl -X POST http://localhost:8000/api/v1/prompts/generate \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"raw_idea":"Create a prompt for image generation"}'
```

---

## 🔒 Security Features

- ✅ JWT-based authentication (7-day expiration)
- ✅ Password hashing with bcrypt
- ✅ Email verification requirement
- ✅ HTTPS enforcement on Render
- ✅ CORS protection with configurable origins
- ✅ Environment variable secrets management
- ✅ MongoDB unique index on email
- ✅ User-scoped prompt history

---

## 📈 Performance & Scaling

- **Optimized API**: Fast response times with async operations
- **Database Indexing**: Email and user_id indexes for quick lookups
- **Connection Pooling**: MongoDB connection pooling enabled
- **Caching**: Client-side token caching in Flutter
- **Containerization**: Docker support for easy scaling

---

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **PyJWT**: JWT token management
- **MongoDB**: NoSQL database
- **Bcrypt**: Password hashing
- **Python-dotenv**: Environment configuration
- **Uvicorn**: ASGI server
- **Gunicorn**: Production server

### Frontend
- **Flutter**: Cross-platform UI framework
- **Dart**: Programming language
- **HTTP Package**: API communication
- **SharedPreferences**: Local token storage

### DevOps
- **Render**: Cloud deployment platform
- **Docker**: Containerization
- **GitHub**: Version control
- **MongoDB Atlas**: Cloud database

---

## 📝 API Response Examples

### Successful Prompt Generation
```json
{
  "id": "507f1f77bcf86cd799439011",
  "category": "image-generation",
  "score": 8.5,
  "prompts": [
    "Create a detailed, high-quality digital artwork of...",
    "Design an intricate illustration featuring...",
    "Generate a stunning visual representation of..."
  ]
}
```

### Error Response
```json
{
  "detail": "Please verify your email first"
}
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| "MONGO_URI is not set" | Add MONGO_URI to .env file |
| Email not sending | Enable Gmail 2-step verification + create app password |
| "Could not validate credentials" | Token expired or invalid, login again |
| CORS error | Update CORS origins in main.py |
| Slow deployment | Render free tier is slower; upgrade plan for production |

---

## 📞 Support & Contact

For issues or questions:
1. Check [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed guides
2. Review API docs at `/docs` endpoint
3. Check Render logs for backend errors
4. Verify all environment variables are set

---

## 📄 License

MIT License - Feel free to use this project for personal or commercial purposes.

---

## 🎯 Roadmap

- [ ] Advanced prompt templates
- [ ] Prompt sharing & collaboration
- [ ] User analytics dashboard
- [ ] Social OAuth (Google, GitHub)
- [ ] Rate limiting & usage quotas
- [ ] Prompt versioning & history
- [ ] Admin dashboard
- [ ] API webhook integration

---

**Built with ❤️ | Last Updated: May 7, 2026**

- Ensure MongoDB is accessible.
- For email, use Gmail app password.
- Update API_BASE_URL for production.