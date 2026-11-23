from .base import generationStrategy


class openAIStrategy(generationStrategy):
    def generate_response(self, question_text: str) -> str:
        raise NotImplementedError("Pendiente: integrar SDK de OpenAI")
