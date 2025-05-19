from litellm import litellm, completion
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import asyncio
from langchain_litellm import ChatLiteLLM

class MCPAgent:
    def __init__(self):
        self.model_name = "bedrock/amazon.nova-pro-v1:0"
        self.llm = ChatLiteLLM(model=self.model_name)
        self.client = None
        self.agent = None

    async def initialize(self):
        self.client = MultiServerMCPClient(
            {
                "agent1": {
                    "command": "python",
                    "args": ["mcp_server.py"],
                    "transport": "stdio",
                }
                # ,
                # "agent2": {
                #     "url": "http://localhost:8000/sse",
                #     "transport": "sse",
                # }
            }
        ) 
        # print(self.client)
        await self.client.__aenter__()
        print("*** Getting tools:")
        tools = self.client.get_tools()
        print("*** Found tools:")
        print(tools)
        self.agent = create_react_agent(
            model=self.llm,
            tools=tools
        )        
        print("*** Agent created")

    async def cleanup(self):
        if self.client:
                await self.client.__aexit__(None, None, None)


    async def question(self, message):
        test_response = await self.agent.ainvoke(
            {"messages": [{"role": "user", "content": message}]}
        )

        return test_response

