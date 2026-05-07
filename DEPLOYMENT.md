# PromptGenie Deployment Guide

## Project Status: ✅ READY FOR DEPLOYMENT

### What's Been Implemented

#### Backend (FastAPI + MongoDB)
- ✅ **JWT Authentication**: Secure token-based user authentication
- ✅ **Email Verification**: Users must verify email before login
- ✅ **Protected Routes**: Prompt generation and history require JWT token
- ✅ **Swagger OAuth**: Integrated Bearer token authentication in API docs
- ✅ **MongoDB Integration**: Full user & prompt storage
- ✅ **Email Service**: Verification emails via Gmail SMTP
- ✅ **Analytics**: Feedback submission and statistics

#### Frontend (Flutter Web)
- ✅ **Dynamic API Base URL**: Configurable endpoint via environment variable
- ✅ **Authentication Flow**: Register → Verify Email → Login → Generate Prompts
- ✅ **JWT Token Storage**: Secure local token management
- ✅ **Protected API Calls**: All prompts endpoints require authentication
- ✅ **Error Handling**: Clear messages for verification status

#### Deployment Configuration
- ✅ **render.yaml**: Multi-service deployment blueprint
- ✅ **Dockerfile**: Flutter web build containerization
- ✅ **Environment Variables**: All secrets properly managed

---

## Step 1: Push Code to GitHub

**If you haven't already:**

```bash
cd c:\Users\diyaa\.gemini\antigravity\scratch\PromptGenie

# Create a GitHub repository first at https://github.com/new

# Then update the remote URL and push:
git remote set-url origin https://github.com/YOUR_USERNAME/PromptGenie.git
git push -u origin main
```

**Current Commits:**
- Initial commit: Project setup
- Latest: JWT auth, email verification, Swagger OAuth support

---

## Step 2: Set Up MongoDB Atlas

1. **Go to**: https://www.mongodb.com/cloud/atlas
2. **Create Free Cluster**:
   - Organization name: Your name
   - Project name: PromptGenie
   - Deployment: M0 Free
   - Provider: AWS
   - Region: us-east-1 (or closest to you)

3. **Create Database User**:
   - Username: `promptgenie_user`
   - Password: Generate a strong password
   - Save this for later

4. **Get Connection String**:
   - Click "Databases" → "Connect" → "Drivers"
   - Copy connection string (looks like: `mongodb+srv://user:pass@cluster.mongodb.net/dbname`)
   - Replace `<password>` with the password you created

5. **Network Access**:
   - Add IP Address: `0.0.0.0/0` (allows all IPs for Render)

---

## Step 3: Set Up Gmail for Email Verification

1. **Enable 2-Step Verification**:
   - Go to: https://myaccount.google.com/security
   - Enable 2-Step Verification if not already done

2. **Create App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Copy the generated password (16 characters)

3. **Save These**:
   ```
   EMAIL_USER = your.email@gmail.com
   EMAIL_PASS = generated_app_password
   ```

---

## Step 4: Deploy on Render

### Create Backend Service

1. **Go to**: https://dashboard.render.com
2. **Click**: "New +" → "Web Service"
3. **Connect GitHub**: Select your PromptGenie repository
4. **Configure**:
   - **Name**: `promptgenie-backend`
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
   - **Plan**: Free (for testing)

5. **Add Environment Variables**:
   ```
   MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/promptgenie_db?retryWrites=true&w=majority
   SECRET_KEY=generate_a_strong_random_string (min 32 chars)
   EMAIL_USER=your.email@gmail.com
   EMAIL_PASS=your_app_password
   BASE_URL=https://promptgenie-backend.onrender.com (update after deployment)
   ```

6. **Click "Create Web Service"** and wait for deployment (~3-5 minutes)

7. **Note the Backend URL**: `https://promptgenie-backend-xxxxx.onrender.com`

### Create Frontend Service

1. **Go to**: https://dashboard.render.com
2. **Click**: "New +" → "Web Service"
3. **Connect GitHub**: Select your PromptGenie repository
4. **Configure**:
   - **Name**: `promptgenie-frontend`
   - **Root Directory**: `frontend`
   - **Runtime**: Docker
   - **Plan**: Free (for testing)

