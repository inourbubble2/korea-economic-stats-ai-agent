from app.schema.news import NewsItem
from typing import List, Dict
from langchain_core.tools import tool
from app.services.news_service import news_service


@tool
def search_naver_news(query: str, display: int = 5) -> List[NewsItem]:
    """
    Search for Naver News articles related to the given query.
    Returns a list of articles with titles, dates, and links.
    """
    items = news_service.search_news(query, display)
    return items


@tool
def scrape_news_article(url: str) -> Dict[str, str]:
    """
    Scrape the full content of a news article from the given URL.
    Use this to read the details of a specific news item found by 'search_naver_news'.
    """
    article = news_service.scrape_article(url)
    return article
