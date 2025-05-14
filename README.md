## How to setup
- Install Python
- Install UV
- Clone this repo
- Authenticate to AWS
- Set AWS_RTEGION
- Cd to the project folder, and run
```bash
uv init
uv sync
uv run litellm-bedrock-mcp-test.py
```

## How to run agent 
- Run
```bash
uv run agent.py
```
- Go to http://localhost:7234/home
- Enter question
- Hit submit
- Verify the answer


## Files
- agent.py = API server. It uses mcp_agent.py to process questions. 
- index.html = HTML interface (chatbot UI)
- litellm-bedrock-mcp-test.py = Quick standalone test if bedrock is reponding
- mcp_agent.py = Uses Bedrock via LiteLLM and communicates to the mcp_server.py
- mcp_server.py = Exposes tools  
- pyproject.toml = Contains the project dependencies