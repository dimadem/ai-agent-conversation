from fastapi import FastAPI, WebSocket, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Dict, Any
import logging
from app.api.websocket import WebSocketManager
from app.core.constants import FRONTEND_DIR

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
ws_manager = WebSocketManager()

# Инициализируем frontend
index_html = Jinja2Templates(directory=FRONTEND_DIR)

# Роут для отображения HTML страницы
@app.get("/", response_class=HTMLResponse)
async def index_page(request: Request):
    return index_html.TemplateResponse("index.html", {"request": request})

@app.get("/select-persona", response_class=HTMLResponse)
async def select_persona_page(request: Request):
    return index_html.TemplateResponse("select-persona.html", {"request": request})

@app.get("/interview", response_class=HTMLResponse)
async def interview_page(request: Request):
    return index_html.TemplateResponse("interview.html", {"request": request})

@app.get("/evaluation", response_class=HTMLResponse)
async def evaluation_page(request: Request):
    return index_html.TemplateResponse("evaluation.html", {"request": request})

# WebSocket endpoints
@app.websocket("/ws/text")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    await ws_manager.handle_text(ws)

@app.websocket("/ws/voice")
async def websocket_voice(ws: WebSocket):
    await ws.accept()
    await ws_manager.handle_voice(ws)


@app.post("/api/evaluation")
async def evaluate_endpoint(request: Request) -> Dict[str, Any]:
    logger.info("Evaluation endpoint called")
    data = await request.json()
    logger.info(f"Received evaluation data: {data}")
    return {"status": "success", "message": "Evaluation received"}

@app.post("/api/select-persona")
async def select_persona_endpoint(request: Request) -> Dict[str, Any]:
    logger.info("Select persona endpoint called")
    data = await request.json()
    logger.info(f"Selected persona: {data}")
    return {"status": "success", "data": data}

@app.post("/api/interview")
async def interview_endpoint(request: Request) -> Dict[str, Any]:
    logger.info("Interview endpoint called")
    data = await request.json()
    logger.info(f"Interview data: {data}")
    return {"status": "success", "data": data}
