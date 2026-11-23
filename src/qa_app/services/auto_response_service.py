from datetime import UTC, datetime
from typing import Any

from qa_app.models.answer import Answer
from qa_app.models.user import AiAgent
from qa_app.services.ai_response_detector import AIResponseDetector
from qa_app.services.ai_strategies.base import generationStrategy
from qa_app.services.ai_strategies.strategies import openAIStrategy

# Alias para mantener compatibilidad con el nombre del issue (AIAgent / AiAgent)
AIAgent = AiAgent


def build_ai_agent(
    name: str = "Agente IA",
    provider: str = "OpenAI",
    version: str = "1.0",
) -> AIAgent:
    return AIAgent(name=name, provider=provider, version=version)


class AutoResponseService:
    """Coordina la detección, generación y asignación de autoría al agente IA."""

    def __init__(
        self,
        strategy: generationStrategy | None = None,
        detector: AIResponseDetector | None = None,
        agent: AIAgent | None = None,
    ) -> None:
        self.strategy: generationStrategy = strategy or openAIStrategy()
        self.detector: AIResponseDetector = detector or AIResponseDetector()
        self.agent: AIAgent = agent or build_ai_agent()

    def set_strategy(self, strategy: generationStrategy) -> None:
        self.strategy = strategy

    def _extract_question_text(self, question: Any) -> str:
        if isinstance(question, dict):
            title = str(question.get("title", "")).strip()
            body = str(question.get("body", "")).strip()
        else:
            title = str(getattr(question, "title", "") or "").strip()
            body = str(getattr(question, "body", "") or "").strip()

        if title and body:
            return f"{title} - {body}"
        return title or body

    def generate_for_question(
        self,
        question: Any,
        force: bool = False,
        now: datetime | None = None,
    ) -> Answer | dict[str, Any] | None:
        if not force and not self.detector.requires_ai_response(question, now=now):
            return None

        question_text = self._extract_question_text(question)
        response_body = self.strategy.generate_response(question_text)

        if hasattr(question, "id"):
            answer = Answer(
                body=response_body,
                author=self.agent,
                author_id=self.agent.id,
                question=question,
                question_id=question.id,
                is_accepted=False,
            )
            return answer

        return {
            "author": self.agent,
            "author_id": self.agent.id,
            "author_name": self.agent.get_name(),
            "provider": self.agent.provider,
            "version": self.agent.version,
            "body": response_body,
            "is_ai": True,
            "is_accepted": False,
            "created_at": datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC"),
        }
