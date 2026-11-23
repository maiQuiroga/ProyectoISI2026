from datetime import date, timedelta

from src.qa_app.services.ai_response_detector import AIResponseDetector
from src.qa_app.services.ai_strategies.strategies import (
    geminiStrategy,
    localModelStrategy,
    openAIStrategy,
)
from src.qa_app.services.auto_response_service import AIAgent, AutoResponseService


def test_detector_identifies_ia_help_tag_and_inactivity():
    detector = AIResponseDetector(trigger_tag="ia-help", inactive_days=7)

    q_tag = {
        "title": "UML",
        "body": "Diagrama de secuencias",
        "tags": ["#ia-help"],
        "created_at": date.today(),
    }
    q_inactive = {
        "title": "SQL",
        "body": "Índices",
        "tags": ["db"],
        "created_at": date.today() - timedelta(days=8),
    }
    q_recent = {
        "title": "Python",
        "body": "Listas",
        "tags": ["python"],
        "created_at": date.today() - timedelta(days=2),
    }

    assert detector.requires_ai_response(q_tag) is True
    assert detector.detection_reason(q_tag) == "trigger_tag"

    assert detector.requires_ai_response(q_inactive) is True
    assert detector.detection_reason(q_inactive) == "inactivity"

    assert detector.requires_ai_response(q_recent) is False
    assert detector.detection_reason(q_recent) is None


def test_dynamic_strategy_switching_and_ai_agent_attribution():
    agent = AIAgent(name="Asistente ISI", provider="OpenAI", version="1.0")
    service = AutoResponseService(strategy=openAIStrategy(), agent=agent)

    question = {
        "title": "Normalización",
        "body": "¿Cuándo pasar de 2FN a 3FN?",
        "tags": ["#ia-help"],
        "created_at": date.today(),
    }

    resp_openai = service.generate_for_question(question)
    assert resp_openai is not None
    assert "[OpenAI simulado]" in resp_openai["body"]
    assert resp_openai["is_ai"] is True
    assert resp_openai["author"] is agent
    assert resp_openai["author_name"] == "Asistente ISI"

    # Cambio dinámico a GeminiStrategy
    service.set_strategy(geminiStrategy())
    resp_gemini = service.generate_for_question(question)
    assert resp_gemini is not None
    assert "[Gemini simulado]" in resp_gemini["body"]
    assert resp_gemini["author"] is agent

    # Cambio dinámico a localModelStrategy
    service.set_strategy(localModelStrategy())
    resp_local = service.generate_for_question(question)
    assert resp_local is not None
    assert "[Modelo local simulado]" in resp_local["body"]
    assert resp_local["author"] is agent


def test_no_response_when_not_triggered_unless_forced():
    service = AutoResponseService(strategy=openAIStrategy())
    question = {
        "title": "Git",
        "body": "¿Cómo hacer rebase?",
        "tags": ["git"],
        "created_at": date.today(),
    }

    assert service.generate_for_question(question) is None

    forced = service.generate_for_question(question, force=True)
    assert forced is not None
    assert forced["is_ai"] is True
