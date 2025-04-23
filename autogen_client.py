import os
import asyncio
from dotenv import load_dotenv
from autogen_ext.tools.mcp import SseServerParams, mcp_server_tools
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient, AzureOpenAIChatCompletionClient

async def main() -> None:
    load_dotenv()
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    apikey = os.getenv("AZURE_OPENAI_API_KEY")
    model_deployment = os.getenv("AZURE_OPENAI_MODEL_DEPLOYMENT")

    # Setup server params for remote service
    server_params = SseServerParams(url="http://localhost:8000/sse")

    # Get all available tools
    tools = await mcp_server_tools(server_params)

    client = AzureOpenAIChatCompletionClient(
        azure_deployment=model_deployment,
        model="gpt-4o",
        api_key=apikey,
        api_version="2025-03-01-preview",
        azure_endpoint=endpoint,
    )

    # Create an agent with all tools
    agent = AssistantAgent(
        name="TravelAgent",
        model_client=client,
        tools=tools,
        system_message="あなたは優秀なトラベルエージェントです。ツールを使って旅行の計画を手伝ってください。",
    )
    
    # Run AssistantAgent and call the tool.
    result = await agent.run(task="おすすめの旅行先を提案して。")
    print(result.messages[-1].content)
    result = await agent.run(task="2泊3日旅行での1人1日あたり2万円使う場合の旅行予算を見積もって。")
    print(result.messages[-1].content)
    result = await agent.run(task="北海道のベストシーズンはいつ？")
    print(result.messages[-1].content)


if __name__ == "__main__":
    asyncio.run(main())