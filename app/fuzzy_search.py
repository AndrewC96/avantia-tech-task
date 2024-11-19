from thefuzz import fuzz
from typing import List, Dict

class FuzzySearcher:
    def __init__(self, threshold: int = 40):
        self.threshold = threshold
    
    def calculate_similarity(self, query: str, text: str) -> float:
        if not query or not text:
            return 0.0
            
        # Convert to lowercase and strip whitespace
        query = query.lower().strip()
        text = text.lower().strip()
        
        # Balanced weights
        ratio = fuzz.ratio(query, text) * 0.35
        partial = fuzz.partial_ratio(query, text) * 0.45  # Increased partial match importance
        token_sort = fuzz.token_sort_ratio(query, text) * 0.1
        token_set = fuzz.token_set_ratio(query, text) * 0.1
        
        # Calculate weighted average
        weighted_score = (ratio + partial + token_sort + token_set)
        
        # Very light length penalty
        length_ratio = (min(len(query), len(text)) / max(len(query), len(text))) * 0.8 + 0.2
        
        return (weighted_score * length_ratio) / 100.0
