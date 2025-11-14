"""Protocol for query processing."""

from typing import Protocol


class QueryProcessorProtocol(Protocol):
    """Protocol defining the interface for query processors."""

    def process_query(self, query: str) -> str:
        """Process and potentially rewrite the query.

        Args:
            query: Original user query

        Returns:
            Processed query
        """
        ...
