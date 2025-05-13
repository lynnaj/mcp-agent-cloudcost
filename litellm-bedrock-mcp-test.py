from litellm import litellm, completion
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import asyncio
# from langchain_community.chat_models import ChatLiteLLM
from langchain_litellm import ChatLiteLLM

litellm._turn_on_debug()

model_name = "bedrock/amazon.nova-pro-v1:0"
llm = ChatLiteLLM(model=model_name)

async def main():
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
        # model_name = "amazon.nova-pro-v1:0 (Served via LiteLLM)"
        tools = client.get_tools()
        print("*** Found tools:")
        print(tools)
        agent = create_react_agent(
            model=llm,
            tools=tools
        )        

        # question = "Greet Kaushik"
        # question = "How much is (3 + 7) * 9"
        question = "Get foo value"

        test_response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": question}]}
        )
        # print(test_response)

        last_message = test_response['messages'][-1]

        print("===========")
        print(last_message.content)        

# Run the main function
asyncio.run(main())