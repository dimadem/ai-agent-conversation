from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.model.ttt import TTT
from app.model.stt import STT
from app.model.tts import TTS
from pprint import pp
import base64

app = FastAPI()
ttt = TTT()
stt = STT()
tts = TTS()

# Инициализируем frontend
index_html = Jinja2Templates(directory="app/frontend")

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

# WebSocket текста
@app.websocket("/ws/text")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            # Получаем текст от пользователя
            user_input = await ws.receive_text()
            pp(f"user_input: {user_input}")

            # Создаем сообщение для TTT
            message = ttt.create_chat_message("user", user_input)

            # Генерируем ответ через TTT
            agent_response = ttt.generate_response([message])
            pp(f"agent_response: {agent_response}")

            # Отправляем ответ пользоват
            await ws.send_json(
                {
                    "user_input_text": user_input,
                    "agent_response_text": agent_response
                }
            )
    except WebSocketDisconnect:
        pass

# WebSocket голоса
@app.websocket("/ws/voice")
async def websocket_voice(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            # Получаем аудио от пользователя
            audio_data = await ws.receive_text()

            # Декодируем base64 в аудио
            audio_bytes = base64.b64decode(audio_data)
            
            # Сохраняем временный файл
            with open("temp_audio.wav", "wb") as f:
                f.write(audio_bytes)
            
            # Транскрибируем с помощью Whisper
            user_input = stt.transcribe_from_path("temp_audio.wav")
            pp(f"user_input: {user_input}")
            # Создаем сообщение для TTT
            chat_message = ttt.create_chat_message("user", user_input)
            # Генерируем ответ через TTT
            agent_response_text = ttt.generate_response([chat_message])
            pp(f"agent_response_text: {agent_response_text}")

            # Генерируем ответ через TTS
            response = tts.generate_speech(agent_response_text)
            
            # Конвертируем аудио ответ в base64
            agent_response_audio = base64.b64encode(response.content).decode('utf-8')
            
            # Отправляем и текст, и аудио
            await ws.send_json(
                {
                    "user_input_text": user_input,
                    "agent_response_text": agent_response_text,
                    "agent_response_audio": agent_response_audio
                }
            )
    except WebSocketDisconnect:
        pass


@app.post("/api/evaluation")
async def evaluate_endpoint(request: Request):
    pp(f"=== Evaluation endpoint ===")
    data = await request.json()
    pp(data)

    return "Evaluation endpoint"

@app.post("/api/select-persona")
async def select_persona_endpoint(request: Request):
    pp(f"=== Select persona endpoint ===")
    data = await request.json()
    pp(data)
    available_personas = ["Persona1", "Persona2", "Persona3"]
    return {"message": "Select persona endpoint", "personas": available_personas}

@app.post("/api/interview")
async def interview_endpoint(request: Request):
    pp(f"=== Interview endpoint ===")
    data = await request.json()
    pp(data)
    return data