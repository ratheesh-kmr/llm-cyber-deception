"""
Deception Gateway entry point for standalone deployment (port 8001).
"""
from app.gateway import gateway_app as app

__all__ = ["app"]
