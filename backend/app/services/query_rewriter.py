"""Query rewriting service for better retrieval using Gemini API."""

from typing import Optional
from google import genai


class QueryRewriterService:
    """Service for rewriting user queries for better retrieval using Gemini API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize query rewriter with optional Gemini API key."""
        self.api_key = api_key
        self.client = None
        
        if api_key:
            self.client = genai.Client(api_key=api_key)
    
    def rewrite_query(
        self,
        query: str,
        expand: bool = True,
        extract_keywords_only: bool = False
    ) -> str:
        """Rewrite query using Gemini API for better retrieval."""
        if not self.client:
            return query.strip()
        
        if extract_keywords_only:
            prompt = f"""Extract only the most important keywords from this question for search. Remove question words and particles.

Question: {query}

Return only the keywords separated by spaces, nothing else."""
        elif expand:
            prompt = f"""Rewrite this question to be more search-friendly by expanding with synonyms and related terms. Keep it concise.

Question: {query}

Return only the rewritten query, nothing else."""
        else:
            return query.strip()
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=100,
                )
            )
            
            rewritten = response.text.strip()
            return rewritten if rewritten else query
            
        except Exception as e:
            print(f"Query rewriting failed, using original: {e}")
            return query.strip()
