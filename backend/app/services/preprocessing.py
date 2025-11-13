"""Data preprocessing service for Q&A dataset."""

import pandas as pd
from typing import List, Dict
import re


class PreprocessingService:
    """Service for preprocessing Q&A data from Excel files."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def load_data(self) -> pd.DataFrame:
        """Load Q&A data from Excel file."""
        df = pd.read_excel(self.file_path)
        return df
    
    def parse_qa_content(self, content: str) -> Dict[str, str]:
        """Parse Q&A content from a single cell."""
        question_match = re.search(r'Q\.\s*(.+?)(?=A\.|$)', content, re.DOTALL)
        answer_match = re.search(r'A\.\s*(.+?)$', content, re.DOTALL)
        
        question = question_match.group(1).strip() if question_match else ""
        answer = answer_match.group(1).strip() if answer_match else ""
        
        return {
            "question": question,
            "answer": answer
        }
    
    def create_chunks(self) -> List[Dict[str, any]]:
        """Create structured chunks from Q&A data."""
        df = self.load_data()
        chunks = []
        
        current_question_part = None
        chunk_counter = 1
        
        for idx, row in df.iterrows():
            content = ""
            for col in df.columns:
                val = str(row[col])
                if "Q." in val or "A." in val:
                    content = val
                    break
            
            if not content:
                continue
            
            full_text = ""

            if "Q." in content and "A." in content:
                full_text = content
                current_question_part = None
            elif "Q." in content:
                current_question_part = content
                continue
            elif "A." in content:
                if current_question_part:
                    full_text = f"{current_question_part}\n{content}"
                    current_question_part = None
                else:
                    continue
            else:
                continue
            
            qa_data = self.parse_qa_content(full_text)
            
            if not qa_data["question"] or not qa_data["answer"]:
                continue
            
            chunk = {
                "id": str(chunk_counter),
                "question": qa_data["question"],
                "answer": qa_data["answer"],
                "content": f"질문: {qa_data['question']}\n답변: {qa_data['answer']}",
                "metadata": {
                    "source": "Q&A.xlsx",
                    "row_number": int(idx + 1),
                    "category": "perso_ai"
                }
            }
            
            chunks.append(chunk)
            chunk_counter += 1
        
        return chunks
    
    def validate_chunks(self, chunks: List[Dict[str, any]]) -> bool:
        """Validate that all chunks have required fields."""
        required_fields = ["id", "question", "answer", "content", "metadata"]
        
        for chunk in chunks:
            if not all(field in chunk for field in required_fields):
                return False
            if not chunk["question"] or not chunk["answer"]:
                return False
        
        return True
