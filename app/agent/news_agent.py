from datetime import datetime

from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, dynamic_prompt
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver

from app.agent.tools_news import search_naver_news, scrape_news_article
from app.core.config import settings


@dynamic_prompt
def news_system_prompt(request: ModelRequest) -> str:
    today = datetime.now().strftime("%Y%m%d")
    return f"""You are an Economic News Analysis Agent. today is {today}.

Goal: Answer the user's economic question by finding and analyzing real news articles.

Workflow:
1. **Search**: Use `search_naver_news` to find relevant articles. 
   - Keywords: Extract key economic terms from the user query.
2. **Select & Scrape**: Look at the titles and dates. Select 1-3 most relevant and recent articles.
   - Use `scrape_news_article` to get the full content of these selected articles.
   - Do NOT scrape everything. Be selective.
3. **Analyze & Answer**:
   - Synthesize the information from the scraped articles.
   - **MANDATORY**: When answering, you MUST cite the source.
   - **Format**: Append a "[References]" section at the end of your response listing the articles used with their Titles and Links.
     Example:
     [References]
     1. Article Title (https://link.com)
     2. Another Title (https://link.com)
   - If user asks about specific numbers (e.g. "Current Exchange Rate"), rely on the LATEST news.
   - If no news is found, admit it.

User Query Context:
The user is asking about Korean/Global economy.
"""


llm = ChatOpenAI(model=settings.CHAT_MODEL, api_key=settings.OPENAI_API_KEY)
tools = [search_naver_news, scrape_news_article]

news_agent = create_agent(
    model=llm,
    tools=tools,
    middleware=[news_system_prompt],
    checkpointer=MemorySaver(),
)
