from fastapi import APIRouter, Request
from pprint import pp
from app.features.evaluation import extract_star_components

router = APIRouter()

# Глобальная переменная для хранения результата последней оценки
last_evaluation_result = None

@router.post("/api/evaluation")
async def evaluate_endpoint(request: Request):
    global last_evaluation_result
    pp(f"=== Evaluation endpoint ===")
    data = await request.json()
    messages = data.get("messages")
    response = extract_star_components(messages) # Вызов функции для извлечения компонентов STAR
    pp(f"=== Evaluation endpoint response ===")
    print(response)
    # Сохраняем результат для использования на странице отчета
    last_evaluation_result = response
    return response

@router.get("/api/evaluation/result")
async def get_last_evaluation_result():
    """Возвращает результат последней оценки"""
    return last_evaluation_result or {"Situation": "-", "Task": "-", "Action": "-", "Result": "-"}