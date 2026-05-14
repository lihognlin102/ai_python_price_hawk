"""
main.py
主入口：启动 CEX/DEX 监控 + 套利引擎 + HTTP API
"""
import asyncio
import uvicorn
import api
from cex_monitor import CEXMonitor
from dex_monitor import DEXMonitor
from arbitrage import ArbitrageEngine
from notifier import send_alert

# 共享数据存储
price_store: dict = {}
opportunity_store: list = []

# 注入到 API 模块
api.price_store = price_store
api.opportunity_store = opportunity_store


async def main():
    # 初始化各模块
    cex = CEXMonitor(price_store)
    dex = DEXMonitor(price_store, interval=12)
    arb = ArbitrageEngine(price_store, opportunity_store, interval=5)

    # 注册邮件报警（每次发现套利机会时触发）
    arb.add_alert_callback(send_alert)

    # 启动 FastAPI（非阻塞）
    config = uvicorn.Config(api.app, host="0.0.0.0", port=8000, log_level="warning")
    server = uvicorn.Server(config)

    print("🦅 Price Hawk 启动中...")
    print("   API 地址: http://0.0.0.0:8000")
    print("   监控: 币安 WSS + Uniswap V3")

    await asyncio.gather(
        cex.start(),
        dex.start(),
        arb.start(),
        server.serve(),
    )


if __name__ == "__main__":
    asyncio.run(main())
