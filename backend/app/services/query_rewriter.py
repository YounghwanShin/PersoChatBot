"""Query rewriting service for better retrieval."""

from typing import Optional
from .llm_client import LLMClient


class QueryRewriterService:
    """Service for rewriting user queries for better retrieval."""

    def __init__(self, llm_client: Optional[LLMClient] = None):
        """Initialize query rewriter with optional LLM client."""
        self.llm_client = llm_client

    def rewrite_query(self, query: str, expand: bool = True) -> str:
        """Rewrite query for better retrieval."""
        if not self.llm_client or not expand:
            return query.strip()

        prompt = f"""Rewrite this question to be more search-friendly by expanding with synonyms and related terms. Keep it concise.

Question: {query}

Return only the rewritten query, nothing else."""

        try:
            rewritten = self.llm_client.generate(prompt)
            return rewritten if rewritten else query.strip()

        except Exception as e:
            print(f"Query rewriting failed, using original: {e}")
            return query.strip()
