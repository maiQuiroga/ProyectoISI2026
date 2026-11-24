
import os

from dotenv import load_dotenv
from google import genai

from qa_app.services.ai_strategies.base import generationStrategy

load_dotenv()

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
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            return (
             f"[Gemini simulado] Guía para '{clean_question}': "
             "Dividí el problema en partes pequeñas, identificá las relaciones "
             "clave y validá el resultado."
            )

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=(
                "Respondé de forma clara, breve y útil en español a la "
                f"siguiente pregunta universitaria:\n\n{clean_question}"
            ),
        )
        return response.text.strip() if response.text else ""



class localModelStrategy(generationStrategy):
    def generate_response(self, question_text: str) -> str:
        clean_question = question_text.strip()
        return (
            f"[Modelo local simulado] Respuesta para '{clean_question}': "
            "Comprobá los tipos de datos, el flujo principal y los posibles "
            "casos borde."
        )
