import grpc
import yandex.cloud.ai.stt.v3.stt_pb2 as stt_pb2
import yandex.cloud.ai.stt.v3.stt_service_pb2_grpc as stt_service_pb2_grpc
from typing import BinaryIO, Generator, List, Optional, Callable

CHUNK_SIZE = 4000

class STT:
    def __init__(self, api_key: str = None, iam_token: str = None, language_code: str = 'ru-RU', sample_rate: int = 48000):
        """
        Инициализация класса распознавания речи с использованием Yandex Cloud STT
        
        Args:
            api_key: API ключ для аутентификации в Yandex Cloud
            iam_token: IAM токен для аутентификации в Yandex Cloud
            language_code: Код языка для распознавания
            sample_rate: Частота дискретизации аудио (Гц)
        """
        self.api_key = api_key
        self.iam_token = iam_token
        self.language_code = language_code
        self.sample_rate = sample_rate
        
        # Создание подключения к API Яндекс STT
        cred = grpc.ssl_channel_credentials()
        self.channel = grpc.secure_channel('stt.api.cloud.yandex.net:443', cred)
        self.stub = stt_service_pb2_grpc.RecognizerStub(self.channel)
    
    def _create_streaming_options(self, sample_rate: int = None) -> stt_pb2.StreamingOptions:
        """Создание настроек распознавания для потокового API"""
        if sample_rate is None:
            sample_rate = self.sample_rate
            
        return stt_pb2.StreamingOptions(
            recognition_model=stt_pb2.RecognitionModelOptions(
                audio_format=stt_pb2.AudioFormatOptions(
                    raw_audio=stt_pb2.RawAudio(
                        audio_encoding=stt_pb2.RawAudio.LINEAR16_PCM,
                        sample_rate_hertz=sample_rate,
                        audio_channel_count=1
                    )
                ),
                text_normalization=stt_pb2.TextNormalizationOptions(
                    text_normalization=stt_pb2.TextNormalizationOptions.TEXT_NORMALIZATION_ENABLED,
                    profanity_filter=True,
                    literature_text=False
                ),
                language_restriction=stt_pb2.LanguageRestrictionOptions(
                    restriction_type=stt_pb2.LanguageRestrictionOptions.WHITELIST,
                    language_code=[self.language_code]
                ),
                audio_processing_type=stt_pb2.RecognitionModelOptions.REAL_TIME
            )
        )
    
    def _get_auth_metadata(self):
        """Получение метаданных для авторизации"""
        if self.api_key:
            return [('authorization', f'Api-Key {self.api_key}')]
        elif self.iam_token:
            return [('authorization', f'Bearer {self.iam_token}')]
        else:
            raise ValueError("Не указан ни API ключ, ни IAM токен для авторизации")
    
    def _generate_requests(self, audio_data: bytes, sample_rate: int = None) -> Generator[stt_pb2.StreamingRequest, None, None]:
        """
        Создает генератор запросов для потокового распознавания
        
        Args:
            audio_data: Байты аудио данных
            sample_rate: Опциональная частота дискретизации
        
        Yields:
            Объекты StreamingRequest для передачи в API
        """
        # Отправляем настройки распознавания
        yield stt_pb2.StreamingRequest(session_options=self._create_streaming_options(sample_rate))
        
        # Отправляем аудио данные по чанкам
        position = 0
        while position < len(audio_data):
            chunk = audio_data[position:position + CHUNK_SIZE]
            yield stt_pb2.StreamingRequest(chunk=stt_pb2.AudioChunk(data=chunk))
            position += CHUNK_SIZE
    
    def transcribe_audio_stream(self, audio_data: bytes, sample_rate: int = None) -> str:
        """
        Распознает речь из потока аудио данных
        
        Args:
            audio_data: Байты аудио данных
            sample_rate: Опциональная частота дискретизации
        
        Returns:
            Распознанный текст
        """
        try:
            metadata = self._get_auth_metadata()
            responses = self.stub.RecognizeStreaming(
                self._generate_requests(audio_data, sample_rate), 
                metadata=metadata
            )
            
            recognized_text = []
            for response in responses:
                event_type = response.WhichOneof('Event')
                
                if event_type == 'final' and response.final.alternatives:
                    recognized_text.append(response.final.alternatives[0].text)
                elif event_type == 'final_refinement' and response.final_refinement.normalized_text.alternatives:
                    recognized_text.append(response.final_refinement.normalized_text.alternatives[0].text)
                    
            return " ".join(recognized_text)
            
        except Exception as e:
            return f"Ошибка при распознавании аудио: {str(e)}"
    
    def stream_recognition(self, audio_chunks_gen, on_partial=None, on_final=None, sample_rate: int = 8000):
        """
        Потоковое распознавание речи из генератора аудио-чанков
        
        Args:
            audio_chunks_gen: Генератор аудио-чанков (bytes)
            on_partial: Функция обратного вызова для частичных результатов
            on_final: Функция обратного вызова для финальных результатов
            sample_rate: Частота дискретизации входного аудио
            
        Returns:
            Полный распознанный текст
        """
        try:
            # Генератор запросов
            def request_generator():
                # Сначала отправляем настройки
                yield stt_pb2.StreamingRequest(
                    session_options=self._create_streaming_options(sample_rate)
                )
                
                # Затем отправляем аудио данные
                for chunk in audio_chunks_gen:
                    if chunk:
                        yield stt_pb2.StreamingRequest(
                            chunk=stt_pb2.AudioChunk(data=chunk)
                        )
            
            # Получаем ответы от API
            metadata = self._get_auth_metadata()
            responses = self.stub.RecognizeStreaming(
                request_generator(), 
                metadata=metadata
            )
            
            # Обрабатываем ответы
            full_text = []
            for response in responses:
                event_type = response.WhichOneof('Event')
                
                if event_type == 'partial' and response.partial.alternatives:
                    partial_text = response.partial.alternatives[0].text
                    if on_partial:
                        on_partial(partial_text)
                
                elif event_type == 'final' and response.final.alternatives:
                    final_text = response.final.alternatives[0].text
                    full_text.append(final_text)
                    if on_final:
                        on_final(final_text)
                
                elif event_type == 'final_refinement' and response.final_refinement.normalized_text.alternatives:
                    refined_text = response.final_refinement.normalized_text.alternatives[0].text
                    if full_text:  # Заменяем последний результат на уточненный
                        full_text[-1] = refined_text
                    else:
                        full_text.append(refined_text)
                    if on_final:
                        on_final(refined_text, is_refinement=True)
            
            return " ".join(full_text)
            
        except Exception as e:
            error_msg = f"Ошибка потокового распознавания: {str(e)}"
            if on_final:
                on_final(error_msg, is_error=True)
            return error_msg
    
    def transcribe_microphone(self, audio_data: bytes) -> str:
        """
        Распознает речь из микрофона (данные в формате bytes)
        
        Args:
            audio_data: Байты аудио данных с микрофона (LINEAR16_PCM, 48кГц)
        
        Returns:
            Распознанный текст
        """
        return self.transcribe_audio_stream(audio_data)
    
    def transcribe_browser_audio(self, audio_data: bytes, sample_rate: int = 48000) -> str:
        """
        Распознает речь из аудиоданных от браузера
        
        Args:
            audio_data: Байты аудио данных из браузера
            sample_rate: Частота дискретизации аудио
        
        Returns:
            Распознанный текст
        """
        try:
            metadata = self._get_auth_metadata()
            
            # Проверяем, содержат ли данные WAV-заголовок
            has_wav_header = len(audio_data) > 12 and audio_data.startswith(b'RIFF') and b'WAVE' in audio_data[0:12]
            
            # Если обнаружен WAV-заголовок, пропускаем его (44 байта)
            if has_wav_header:
                audio_data = audio_data[44:]
            
            # Используем потоковое распознавание вместо RecognizeFile
            def request_generator():
                # Отправляем настройки
                yield stt_pb2.StreamingRequest(
                    session_options=self._create_streaming_options(sample_rate)
                )
                
                # Отправляем аудио данные порциями
                for i in range(0, len(audio_data), CHUNK_SIZE):
                    chunk = audio_data[i:i + CHUNK_SIZE]
                    yield stt_pb2.StreamingRequest(
                        chunk=stt_pb2.AudioChunk(data=chunk)
                    )
            
            # Получаем ответы от API
            responses = self.stub.RecognizeStreaming(
                request_generator(), 
                metadata=metadata
            )
            
            # Обрабатываем ответы
            result_text = []
            for response in responses:
                event_type = response.WhichOneof('Event')
                
                if event_type == 'final' and response.final.alternatives:
                    result_text.append(response.final.alternatives[0].text)
                elif event_type == 'final_refinement' and response.final_refinement.normalized_text.alternatives:
                    result_text.append(response.final_refinement.normalized_text.alternatives[0].text)
            
            return " ".join(result_text)
            
        except Exception as e:
            print(f"Ошибка при распознавании аудио: {str(e)}")
            return f"Ошибка при распознавании аудио: {str(e)}"
    
    def transcribe_audio(self, audio_file: BinaryIO) -> str:
        """
        Распознает речь из файлового объекта
        
        Args:
            audio_file: Файловый объект с аудио
        
        Returns:
            Распознанный текст
        """
        try:
            audio_data = audio_file.read()
            return self.transcribe_audio_stream(audio_data)
        except Exception as e:
            return f"Ошибка при чтении аудио файла: {str(e)}"
    
    def transcribe_from_path(self, file_path: str) -> str:
        """
        Распознает речь из файла по указанному пути
        
        Args:
            file_path: Путь к аудио файлу
        
        Returns:
            Распознанный текст
        """
        try:
            with open(file_path, "rb") as audio_file:
                return self.transcribe_audio(audio_file)
        except FileNotFoundError:
            return "Ошибка: Аудио файл не найден"
        except Exception as e:
            return f"Ошибка при открытии аудио файла: {str(e)}"