"""
arbitrage.py
计算 CEX vs DEX 价差，发现套利机会
"""
import asyncio
from datetime import datetime
from config import ARBITRAGE_THRESHOLD, SYMBOLS, UNISWAP_POOLS


class ArbitrageEngine:
    def __init__(self, price_store: dict, opportunity_store: list, interval: int = 5):
        """
        price_store:      共享价格字典
        opportunity_store: 套利机会列表（最新100条）
        interval:         检查间隔秒数
        """
        self.price_store = price_store
        self.opportunity_store = opportunity_store
        self.interval = interval
        self.running = False
        self.alert_callbacks = []

    def add_alert_callback(self, cb):
        """注册报警回调函数"""
        self.alert_callbacks.append(cb)

    def _check(self):
        opportunities = []
        for symbol in SYMBOLS:
            if UNISWAP_POOLS.get(symbol) is None:
                continue
            cex_price = self.price_store.get(symbol)
            dex_price = self.price_store.get(f"{symbol}_DEX")
            if not cex_price or not dex_price:
                continue

            diff = cex_price - dex_price
            diff_pct = abs(diff) / cex_price * 100

            if diff_pct >= ARBITRAGE_THRESHOLD:
                direction = "买DEX卖CEX" if diff > 0 else "买CEX卖DEX"
                opp = {
                    "time":      datetime.now().strftime("%H:%M:%S"),
                    "symbol":    symbol,
                    "cex_price": cex_price,
                    "dex_price": dex_price,
                    "diff_pct":  round(diff_pct, 4),
                    "direction": direction,
                }
                opportunities.append(opp)
                print(f"[套利] ⚡ {symbol} 差价 {diff_pct:.3f}% | {direction} | CEX={cex_price} DEX={dex_price}")

        return opportunities

    async def start(self):
        self.running = True
        print(f"[套利] 引擎启动，阈值 {ARBITRAGE_THRESHOLD}%，检查间隔 {self.interval}s")
        while self.running:
            opps = self._check()
            for opp in opps:
                # 插入到列表头部，保留最新100条
                self.opportunity_store.insert(0, opp)
                if len(self.opportunity_store) > 100:
                    self.opportunity_store.pop()
                # 触发报警回调
                for cb in self.alert_callbacks:
                    await cb(opp)
            await asyncio.sleep(self.interval)

    def stop(self):
        self.running = False
