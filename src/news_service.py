import os
import requests
from dotenv import load_dotenv

load_dotenv()

class NewsService:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2"

    def find_related_articles(self, query):
        """
        Finds articles related to a topic or headline.
        """
        if not self.api_key:
            print("Warning: No NewsAPI key provided. Receiving mock data.")
            return self._get_mock_data()

        url = f"{self.base_url}/everything"
        params = {
            "q": query,
            "sortBy": "publishedAt",
            "language": "en",
            "apiKey": self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("articles", [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news: {e}")
            return self._get_mock_data()

    def _get_mock_data(self):
        return [
            {
                "source": {"name": "Mock Source 1"},
                "author": "Alice",
                "title": "Breaking: AI Solves Everything",
                "description": "Artificial Intelligence has solved all world problems...",
                "url": "http://mock1.com",
                "publishedAt": "2023-10-27T10:00:00Z",
                "content": "Full content of the article..."
            },
            {
                "source": {"name": "Mock Source 2 - The Original"},
                "author": "Bob",
                "title": "AI Solves Everything",
                "description": "Early reports suggest AI is doing great.",
                "url": "http://mock2.com",
                "publishedAt": "2023-10-26T09:00:00Z",
                "content": "Initial findings..."
            }
        ]
