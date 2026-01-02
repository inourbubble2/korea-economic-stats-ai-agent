from pydantic import BaseModel, Field


class NewsItem(BaseModel):
    title: str = Field(description="Title of the news article")
    original_link: str = Field(
        alias="originallink", description="Original link to the article"
    )
    link: str = Field(description="Naver news link or platform link")
    description: str = Field(description="Description or summary of the article")
    pub_date: str = Field(alias="pubDate", description="Publication date string")

    class Config:
        populate_by_name = True
