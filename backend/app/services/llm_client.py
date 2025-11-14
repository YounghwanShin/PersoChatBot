"""LLM client abstraction for generation tasks."""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from google import genai
from google.genai import types


class LLMClient(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """Generate text from prompt."""
        pass


class GeminiLLMClient(LLMClient):
    """Gemini API-based LLM client."""

    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-2.0-flash",
        default_temperature: float = 0.1,
        default_max_tokens: int = 512
    ):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.default_temperature = default_temperature
        self.default_max_tokens = default_max_tokens

    def generate(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """Generate text using Gemini API."""
        config = types.GenerateContentConfig(
            temperature=temperature if temperature is not None else self.default_temperature,
            max_output_tokens=max_tokens if max_tokens is not None else self.default_max_tokens,
        )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=config
        )

        return response.text.strip()


def create_llm_client(
    api_key: str,
    model_name: str = "gemini-2.0-flash",
    temperature: float = 0.1,
    max_tokens: int = 512
) -> LLMClient:
    """Factory function to create LLM client."""
    return GeminiLLMClient(
        api_key=api_key,
        model_name=model_name,
        default_temperature=temperature,
        default_max_tokens=max_tokens
    )
