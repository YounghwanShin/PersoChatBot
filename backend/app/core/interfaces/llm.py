"""Protocol for LLM clients."""

from typing import Protocol, Optional


class LLMClientProtocol(Protocol):
    """Protocol defining the interface for LLM clients."""

    def generate(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """Generate text from prompt.

        Args:
            prompt: Input prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text
        """
        ...
