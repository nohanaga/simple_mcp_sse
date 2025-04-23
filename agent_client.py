import os
import asyncio
from dotenv import load_dotenv
from typing import Any
from openai import AsyncAzureOpenAI
from agents import Agent, Runner, gen_trace_id, trace, set_default_openai_client
from agents import OpenAIChatCompletionsModel, set_tracing_disabled, set_tracing_export_api_key
from agents.mcp import MCPServer, MCPServerSse
from agents.model_settings import ModelSettings

# 環境変数と接続設定の読み込み
load_dotenv()

# Azure OpenAIのAPIキーとエンドポイントを環境変数から取得
api_version = "2025-03-01-preview"
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
apikey = os.getenv("AZURE_OPENAI_API_KEY")
model_deployment = os.getenv("AZURE_OPENAI_MODEL_DEPLOYMENT")

openai_client = AsyncAzureOpenAI(
    api_key=apikey,
    api_version=api_version,
    azure_endpoint=endpoint,
)
# Set the default OpenAI client for the Agents SDK
set_default_openai_client(openai_client, use_for_tracing=False)
set_tracing_disabled(disabled=True) # Azure OpenAI 401 Error 回避
#set_tracing_export_api_key("") # もし使用する場合「OpenAIのAPIキー」が必要

async def run(mcp_server: MCPServer):

    agent = Agent(
        name="TravelAgent",
        instructions="あなたは優秀なトラベルエージェントです。ツールを使って旅行の計画を手伝ってください。",
        mcp_servers=[mcp_server],
        model=OpenAIChatCompletionsModel( 
            model=model_deployment,
            openai_client=openai_client
        )
        #model_settings=ModelSettings(tool_choice="required"),
    )

    # Run the `get_secret_word` tool
    message = "おすすめの旅行先を提案して。"
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

    message = "2泊3日旅行での1人1日あたり2万円使う場合の旅行予算を見積もって。"
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

    message = "北海道のベストシーズンはいつ？"
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

async def main():
    async with MCPServerSse(
        name="SSE Python Server",
        params={
            "url": "http://localhost:8000/sse",
        },
    ) as server:
        await run(server)


if __name__ == "__main__":
    asyncio.run(main())