import asyncio
from typing import List
import httpx
import nltk
from newspaper import Article

from app.core.config import settings
from app.schema.news import News, NewsItem
from app.core.logger import get_logger

logger = get_logger(__name__)

nltk.download("punkt_tab", quiet=True)


class NewsService:
    def __init__(self):
        self.api_url = "https://openapi.naver.com/v1/search/news.json"
        self.client_id = settings.NAVER_CLIENT_ID
        self.client_secret = settings.NAVER_CLIENT_SECRET
        self.headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret,
        }

    async def search_news(
        self, query: str, display: int = 5, sort: str = "sim"
    ) -> List[News]:
        """
        Search Naver News for the given query.
        """
        params = {"query": query, "display": display, "sort": sort}
        logger.info(f"📰 Searching News: {query}")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.api_url, headers=self.headers, params=params
            )
            response.raise_for_status()
            data = response.json()
            items = data.get("items", [])

            news_items = []
            for item in items:
                news_items.append(News(**item))

            logger.info(f"📰 Found {len(news_items)} articles.")
            return news_items

    async def scrape_article(self, url: str) -> NewsItem:
        """
        Scrape article content using httpx (async) + newspaper4k (parsing).
        """
        logger.info(f"🧹 Scraping Article: {url}")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=2.0, follow_redirects=True)
                response.raise_for_status()
                html = response.text
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            raise e

        # Run parsing in thread to avoid blocking the loop
        return await asyncio.to_thread(self._scrape_article_sync, url, html)

    def _scrape_article_sync(self, url: str, html: str) -> NewsItem:
        """
        Internal synchronous method for parsing.
        """
        article = Article(url, fetch_images=False)
        article.download(input_html=html)
        article.parse()

        return NewsItem(
            title=article.title,
            text=article.text,
            publish_date=str(article.publish_date) if article.publish_date else None,
            authors=", ".join(article.authors),
            summary=article.summary,
        )


news_service = NewsService()
