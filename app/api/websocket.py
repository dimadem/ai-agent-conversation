import base64
from fastapi import WebSocket, WebSocketDisconnect
from app.model.ttt import TTT
from app.model.stt import STT
from app.model.tts import TTS
from app.core.constants import TEMP_AUDIO_FILE
import logging
import os
from typing import Dict, Any

logger = logging.getLogger(__name__)

class WebSocketManager:
    def __init__(self):
        self.ttt = TTT()
        self.stt = STT()
        self.tts = TTS()

    async def handle_text(self, ws: WebSocket) -> None:
        try:
            while True:
                user_input = await ws.receive_text()
                logger.info(f"Received text input: {user_input}")
                
                # Обрабатываем текстовый запрос
                chat_message = self.ttt.create_message("user", user_input)
                agent_response_text = self.ttt.generate_response([chat_message])
                logger.info(f"Generated response: {agent_response_text}")
                
                # Отправляем текстовый ответ
                await ws.send_json({
                    "agent_response_text": agent_response_text
                })
        except WebSocketDisconnect:
            logger.info("WebSocket disconnected")
        except Exception as e:
            logger.error(f"Error in text websocket: {str(e)}")
            raise

    async def handle_voice(self, ws: WebSocket) -> None:
        try:
            while True:
                audio_data = await ws.receive_text()
                audio_bytes = base64.b64decode(audio_data)
                
                # Сохраняем временный файл
                with open(TEMP_AUDIO_FILE, "wb") as f:
                    f.write(audio_bytes)
                    
                try:
                    user_input = self.stt.transcribe_browser_audio(audio_bytes, sample_rate=48000)
                    logger.info(f"Transcribed input: {user_input}")
                    
                    if not user_input or user_input.startswith("Ошибка"):
                        logger.error(f"Ошибка распознавания речи: {user_input}")
                        await ws.send_json({
                            "error": "Не удалось распознать речь. Пожалуйста, попробуйте снова."
                        })
                        continue
                        
                    chat_message = self.ttt.create_message("user", user_input)
                    agent_response_text = self.ttt.generate_response([chat_message])
                    logger.info(f"Generated response: {agent_response_text}")

                    # Генерируем аудиоответ
                    response = self.tts.generate_speech(agent_response_text)
                    agent_response_audio = base64.b64encode(response.content).decode('utf-8')
                        
                    await ws.send_json({
                        "user_input_text": user_input,
                        "agent_response_text": agent_response_text,
                        "agent_response_audio": agent_response_audio
                    })
                    
                except Exception as e:
                    logger.error(f"Ошибка при обработке аудио: {str(e)}")
                    await ws.send_json({
                        "error": "Произошла ошибка при обработке речи"
                    })
                        
        except WebSocketDisconnect:
            logger.info("WebSocket disconnected")
        except Exception as e:
            logger.error(f"Error in voice websocket: {str(e)}")
            raise
