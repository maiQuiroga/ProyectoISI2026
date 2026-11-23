from .base import generationStrategy 
  

class geminiStrategy(generationStrategy):
    def generate_response(self, question_text: str) -> str:
        raise NotImplementedError("Pendiente: integrar SDK de Gemini")
