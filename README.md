

## Setup for dev
uv init
uv add fastmcp
uv add fastapi
uv add langchain_mcp_adapters
uv add langgraph
uv add langchain
uv add litellm
uv add boto3
uv add langchain_community
uv add langchain_litellm


pip install -U langchain-openai


## Run server
uv run mcp-server.py 