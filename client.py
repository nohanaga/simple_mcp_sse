import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    # MCP SSE サーバーの URL を指定
    server_url = "http://localhost:8000/sse"

    # SSE クライアントを作成して接続
    async with sse_client(server_url) as (read, write):
        async with ClientSession(read, write) as session:
            # セッションを初期化
            await session.initialize()

            # 利用可能なツールを取得
            tools = await session.list_tools()
            print("利用可能なツール:", [tool.name for tool in tools.tools])

            # おすすめの旅行先を提案するツールを呼び出す
            result = await session.call_tool("suggest_onsen_destination")

            # 結果を表示
            print(f"おすすめの旅行先は{result.content[0].text}です。")

            # おすすめの旅行先を提案するツールを呼び出す
            result = await session.call_tool("estimate_travel_budget",{ "days":3, "people":2, "per_day_per_person":15000})

            # 結果を表示
            print(f"旅行予算は{result.content[0].text}円です。")

            # 観光地のベストシーズンをチェックするツールを呼び出す
            result = await session.call_tool("check_best_season", {"destination":"北海道"})
            # 結果を表示
            print(f"北海道のベストシーズンは{result.content[0].text}です。")


# 非同期関数を実行
if __name__ == "__main__":
    asyncio.run(main())
