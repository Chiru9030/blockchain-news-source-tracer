from datetime import datetime

try:
    from textblob import TextBlob
except ImportError:
    TextBlob = None

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
        valid_articles = [a for a in articles if a.get('publishedAt')]
        if not valid_articles:
            return None

        sorted_articles = sorted(valid_articles, key=lambda x: x['publishedAt'])
        original_source = sorted_articles[0]

        analysis_result = {
            "original_article": original_source,
            "timeline": [
                {
                    "source": a.get('source', {}).get('name', 'Unknown Source'),
                    "title": a.get('title', 'Untitled'),
                    "time": a.get('publishedAt'),
                    "url": a.get('url', '#')
                } for a in sorted_articles
            ],
            "confidence_score": self._calculate_confidence(original_source, sorted_articles)
        }

        return analysis_result

    def _calculate_confidence(self, original, all_articles):
        """
        Calculates an objective provenance confidence score (0-100).
        """
        score = 65  # Base confidence for chronological precedence

        title = original.get('title', '')
        if TextBlob:
            try:
                blob = TextBlob(title)
                if blob.sentiment.subjectivity < 0.5:
                    score += 15  # Objective reporting tone bonus
                else:
                    score -= 5
            except Exception:
                pass
        else:
            # High-fidelity fallback heuristic for tone
            sensational_words = {'shocking', 'unbelievable', 'secret', 'miracle', 'revealed', 'insane', 'destroy'}
            words = set(title.lower().split())
            if not words.intersection(sensational_words):
                score += 15

        # Citation & corroboration multiplier
        if len(all_articles) >= 3:
            score += 15
        elif len(all_articles) >= 2:
            score += 10

        return min(max(score, 30), 99)
