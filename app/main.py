from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request as StarletteRequest
from typing import Dict, Optional

from pprint import pp

from app.api.evaluation import router as evaluation_router
from app.api.interview import router as interview_router


app = FastAPI()

app.include_router(evaluation_router)
app.include_router(interview_router)

# Инициализируем frontend
index_html = Jinja2Templates(directory="app/frontend")

# Роут для отображения HTML страницы
@app.get("/", response_class=HTMLResponse)
async def index_page(request: Request):
    return index_html.TemplateResponse("index.html", {"request": request})

@app.get("/select-persona", response_class=HTMLResponse)
async def select_persona_page(request: Request):
    return index_html.TemplateResponse("select-candidate.html", {"request": request})

@app.get("/interview", response_class=HTMLResponse)
async def interview_page(request: Request):
    # Simplified - no session usage
    context = {"request": request}
    return index_html.TemplateResponse("interview.html", context)

@app.get("/evaluation", response_class=HTMLResponse)
async def evaluation_page(request: Request):
    return index_html.TemplateResponse("evaluation.html", {"request": request})

@app.get("/report", response_class=HTMLResponse)
async def report_page(request: Request):
    return index_html.TemplateResponse("report.html", {"request": request})

@app.post("/api/select-persona")
async def select_persona_endpoint(request: Request):
    pp(f"=== Select persona endpoint ===")
    data = await request.json()
    
    # No session storage - just return the data
    pp(data)
    return data

@app.post("/api/interview")
async def interview_endpoint(request: Request):
    pp(f"=== Interview endpoint ===")
    data = await request.json()
    pp(data)
    return data