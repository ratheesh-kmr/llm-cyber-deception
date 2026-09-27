import os
from fastapi import FastAPI, Request, Response, Depends, Header
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db, init_db, SessionLocal
from app.services.session_service import get_or_create_session
from app.services.event_service import log_event
from app.services.lure.interaction_tracker import record_interaction
from app.models.database import Lure

gateway_app = FastAPI(
    title=f"{settings.FAKE_COMPANY_NAME} Portal",
    description="Synthetic Deception Environment Gateway",
    docs_url=None, redoc_url=None
)

gateway_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_base_prefix(request: Request) -> str:
    path = request.url.path
    return "/gateway" if path.startswith("/gateway") else ""

def normalize_path(path: str) -> str:
    if path.startswith("/gateway"):
        sub = path[len("/gateway"):]
        return sub if sub.startswith("/") else f"/{sub}"
    return path

def get_session_and_log(request: Request, db: Session):
    session_id = request.headers.get("X-Session-ID") or request.cookies.get("deception_session")
    client_ip = request.client.host if request.client else "127.0.0.1"
    user_agent = request.headers.get("User-Agent", "Unknown")

    attacker = get_or_create_session(db, source_ip=client_ip, user_agent=user_agent, session_id=session_id)

    # Log event
    log_event(
        db,
        session_id=attacker.session_id,
        endpoint=request.url.path,
        method=request.method,
        source_ip=client_ip,
        user_agent=user_agent,
        metadata={"headers": dict(request.headers), "query_params": dict(request.query_params)}
    )

    return attacker

