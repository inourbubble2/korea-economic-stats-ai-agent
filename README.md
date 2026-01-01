# 🇰🇷 Korea Economic Statistics AI Agent (ECOS Agent)

An AI agent that retrieves and analyzes Bank of Korea economic statistics (ECOS). It uses LangGraph for agent orchestration and supports the Model Context Protocol (MCP).

## Key Features
- **Intelligent Search**: Semantically searches for statistics codes and items.
- **RAG Engine**: Retrieves precise data from the ECOS API.
- **MCP Server**: Provides a standard **Streamable HTTP** interface (`/mcp`) for AI IDEs (Cursor, Windsurf) and other clients.
- **Korean Formatting**: Auto-formats large currency units (e.g., 1조 원).

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
- **Core**: FastAPI, LangGraph, LangChain
- **Protocol**: Model Context Protocol (MCP) - Streamable HTTP
- **Infra**: Google Cloud Run, Docker

## 🔌 MCP Configuration
To connect from an MCP Client (like Cursor):
- **Type**: Streamable HTTP
- **URL**: `http://localhost:8000/mcp`
