from abc import ABC, abstractmethod

class generationStrategy(ABC):
  """Contrato comun para todos los proveedores de IA."""

  @abstractmethod
  def generate_response(self, question_text: str) ->str:
    """Genera una respuesta de texto a partir de la pregunta del usuario"""
    raise NotImplementedError  
﻿from abc import ABC, abstractmethod


class generationStrategy(ABC):
    @abstractmethod
    def generate_response(self, question_text: str) -> str:
        pass