@gateway_app.api_route("/", methods=["GET", "HEAD"], response_class=HTMLResponse)
def gateway_home(request: Request, db: Session = Depends(get_db)):
    attacker = get_session_and_log(request, db)
    base = get_base_prefix(request)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{settings.FAKE_COMPANY_NAME} - Enterprise Portal</title>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 0; background: #f4f6f9; color: #333; }}
            header {{ background: #0f172a; color: white; padding: 20px 40px; display: flex; justify-content: space-between; align-items: center; }}
            header h1 {{ margin: 0; font-size: 24px; font-weight: 600; color: #38bdf8; }}
            nav a {{ color: #94a3b8; text-decoration: none; margin-left: 20px; font-size: 14px; transition: color 0.2s; }}
            nav a:hover {{ color: white; }}
            .container {{ max-width: 1000px; margin: 40px auto; padding: 0 20px; }}
            .hero {{ background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
            .hero h2 {{ margin-top: 0; color: #0f172a; }}
            .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 30px; }}
            .card {{ background: white; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; }}
            .card h3 {{ margin-top: 0; font-size: 16px; color: #1e293b; }}
            footer {{ text-align: center; margin-top: 60px; padding: 20px; color: #64748b; font-size: 13px; }}
        </style>
    </head>
    <body>
        <header>
            <h1>{settings.FAKE_COMPANY_NAME}</h1>
            <nav>
                <a href="{base}/">Home</a>
                <a href="{base}/login">Employee Login</a>
                <a href="{base}/admin">Internal Admin</a>
                <a href="{base}/documents">Documents</a>
            </nav>
        </header>
        <div class="container">
            <div class="hero">
                <h2>Welcome to {settings.FAKE_COMPANY_NAME}</h2>
                <p>Leading enterprise cloud infrastructure and cybersecurity intelligence solutions.</p>
            </div>
            <div class="grid">
                <div class="card">
                    <h3>Internal Portal</h3>
                    <p>Access employee services and system documentation.</p>
                    <a href="{base}/login" style="color:#0284c7; text-decoration: none; font-weight: bold;">Sign In &rarr;</a>
                </div>
                <div class="card">
                    <h3>System Status</h3>
                    <p>All core infrastructure services operating normally.</p>
                </div>
                <div class="card">
                    <h3>Security Policy</h3>
                    <p>Internal network access is strictly monitored and all interactions logged.</p>
                </div>
            </div>
        </div>
        <footer>
            &copy; 2026 {settings.FAKE_COMPANY_NAME}. All rights reserved. [Session: {attacker.session_id[:8]}...]
        </footer>
    </body>
    </html>
    """
    response = HTMLResponse(content=html)
    response.set_cookie(key="deception_session", value=attacker.session_id)
    return response

@gateway_app.api_route("/login", methods=["GET", "HEAD"], response_class=HTMLResponse)
@gateway_app.api_route("/admin", methods=["GET", "HEAD"], response_class=HTMLResponse)
@gateway_app.api_route("/config", methods=["GET", "HEAD"], response_class=HTMLResponse)
@gateway_app.api_route("/backup", methods=["GET", "HEAD"], response_class=HTMLResponse)
@gateway_app.api_route("/documents", methods=["GET", "HEAD"], response_class=HTMLResponse)
def gateway_pages(request: Request, db: Session = Depends(get_db)):
    attacker = get_session_and_log(request, db)
    path = request.url.path
    norm_path = normalize_path(path)
    base = get_base_prefix(request)

    # Check if this endpoint matches a deployed lure!
    lure = db.query(Lure).filter(
        (Lure.endpoint_path == path) | (Lure.endpoint_path == norm_path),
        Lure.status == "deployed"
    ).first()
    if lure:
        record_interaction(db, lure_id=lure.lure_id, session_id=attacker.session_id, interaction_type="VIEW")
        return PlainTextResponse(content=lure.content)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{settings.FAKE_COMPANY_NAME} - {path}</title>
        <style>
            body {{ font-family: sans-serif; background: #0f172a; color: #f8fafc; padding: 50px; text-align: center; }}
            .box {{ background: #1e293b; padding: 40px; border-radius: 8px; max-width: 450px; margin: 0 auto; border: 1px solid #334155; }}
            input {{ width: 90%; padding: 10px; margin: 10px 0; background: #0f172a; border: 1px solid #475569; color: white; border-radius: 4px; box-sizing: border-box; }}
            button {{ width: 90%; padding: 12px; background: #0284c7; color: white; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; }}
            a {{ color: #38bdf8; font-size: 13px; text-decoration: none; display: inline-block; margin-top: 15px; }}
        </style>
    </head>
    <body>
        <div class="box">
            <h2>{settings.FAKE_COMPANY_NAME} Access Panel</h2>
            <p style="color: #94a3b8;">Restricted Area: {path}</p>
            <form action="{base}/login" method="POST">
                <input type="text" name="username" placeholder="Username" required /><br/>
                <input type="password" name="password" placeholder="Password" required /><br/>
                <button type="submit">Authenticate</button>
            </form>
            <br/>
            <a href="{base}/">&larr; Return to Meridian Portal</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

@gateway_app.post("/login")
def gateway_login(request: Request, db: Session = Depends(get_db)):
    attacker = get_session_and_log(request, db)
    return JSONResponse(status_code=401, content={"error": "Unauthorized", "detail": "Invalid credentials provided."})

@gateway_app.api_route("/.env", methods=["GET", "HEAD"])
@gateway_app.api_route("/config/database", methods=["GET", "HEAD"])
@gateway_app.api_route("/backup/db", methods=["GET", "HEAD"])
@gateway_app.api_route("/backup/keys", methods=["GET", "HEAD"])
@gateway_app.api_route("/robots.txt", methods=["GET", "HEAD"])
@gateway_app.api_route("/sitemap.xml", methods=["GET", "HEAD"])
@gateway_app.api_route("/.git", methods=["GET", "HEAD"])
def gateway_files(request: Request, db: Session = Depends(get_db)):
    attacker = get_session_and_log(request, db)
    path = request.url.path
    norm_path = normalize_path(path)

    # Check for deployed lure matching endpoint
    lure = db.query(Lure).filter(
        (Lure.endpoint_path == path) | (Lure.endpoint_path == norm_path),
        Lure.status == "deployed"
    ).first()
    if lure:
        record_interaction(db, lure_id=lure.lure_id, session_id=attacker.session_id, interaction_type="VIEW")
        return PlainTextResponse(content=lure.content)

    # If no specific deployed lure, return synthetic default probe responses
    if norm_path == "/robots.txt":
        return PlainTextResponse("User-agent: *\nDisallow: /admin/\nDisallow: /config/\nDisallow: /backup/\n")
    if norm_path == "/sitemap.xml":
        return PlainTextResponse("<?xml version=\"1.0\" encoding=\"UTF-8\"?><urlset><url><loc>http://meridian-tech.internal/</loc></url></urlset>")

    return PlainTextResponse(content=f"# Synthetic file endpoint for {path}\n# Access logged by Meridian Security Gate", status_code=404)

@gateway_app.api_route("/lures/{path:path}", methods=["GET", "HEAD"])
def gateway_lure_dynamic(path: str, request: Request, db: Session = Depends(get_db)):
    attacker = get_session_and_log(request, db)
    full_path = f"/lures/{path}"
    norm_full_path = normalize_path(request.url.path)

    lure = db.query(Lure).filter(
        (Lure.endpoint_path == full_path) |
        (Lure.endpoint_path == norm_full_path) |
        (Lure.endpoint_path == request.url.path) |
        (Lure.title == path)
    ).first()
    if lure:
        record_interaction(db, lure_id=lure.lure_id, session_id=attacker.session_id, interaction_type="VIEW")
        return PlainTextResponse(content=lure.content)

    return PlainTextResponse(content="# Lure not found", status_code=404)
