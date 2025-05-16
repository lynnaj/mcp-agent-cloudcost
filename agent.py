from typing import Union
import asyncio
from fastapi import FastAPI
from starlette.responses import FileResponse 
from mcp_agent import MCPAgent

app = FastAPI()

# Create a single instance of MCPAgent
agent = MCPAgent()

# Background task to initialize the agent
async def initialize_agent():
    await agent.initialize()

# Startup event to initialize the agent
@app.on_event("startup")
async def startup_event():
    await initialize_agent()

@app.on_event("shutdown")
async def shutdown_event():
    await agent.cleanup()


@app.get("/home")
async def index():
    print("Home route called")
    return FileResponse('index.html')

@app.get("/q/{question}")
async def q(question):
    print(f"Asking: {question}")
    # question = "How much is (3 + 7) * 9?"
    # question = "Get foo value"
    response = await agent.question(question)
    return response

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("agent:app", host="127.0.0.1", port=7236, log_level="info", reload=False)