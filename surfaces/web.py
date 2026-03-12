"""
web surface — fastapi interface for browser-based interaction.
"""

import os
from fastapi import Request
from fastapi.responses import HTMLResponse, JSONResponse


async def index():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())
