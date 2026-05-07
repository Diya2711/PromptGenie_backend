from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import prompt_routes, auth_routes, analytics_routes

# Initialize app
app = FastAPI(
    title="PromptGenie API",
    version="1.0.0"
)

# CORS middleware for Flutter frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change later for production security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(prompt_routes.router, prefix="/api/v1/prompts", tags=["Prompts"])
app.include_router(analytics_routes.router, prefix="/api/v1/analytics", tags=["Analytics"])


# Root route
@app.get("/")
def read_root():
    return {"message": "🚀 PromptGenie API is running successfully!"}


# Health check (VERY IMPORTANT for Render)
@app.get("/health")
def health_check():
    return {"status": "ok"}