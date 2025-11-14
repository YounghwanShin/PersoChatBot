"""Query rewriter implementation."""

from typing import Optional

from ...core.interfaces import LLMClientProtocol
from ...core.exceptions import QueryProcessingError


class QueryRewriter:
    """Query rewriter using LLM for query expansion."""

    def __init__(self, llm_client: Optional[LLMClientProtocol] = None):
        """Initialize query rewriter.

        Args:
            llm_client: Optional LLM client for query expansion
        """
        self.llm_client = llm_client

    def process_query(self, query: str) -> str:
        """Process and potentially rewrite the query.

        Args:
            query: Original user query

        Returns:
            Processed query
        """
        if not self.llm_client:
            return query.strip()

        prompt = f"""Rewrite this question to be more search-friendly by expanding with synonyms and related terms. Keep it concise.

Question: {query}

Return only the rewritten query, nothing else."""

        try:
            rewritten = self.llm_client.generate(prompt)
            return rewritten if rewritten else query.strip()

        except Exception as e:
            raise QueryProcessingError(f"Query rewriting failed: {e}")
