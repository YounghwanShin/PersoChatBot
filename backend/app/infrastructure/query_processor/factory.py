"""Factory for creating query processors."""

from typing import Optional

from ...core.interfaces import QueryProcessorProtocol, LLMClientProtocol
from .rewriter import QueryRewriter


def create_query_processor(
    llm_client: Optional[LLMClientProtocol] = None
) -> QueryProcessorProtocol:
    """Create a query processor instance.

    Args:
        llm_client: Optional LLM client for query rewriting

    Returns:
        Query processor instance
    """
    return QueryRewriter(llm_client=llm_client)
