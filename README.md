# PromptGenie

A full-stack application for generating and managing AI prompts.

## Project Structure

- `backend/`: FastAPI backend with MongoDB
- `frontend/`: Flutter web app

## Deployment on Render

### Backend Deployment

1. Create a new Web Service on Render.
2. Connect your GitHub repository.
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
5. Set environment variables:
   - `MONGO_URI`: Your MongoDB connection string (e.g., from MongoDB Atlas)
   - `SECRET_KEY`: A random secret key for JWT
   - `EMAIL_USER`: Your Gmail address for sending emails
   - `EMAIL_PASS`: Your Gmail app password
   - `BASE_URL`: The URL of your deployed backend (e.g., https://your-backend.onrender.com)

### Frontend Deployment

1. Build the Flutter web app locally:
   ```
   cd frontend
   flutter build web --release --dart-define=API_BASE_URL=https://your-backend.onrender.com
   ```
2. Create a new Static Site on Render.
3. Upload the `build/web` folder or connect repo and set publish directory to `frontend/build/web`.
4. Deploy.

## Local Development

### Backend

1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables in `.env` file.
3. Run: `python main.py`

### Frontend

1. Install Flutter.
2. Run: `flutter run` (for mobile) or `flutter run -d web` (for web).

## Notes

- Ensure MongoDB is accessible.
- For email, use Gmail app password.
- Update API_BASE_URL for production.