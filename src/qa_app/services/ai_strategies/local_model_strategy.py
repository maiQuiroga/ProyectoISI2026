from .base import generationStrategy 
  

class localModelStrategy(generationStrategy):
    def generate_response(self, question_text: str) -> str:
        raise NotImplementedError("Pendiente: integrar modelo local ")
