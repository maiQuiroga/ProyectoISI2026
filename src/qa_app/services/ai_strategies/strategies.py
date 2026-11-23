from qa_app.services.ai_strategies.base import generationStrategy


class openAIStrategy(generationStrategy):
    def generate_response(self, question_text: str) -> str:
        clean_question = question_text.strip()
        return (
            f"[OpenAI simulado] Análisis para '{clean_question}': "
            "Revisá el planteo paso a paso, verificá las precondiciones y "
            "probá con un caso mínimo."
        )


class geminiStrategy(generationStrategy):
    def generate_response(self, question_text: str) -> str:
        clean_question = question_text.strip()
        return (
            f"[Gemini simulado] Guía para '{clean_question}': "
            "Dividí el problema en partes pequeñas, identificá las relaciones "
            "clave y validá el resultado."
        )


class localModelStrategy(generationStrategy):
    def generate_response(self, question_text: str) -> str:
        clean_question = question_text.strip()
        return (
            f"[Modelo local simulado] Respuesta para '{clean_question}': "
            "Comprobá los tipos de datos, el flujo principal y los posibles "
            "casos borde."
        )
