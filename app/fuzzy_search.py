from thefuzz import fuzz
from typing import List, Dict
from config import FUZZY_SEARCH_THRESHOLD

class FuzzySearcher:
    def __init__(self):
        self.threshold = FUZZY_SEARCH_THRESHOLD
    
    def calculate_similarity(self, query: str, text: str) -> float:
        if not query or not text:
            return 0.0
            
        # Convert to lowercase and strip whitespace
        query = query.lower().strip()
        text = text.lower().strip()
        
        # Split names into parts
        query_parts = query.split()
        text_parts = text.split()
        
        # Check for exact full name match first
        if query == text:
            return 1.0
        
        # For partial queries, check if all parts match exactly
        if all(q_part in text_parts for q_part in query_parts):
            return 1.0
        
        # Calculate best match score for each query part
        part_scores = []
        for q_part in query_parts:
            best_part_score = 0
            for t_part in text_parts:
                ratio = fuzz.ratio(q_part, t_part) * 0.4
                partial = fuzz.partial_ratio(q_part, t_part) * 0.6
                score = (ratio + partial) / 100.0
                best_part_score = max(best_part_score, score)
            part_scores.append(best_part_score)
        
        return sum(part_scores) / len(part_scores) if part_scores else 0.0
