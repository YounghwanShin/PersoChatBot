"""
Data preprocessing service for Q&A dataset.

This module handles loading Excel data and converting it into
structured chunks for vector storage.
"""

import pandas as pd
from typing import List, Dict
import re


class PreprocessingService:
    """Service for preprocessing Q&A data from Excel files."""
    
    def __init__(self, file_path: str):
        """
        Initialize preprocessing service.
        
        Args:
            file_path: Path to the Excel file containing Q&A data
        """
        self.file_path = file_path
    
    def load_data(self) -> pd.DataFrame:
        """
        Load Q&A data from Excel file.
        
        Returns:
            DataFrame containing the Q&A data
        """
        df = pd.read_excel(self.file_path)
        return df
    
    def parse_qa_content(self, content: str) -> Dict[str, str]:
        """
        Parse Q&A content from a single cell.
        
        Expected format:
        "Q. 질문내용
         A. 답변내용"
        
        Args:
            content: Raw content string from Excel cell
            
        Returns:
            Dictionary with 'question' and 'answer' keys
        """
        # Split by Q. and A. patterns
        question_match = re.search(r'Q\.\s*(.+?)(?=A\.|$)', content, re.DOTALL)
        answer_match = re.search(r'A\.\s*(.+?)$', content, re.DOTALL)
        
        question = question_match.group(1).strip() if question_match else ""
        answer = answer_match.group(1).strip() if answer_match else ""
        
        return {
            "question": question,
            "answer": answer
        }
    
    def create_chunks(self) -> List[Dict[str, any]]:
        """
        Create structured chunks from Q&A data.
        
        Each chunk contains:
        - question: The question text
        - answer: The answer text
        - metadata: Additional information (id, category, etc.)
        
        Returns:
            List of chunk dictionaries
        """
        df = self.load_data()
        chunks = []
        
        # Variable to handle split rows (due to merged cells)
        current_question_part = None
        chunk_counter = 1
        
        for idx, row in df.iterrows():
            # Find the cell containing the content (ignoring specific column names)
            content = ""
            for col in df.columns:
                val = str(row[col])
                if "Q." in val or "A." in val:
                    content = val
                    break
            
            if not content:
                continue
            
            full_text = ""

            # Case 1: Single cell containing both Question and Answer
            if "Q." in content and "A." in content:
                full_text = content
                current_question_part = None  # Reset state if mixed

            # Case 2: Row contains only the Question (start of merged cell)
            elif "Q." in content:
                current_question_part = content
                continue  # Wait for the next row (Answer)
            
            # Case 3: Row contains only the Answer (end of merged cell)
            elif "A." in content:
                if current_question_part:
                    # Combine previous question part with current answer part
                    full_text = f"{current_question_part}\n{content}"
                    current_question_part = None  # Reset state
                else:
                    continue
            else:
                continue
            
            # Parse Q&A
            qa_data = self.parse_qa_content(full_text)
            
            if not qa_data["question"] or not qa_data["answer"]:
                continue
            
            # Create chunk
            chunk = {
                "id": str(chunk_counter),
                "question": qa_data["question"],
                "answer": qa_data["answer"],
                # Combine Q&A for embedding
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
        """
        Validate that all chunks have required fields.
        
        Args:
            chunks: List of chunk dictionaries
            
        Returns:
            True if all chunks are valid, False otherwise
        """
        required_fields = ["id", "question", "answer", "content", "metadata"]
        
        for chunk in chunks:
            if not all(field in chunk for field in required_fields):
                return False
            if not chunk["question"] or not chunk["answer"]:
                return False
        
        return True