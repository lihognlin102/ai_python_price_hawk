"""
api.py
提供 HTTP 接口给前端调用
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Price Hawk API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 由 main.py 注入
price_store: dict = {}
opportunity_store: list = []


@app.get("/api/prices")
def get_prices():
    """返回所有实时价格"""
    result = {}
    for k, v in price_store.items():
        result[k] = round(v, 4)
    return {"success": True, "data": result}


@app.get("/api/arbitrage")
def get_arbitrage():
    """返回最新套利机会列表"""
    return {"success": True, "data": opportunity_store[:20]}


@app.get("/api/status")
def get_status():
    """服务健康检查"""
    return {
        "success": True,
        "status": "running",
        "tracked_symbols": list(price_store.keys()),
    }
