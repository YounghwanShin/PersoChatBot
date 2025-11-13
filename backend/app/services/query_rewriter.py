"""Query rewriting service for better retrieval."""

import re
from typing import List


class QueryRewriterService:
    """Service for rewriting user queries for better retrieval."""
    
    def __init__(self):
        self.question_patterns = [
            r"(.+?)이?가?\s*무엇",
            r"(.+?)이?가?\s*뭐",
            r"(.+?)(은|는)\s*어떻게",
            r"(.+?)(은|는)\s*어디",
            r"(.+?)(은|는)\s*누구",
            r"(.+?)(을|를)\s*어떻게",
        ]
    
    def expand_query(self, query: str) -> str:
        """Expand query with synonyms and related terms."""
        synonyms = {
            "서비스": ["플랫폼", "솔루션", "프로그램"],
            "기능": ["특징", "능력"],
            "사용": ["이용", "활용"],
            "가격": ["요금", "비용", "가격"],
            "회원가입": ["가입", "등록"],
        }
        
        expanded_terms = []
        for word, related in synonyms.items():
            if word in query:
                expanded_terms.extend(related)
        
        if expanded_terms:
            return f"{query} {' '.join(expanded_terms[:2])}"
        
        return query
    
    def extract_keywords(self, query: str) -> List[str]:
        """Extract key terms from query."""
        stop_words = [
            "무엇", "뭐", "어떻게", "어디", "누구", "언제", "왜",
            "인가요", "인지", "이에요", "예요", "가요",
            "은", "는", "이", "가", "을", "를"
        ]
        
        tokens = query.split()
        keywords = [
            token for token in tokens
            if not any(stop in token for stop in stop_words)
        ]
        
        return keywords
    
    def rewrite_as_statement(self, query: str) -> str:
        """Convert question into a statement form."""
        query = query.replace("?", "")
        
        conversions = {
            r"(.+?)(은|는|이|가)\s*무엇인가요": r"\1",
            r"(.+?)(을|를)\s*어떻게\s*(.+)": r"\1 \3",
            r"(.+?)(은|는)\s*어디": r"\1 위치",
        }
        
        for pattern, replacement in conversions.items():
            query = re.sub(pattern, replacement, query)
        
        return query.strip()
    
    def rewrite_query(
        self,
        query: str,
        expand: bool = True,
        extract_keywords_only: bool = False
    ) -> str:
        """Main query rewriting function."""
        query = query.strip()
        
        if extract_keywords_only:
            keywords = self.extract_keywords(query)
            return " ".join(keywords)
        
        if expand:
            query = self.expand_query(query)
        
        return query
    
    def generate_multiple_variants(self, query: str) -> List[str]:
        """Generate multiple query variants for ensemble retrieval."""
        variants = [
            query,
            self.rewrite_query(query, expand=True),
            self.rewrite_query(query, extract_keywords_only=True),
            self.rewrite_as_statement(query),
        ]
        
        seen = set()
        unique_variants = []
        for variant in variants:
            if variant not in seen:
                seen.add(variant)
                unique_variants.append(variant)
        
        return unique_variants
