from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import prompt_routes, auth_routes, analytics_routes

app = FastAPI(title="PromptGenie API", version="1.0.0")

# CORS middleware for Flutter frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(prompt_routes.router, prefix="/api/v1/prompts", tags=["Prompts"])
app.include_router(analytics_routes.router, prefix="/api/v1/analytics", tags=["Analytics"])

@app.get("/")
def read_root():
    return {"message": "Welcome to PromptGenie API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

