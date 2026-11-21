from abc import ABC, abstractmethod


class generationStrategy(ABC):
    @abstractmethod
    def generate_response(self, question_text: str) -> str:
        pass
