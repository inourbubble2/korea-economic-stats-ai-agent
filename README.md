# 🇰🇷 Korea Economic Statistics AI Agent (ECOS Agent)

This project is an AI-powered agent specialized in retrieving and analyzing Korean economic statistics using the Bank of Korea's ECOS API. It leverages LangChain and OpenAI to understand natural language queries, search for relevant statistics, and fetch precise time-series data.

## Key Features

- **Intelligent Search**: Uses semantic search (Vector Embeddings) to find the right statistics even if the user's query doesn't match the exact official name.
- **Smart Metadata Discovery**: Automatically inspects statistic sub-items (e.g., distinguishing "Total GDP" from "Agriculture GDP") to ensure data accuracy.
- **Context-Aware Retrieval**: Dynamically adjusts the query date range based on data availability (e.g., if data ends in 2023, it won't fail trying to fetch 2025).
- **Korean-Friendly Formatting**: Automatically converts large numbers (e.g., `1,000,000 백만원`) into readable Korean units (`1조 원`).
- **Streaming API**: Supports real-time streaming of agent thought processes and answers via Server-Sent Events (SSE).

## Tech Stack

- **Framework**: FastAPI
- **AI/LLM**: LangChain, LangGraph, OpenAI (GPT-4o/mini)
- **Vector Store**: In-Memory (using `numpy` & `pickle` for lightweight local persistence)
- **Data Source**: Bank of Korea ECOS API
- **HTTP Client**: `httpx` (Async)

### Running the Server

```bash
uvicorn app.main:create_app --factory --reload
```
The API will be available at `http://localhost:8000`.
- **Docs**: `http://localhost:8000/docs`

## 🧠 How It Works

1. **Search**: The user's query is converted to a vector and matched against `ecos_statistics.csv` to find the relevant `StatCode`.
2. **Item Inspection**: The agent calls `get_statistic_item_list` to see valid sub-items and **data availability range** (Start/End Time).
3. **Data Fetch**: Using the `StatCode` and specific `ItemCode`, the agent fetches the time-series data via `get_statistic_data` from ECOS.
4. **Analysis & Format**: The agent analyzes the data, formats numbers into "Jo/Euk" units, and generates a natural language response.
