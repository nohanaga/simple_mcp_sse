from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI
import random
from pydantic import Field
# MCP サーバーのインスタンスを作成
mcp = FastMCP("Travel Agent")

# Tool 1: おすすめの旅行先を提案
@mcp.tool()
def suggest_onsen_destination() -> str:
    """
    おすすめの温泉地をランダムに提案します。
    """
    destinations = [
        "草津温泉（群馬県）",
        "下呂温泉（岐阜県）",
        "道後温泉（愛媛県）",
        "別府温泉（大分県）",
        "有馬温泉（兵庫県）",
        "黒川温泉（熊本県）",
        "城崎温泉（兵庫県）",
        "銀山温泉（山形県）",
        "熱海温泉（静岡県）",
        "登別温泉（北海道）"
    ]
    choice = random.choice(destinations)
    print(f"おすすめの温泉： {choice}")
    return choice

# Tool 2: 旅行予算の見積もり
@mcp.tool()
def estimate_travel_budget(
    days: int = Field(..., description="旅行の日数（例：3）"),
    people: int = Field(..., description="旅行者の人数（例：2）"),
    per_day_per_person: int = Field(15000, description="1人1日あたりの予算（円、デフォルトは15,000円）")
) -> int:
    """人数と日数から旅行の予算を見積もります。"""
    budget = days * people * per_day_per_person
    print(f"Estimating budget: {days}日 x {people}人 x {per_day_per_person}円 = {budget}円")
    return budget

# Tool 3: 観光地のベストシーズンをチェック
@mcp.tool()
def check_best_season(
    destination: str = Field(..., description="観光地の名前（例：北海道、京都、沖縄など）")
) -> str:
    """指定された観光地のベストシーズンを返します。"""
    seasons = {
        "北海道": "6月〜8月（夏）",
        "京都": "4月（桜）・11月（紅葉）",
        "沖縄": "5月〜10月（海）",
        "金沢": "3月（雪解け）・10月（文化祭）",
    }
    best = seasons.get(destination, "ベストシーズン情報は見つかりませんでした。")
    print(f"{destination} のベストシーズン: {best}")
    return best

# FastAPI アプリケーションを作成し、MCP の SSE エンドポイントをマウント
app = FastAPI()
app.mount("/", mcp.sse_app())

# サーバーを起動するには、以下のコマンドを実行してください:
# uvicorn server:app --host 127.0.0.1 --port 8000
