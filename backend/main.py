from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from routes import prompt_routes, auth_routes, analytics_routes

# Initialize app
app = FastAPI(
    title="PromptGenie API",
    version="1.0.0",
    description="AI-powered prompt generation and optimization API"
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


# Custom OpenAPI schema to support Bearer token auth in Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="PromptGenie API",
        version="1.0.0",
        description="AI-powered prompt generation API",
        routes=app.routes,
    )
    
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT Bearer token. Get it by logging in at /api/v1/auth/login"
        }
    }
    
    # Add security to all endpoints that require auth
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            if isinstance(operation, dict):
                # Add security to prompts and protected endpoints
                if "tags" in operation and ("Prompts" in operation["tags"] or "Analytics" in operation["tags"]):
                    if "generate" in str(operation) or "history" in str(operation):
                        operation["security"] = [{"bearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)