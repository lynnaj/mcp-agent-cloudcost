# nova_agent.py
from litellm import litellm, completion
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import asyncio
# from langchain_community.chat_models import ChatLiteLLM
from langchain_litellm import ChatLiteLLM

# import os
# os.environ["LANGSMITH_TRACING"] = "true"

class MCPAgent:
    def __init__(self):
        self.model_name = "bedrock/amazon.nova-pro-v1:0"
        self.llm = ChatLiteLLM(model=self.model_name)
        self.client = None
        self.agent = None


    async def make_agent(self):
        async with MultiServerMCPClient(
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
        ) as client:
            tools = client.get_tools()
            print("*** Found tools:")
            print(tools)
            self.agent = create_react_agent(
                model=self.llm,
                tools=tools
            )        
            print("*** Agent created")



    async def initialize(self):
        print("*** Initializing")
        self.client = MultiServerMCPClient(
            {
                "agent1": {
                    "command": "python",
                    "args": ["mcp_server.py"],
                    "transport": "stdio",
                }
            }
        )
        tools = self.client.get_tools()

        print("*** Found tools:")
        print(tools)
        print("*** LLM")
        print(self.llm)

        self.agent = create_react_agent(
            model=self.llm,
            tools=tools
        )
        print("*** Agent created")


    async def question(self, message):
        # test_response = await self.agent.ainvoke(
        #     {"messages": [{"role": "user", "content": message}]}
        # )

        test_response = await self.agent.ainvoke(
            {"messages": [{"role": "user", "content": message}]}
        )

        return test_response


    async def XXquestion(self, message):
        if self.client is None or self.agent is None:
            await self.initialize()

        test_response = await self.agent.ainvoke(
            {"messages": [{"role": "user", "content": message}]}
        )
        last_message = test_response['messages'][-1]
        return last_message