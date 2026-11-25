from textblob import TextBlob
from datetime import datetime

class SourceAnalyzer:
    def __init__(self):
        pass

    def analyze_sources(self, articles):
        """
        Analyzes a list of articles to find the original source.
        Returns a dictionary with the best source and credibility details.
        """
        if not articles:
            return None

        # Sort by published date
        # Handle cases where publishedAt might be None or malformed
        valid_articles = []
        for a in articles:
            if a.get('publishedAt'):
                valid_articles.append(a)
        
        if not valid_articles:
            return None

        sorted_articles = sorted(valid_articles, key=lambda x: x['publishedAt'])
        
        original_source = sorted_articles[0]
        
        # Simple credibility algorithm:
        # 1. Being the first (earliest timestamp).
        # 2. Sentiment/Subjectivity check (optional - neutral is often better for news).
        
        analysis_result = {
            "original_article": original_source,
            "timeline": [
                {"source": a['source']['name'], "time": a['publishedAt']} for a in sorted_articles[:5]
            ],
            "confidence_score": self._calculate_confidence(original_source, sorted_articles)
        }
        
        return analysis_result

    def _calculate_confidence(self, original, all_articles):
        """
        Calculates a confidence score (0-100).
        """
        score = 50  # Base score
        
        # Boost for being significantly earlier? 
        # For now, just a placeholder logic.
        
        # Check title subjectivity
        blob = TextBlob(original.get('title', ''))
        if blob.subjectivity < 0.5:
             score += 10 # More objective = potentially more credible
        
        # If multiple sources cite similar things later, boost score
        if len(all_articles) > 3:
            score += 20
            
        return min(score, 100)
