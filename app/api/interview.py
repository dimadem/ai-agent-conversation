from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from typing import Optional
import base64
import json

from app.model.ttt import TTT
from app.model.stt import STT
from app.model.tts import TTS

from app.features.interview import interviewee_response
from app.prompts.utils import load_prompts
from pprint import pp

router = APIRouter()

ttt = TTT()
stt = STT()
tts = TTS()
prompts = load_prompts("persona_system_prompt.yaml")

@router.websocket("/ws/interview")
async def websocket_interview(ws: WebSocket):
    await ws.accept()
    conversation_history = []
    
    # Используем фиксированные значения
    persona = "Junior Python Developer"
    skill = "Python programming"
    
    pp(f"WebSocket connected with default persona: {persona}, skill: {skill}")
    
    try:
        while True:
            data = await ws.receive_text()
            is_audio = False
            user_input = ""
            
            # Определяем тип входящих данных (текст или аудио)
            try:
                # Пытаемся распарсить JSON
                pp(f"Received data: {data[:100]}..." if len(data) > 100 else f"Received data: {data}")
                json_data = json.loads(data)
                pp(f"Parsed JSON: {json_data}")
                
                # Обработка аудио
                if "audio" in json_data:
                    is_audio = True
                    pp("Processing audio data")
                    audio_bytes = base64.b64decode(json_data["audio"])
                    
                    # Сохранение и транскрибирование аудио
                    with open("temp/temp_audio.wav", "wb") as f:
                        f.write(audio_bytes)
                    user_input = stt.transcribe_from_path("temp/temp_audio.wav")
                    pp(f"Transcribed: {user_input}")
                else:
                    # Текстовый режим
                    pp("Processing text data from JSON")
                    user_input = json_data.get("message", data)
                    pp(f"Extracted message: {user_input}")
            except json.JSONDecodeError as e:
                # Если не JSON, то просто текст
                pp(f"Not a valid JSON, treating as plain text: {e}")
                user_input = data
            except Exception as e:
                # Другие ошибки
                pp(f"Error processing data: {str(e)}")
                user_input = f"Error processing input: {str(e)}"
            
            pp(f"User input: {user_input}")
            
            # Формируем системный промпт с указанными значениями
            system_prompt = prompts["persona_system_prompt"].format(
                persona=persona, skill=skill
            )
            
            # Создаем сообщения и формируем историю
            messages = [
                ttt.create_chat_message("system", system_prompt),
                *conversation_history,
                ttt.create_chat_message("user", user_input)
            ]
            
            try:
                # Генерируем ответ
                response = interviewee_response(messages)
                pp(f"Response type: {type(response)}")
                
                # Проверяем тип ответа (может быть словарь или строка)
                if isinstance(response, dict):
                    agent_text = response.get("response", "Sorry, I couldn't generate a response.")
                else:
                    # Если response - это строка
                    agent_text = str(response)
                
                pp(f"Agent response: {agent_text}")
            except Exception as e:
                pp(f"Error generating response: {str(e)}")
                agent_text = f"Error: {str(e)}"
            
            # Добавляем сообщения в историю
            conversation_history.append(ttt.create_chat_message("user", user_input))
            conversation_history.append(ttt.create_chat_message("assistant", agent_text))
            
            # Ограничиваем размер истории
            if len(conversation_history) > 10:
                conversation_history = conversation_history[-10:]
            
            # Режим аудио-ответа
            if is_audio:
                tts_response = tts.generate_speech(agent_text)
                agent_audio = base64.b64encode(tts_response.content).decode('utf-8')
                
                await ws.send_json({
                    "type": "voice",
                    "text": agent_text,
                    "user_text": user_input,  # Отправляем транскрибированный текст
                    "audio": agent_audio
                })
            else:
                # Только текстовый ответ
                await ws.send_json({
                    "type": "text",
                    "text": agent_text
                })
    except WebSocketDisconnect:
        pp("WebSocket disconnected")