from app.schema.news import News, NewsItem
from typing import List
from langchain_core.tools import tool
from app.services.news_service import news_service


@tool
async def search_naver_news(query: str, display: int = 5) -> List[News]:
    """
    Search for Naver News articles related to the given query.
    Returns a list of articles with titles, dates, and links.
    """
    try:
        return await news_service.search_news(query, display)
    except Exception as e:
        return f"Error fetching Naver News: {str(e)}"


@tool
async def scrape_news_article(url: str) -> NewsItem:
    """
    Scrape the full content of a news article from the given URL.
    Use this to read the details of a specific news item found by 'search_naver_news'.
    """
    try:
        return await news_service.scrape_article(url)
    except Exception as e:
        return f"Error fetching article {url}: {str(e)}"
