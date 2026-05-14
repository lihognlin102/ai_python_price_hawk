"""
dex_monitor.py
通过以太坊公共 RPC 轮询 Uniswap V3 池子价格
"""
import asyncio
import math
from web3 import Web3
from config import ETH_RPC_URL, UNISWAP_POOLS

# Uniswap V3 Pool ABI（只需要 slot0）
POOL_ABI = [
    {
        "inputs": [],
        "name": "slot0",
        "outputs": [
            {"internalType": "uint160", "name": "sqrtPriceX96", "type": "uint160"},
            {"internalType": "int24",   "name": "tick",          "type": "int24"},
            {"internalType": "uint16",  "name": "observationIndex",             "type": "uint16"},
            {"internalType": "uint16",  "name": "observationCardinality",       "type": "uint16"},
            {"internalType": "uint16",  "name": "observationCardinalityNext",   "type": "uint16"},
            {"internalType": "uint8",   "name": "feeProtocol", "type": "uint8"},
            {"internalType": "bool",    "name": "unlocked",    "type": "bool"},
        ],
        "stateMutability": "view",
        "type": "function",
    }
]

# 各池子 token0/token1 精度配置
POOL_DECIMALS = {
    "ETHUSDT":   {"token0_dec": 6,  "token1_dec": 18, "invert": True},   # USDC/ETH → invert
    "BTCUSDT":   {"token0_dec": 8,  "token1_dec": 6,  "invert": False},  # WBTC/USDC
    "MATICUSDT": {"token0_dec": 18, "token1_dec": 6,  "invert": True},   # MATIC/USDC → invert
}


def sqrt_price_to_price(sqrt_price_x96: int, token0_dec: int, token1_dec: int, invert: bool) -> float:
    """将 sqrtPriceX96 转换为人类可读价格"""
    price = (sqrt_price_x96 / (2 ** 96)) ** 2
    price = price * (10 ** token0_dec) / (10 ** token1_dec)
    if invert:
        price = 1 / price if price != 0 else 0
    return price


class DEXMonitor:
    def __init__(self, price_store: dict, interval: int = 12):
        """
        price_store: 共享字典，格式 {"ETHUSDT_DEX": 2300.0, ...}
        interval: 轮询间隔秒数（以太坊出块约12秒）
        """
        self.price_store = price_store
        self.interval = interval
        self.w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
        self.running = False

    def _fetch_price(self, symbol: str, pool_address: str) -> float | None:
        try:
            cfg = POOL_DECIMALS.get(symbol)
            if not cfg:
                return None
            contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(pool_address),
                abi=POOL_ABI
            )
            slot0 = contract.functions.slot0().call()
            sqrt_price_x96 = slot0[0]
            price = sqrt_price_to_price(
                sqrt_price_x96,
                cfg["token0_dec"],
                cfg["token1_dec"],
                cfg["invert"]
            )
            return price
        except Exception as e:
            print(f"[DEX] 获取 {symbol} 价格失败: {e}")
            return None

    async def start(self):
        self.running = True
        print(f"[DEX] 开始轮询 Uniswap V3，间隔 {self.interval}s")
        while self.running:
            for symbol, pool_addr in UNISWAP_POOLS.items():
                if pool_addr is None:
                    continue
                price = await asyncio.get_event_loop().run_in_executor(
                    None, self._fetch_price, symbol, pool_addr
                )
                if price and price > 0:
                    self.price_store[f"{symbol}_DEX"] = price
                    print(f"[DEX] {symbol}: ${price:,.2f}")
            await asyncio.sleep(self.interval)

    def stop(self):
        self.running = False
