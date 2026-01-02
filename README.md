# 🇰🇷 Korea Economy Agent
AI Agents that retrieves Bank of Korea economic statistics (ECOS) and analyzes real-time economic news. 
It uses LangGraph for agent orchestrating and supports the Model Context Protocol (MCP) & The Agent–User Interaction (AG-UI) Protocol.

## Key Features
- **Macro Analysis**: Retrieval of official Bank of Korea statistics (ECOS Agent).
- **News Insight**: Real-time searching and scraping of Naver News (News Agent).

## Quick Start

### Prerequisites
- Python 3.12+
- `uv` package manager

### Local Development
1. **Install dependencies**
   ```bash
   uv sync
   ```
2. **Run Server**
   ```bash
   uv run uvicorn app.main:app --reload
   ```
   - API Docs: `http://localhost:8000/docs`
   - MCP Endpoint: `http://localhost:8000/mcp`

## 🛠 Tech Stack
- **Core**: FastAPI, LangGraph, LangChain, newspaper4k
- **Protocol**: Model Context Protocol (MCP) - Streamable HTTP
- **Infra**: Google Cloud Run, Docker

## 🌐 AG UI & LangGraph Endpoints
This agent exposes endpoints for **AG-UI**.

- **ECOS Agent**: `http://localhost:8000/ecos`
- **News Agent**: `http://localhost:8000/news`

## 📨 MCP Configuration
To connect from an MCP Client (like Cursor):
- **Type**: Streamable HTTP
- **URL**: `http://localhost:8000/mcp`
