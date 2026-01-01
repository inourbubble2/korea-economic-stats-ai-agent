import asyncio
import httpx
import json


async def verify_mcp_connection():
    base_url = "http://localhost:8000"

    print(f"Testing MCP SSE endpoint at {base_url}/sse ...")

    print(f"Testing MCP endpoint via POST at {base_url}/mcp ...")
    async with httpx.AsyncClient() as client:
        try:
            # JSON-RPC Initialize Payload
            payload = {
                "jsonrpc": "2.0",
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "test-client", "version": "1.0"},
                },
                "id": 1,
            }

            # Send POST with JSON body and required Accept headers
            response = await client.post(
                f"{base_url}/mcp",
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream",
                },
            )

            print(f"Response Status: {response.status_code}")
            print(f"Response Content: {response.text}")

            if response.status_code == 200:
                print("Connected to MCP via POST and received response!")
            else:
                print(f"Failed to connect via POST. Status: {response.status_code}")

        except Exception as e:
            print(f"POST request failed with exception: {e}")


if __name__ == "__main__":
    asyncio.run(verify_mcp_connection())
