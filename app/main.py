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
async def get_chat_page(request: Request):
    return index_html.TemplateResponse(
        "index.html", 
        {
            "request": request
        }
    )

# WebSocket текста
@app.websocket("/ws/text")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            # Получаем текст от пользователя
            user_input = await ws.receive_text()
            pp(f"user_input: {message}")
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
