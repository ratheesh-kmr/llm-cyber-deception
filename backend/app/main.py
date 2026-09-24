import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.api.routes import sessions, events, risk, lures, interactions, dashboard, simulation
from app.gateway import gateway_app

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Active Cyber Deception Platform with LLM-Generated Lures Backend API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def api_root():
    return {
        "status": "online",
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "docs_url": "/docs",
        "gateway_url": f"http://127.0.0.1:{settings.DECEPTION_ENV_PORT}"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected", "llm_provider": settings.LLM_PROVIDER}

# Register API routes under /api
app.include_router(sessions.router, prefix="/api")
app.include_router(events.router, prefix="/api")
app.include_router(risk.router, prefix="/api")
app.include_router(lures.router, prefix="/api")
app.include_router(interactions.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(simulation.router, prefix="/api")

# Mount gateway portal application inside main app as well for convenience
app.mount("/gateway", gateway_app)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=settings.APP_DEBUG)
