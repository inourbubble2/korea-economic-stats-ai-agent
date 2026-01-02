from typing import List, Dict, Any
import requests
from newspaper import Article
from app.core.config import settings
from app.schema.news import NewsItem


class NewsService:
    def __init__(self):
        self.api_url = "https://openapi.naver.com/v1/search/news.json"
        self.client_id = settings.NAVER_CLIENT_ID
        self.client_secret = settings.NAVER_CLIENT_SECRET
        self.headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret,
        }

    def search_news(
        self, query: str, display: int = 5, sort: str = "sim"
    ) -> List[NewsItem]:
        """
        Search Naver News for the given query.
        """
        params = {"query": query, "display": display, "sort": sort}

        response = requests.get(self.api_url, headers=self.headers, params=params)
        response.raise_for_status()
        data = response.json()
        items = data.get("items", [])

        news_items = []
        for item in items:
            news_items.append(NewsItem(**item))

        return news_items

    def scrape_article(self, url: str) -> Dict[str, str]:
        """
        Scrape article content using newspaper4k.
        """
        article = Article(url)
        article.download()
        article.parse()

        return {
            "title": article.title,
            "text": article.text,
            "publish_date": str(article.publish_date) if article.publish_date else None,
            "authors": ", ".join(article.authors),
            "summary": article.summary,
        }


news_service = NewsService()