5. **Add Environment Variables**:
   ```
   API_BASE_URL=https://promptgenie-backend-xxxxx.onrender.com
   ```

6. **Click "Create Web Service"** and wait for deployment (~5-10 minutes)

---

## Step 5: Test the Deployment

### Backend API Testing

1. **Open**: `https://promptgenie-backend-xxxxx.onrender.com/docs`
   - This is the Swagger UI with OAuth support

2. **Test Health Check**:
   - Click on GET `/health`
   - Click "Try it out" → "Execute"
   - Should return: `{"status": "ok"}`

3. **Test Registration**:
   - Click on POST `/api/v1/auth/register`
   - Click "Try it out"
   - Enter test data:
     ```json
     {
       "email": "test@example.com",
       "password": "Test123!@",
       "name": "Test User"
     }
     ```
   - Should return 200 with user ID

4. **Check Email**:
   - You should receive a verification email
   - Click the link to verify (this updates the backend)

5. **Test Login**:
   - Click on POST `/api/v1/auth/login`
   - Enter your test email and password
   - Should return JWT token

6. **Test Protected Route**:
   - Copy the JWT token from login response
   - Click on "Authorize" button (top-right)
   - Paste token in format: `Bearer <token>`
   - Click on POST `/api/v1/prompts/generate`
   - Try it out with a test prompt
   - Should generate optimized prompts

### Frontend Testing

1. **Open**: `https://promptgenie-frontend-xxxxx.onrender.com`

2. **Test Registration**:
   - Click "Create Account"
   - Fill in name, email, password
   - Click "Sign Up"
   - Should show: "Check your email to verify"

3. **Verify Email**:
   - Check your email for verification link
   - Click the verification link (from the email)
   - Should show: "Email verified successfully!"

4. **Login**:
   - Go back to the frontend
   - Click "Sign In"
   - Enter your credentials
   - Should redirect to Home screen

5. **Generate Prompts**:
   - Enter a raw idea
   - Click "Generate"
   - Should show optimized prompts

---

## Step 6: Production Checklist

Before full deployment:

- [ ] Update `CORS` origins in `backend/main.py` (line 16) from `["*"]` to your frontend URL
- [ ] Generate a new strong `SECRET_KEY` (minimum 32 characters)
- [ ] Test all authentication flows
- [ ] Verify email delivery is working
- [ ] Monitor logs in Render dashboard
- [ ] Set up custom domain (optional)
- [ ] Enable HTTPS (automatic on Render)

---

## Step 7: Future Enhancements

Consider adding:

1. **Password Reset Flow**
2. **User Profile Management**
3. **Prompt Sharing & Public Library**
4. **Advanced Analytics Dashboard**
5. **Rate Limiting & Quotas**
6. **Google/GitHub OAuth Integration**

---

## Troubleshooting

### Backend won't start
- Check logs in Render: Dashboard → Service → Logs
- Verify all environment variables are set
- Ensure MONGO_URI is correct

### Email not sending
- Check Gmail app password format
- Verify "Less secure apps" setting
- Check Render logs for SMTP errors

### Frontend can't reach backend
- Verify API_BASE_URL environment variable
- Check CORS settings in backend main.py
- Test API directly: curl https://promptgenie-backend-xxxxx.onrender.com/health

### Slow deployment
- Render free tier has limited resources
- Flutter build can take 5-10 minutes
- Be patient on first deployment

---

## Support Commands

```bash
# Check git status
git status

# View recent commits
git log --oneline -5

# View environment variables (backend)
cat backend/.env

# Test backend locally (requires venv)
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn main:app --reload
```

---

**Deployed Services URLs** (Update these after deployment):

- 🔵 Backend API: `https://promptgenie-backend-xxxxx.onrender.com`
- 🟢 Frontend App: `https://promptgenie-frontend-xxxxx.onrender.com`
- 📊 API Docs: `https://promptgenie-backend-xxxxx.onrender.com/docs`

---

**Date Prepared**: May 7, 2026
**Status**: ✅ Ready for Production Deployment
