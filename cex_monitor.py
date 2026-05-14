"""
cex_monitor.py
通过币安 WebSocket 实时订阅主流币价格
"""
import asyncio
import json
import websockets
from config import BINANCE_WSS, SYMBOLS


class CEXMonitor:
    def __init__(self, price_store: dict):
        """
        price_store: 共享字典，格式 {"BTCUSDT": 68000.0, ...}
        """
        self.price_store = price_store
        self.running = False

    def _build_url(self):
        streams = "/".join(f"{s.lower()}@miniTicker" for s in SYMBOLS)
        return f"{BINANCE_WSS}?streams={streams}"

    async def start(self):
        self.running = True
        url = self._build_url()
        print(f"[CEX] 连接币安 WSS: {url}")
        while self.running:
            try:
                async with websockets.connect(url, ping_interval=20) as ws:
                    print("[CEX] 连接成功，开始接收价格...")
                    async for message in ws:
                        data = json.loads(message)
                        ticker = data.get("data", {})
                        symbol = ticker.get("s")
                        price  = ticker.get("c")
                        if symbol and price:
                            self.price_store[symbol] = float(price)
            except Exception as e:
                print(f"[CEX] 连接断开: {e}，3秒后重连...")
                await asyncio.sleep(3)

    def stop(self):
        self.running = False
