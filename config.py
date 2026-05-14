# 监控币种及 Uniswap V3 池子地址（ETH 主网）
SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "MATICUSDT"]

# 币安 WSS
BINANCE_WSS = "wss://stream.binance.com:9443/stream"

# 免费公共以太坊 RPC
ETH_RPC_URL = "https://eth.llamarpc.com"

# Uniswap V3 池子地址（token/USDC 0.05% 池）
UNISWAP_POOLS = {
    "ETHUSDT":   "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640",  # ETH/USDC
    "BTCUSDT":   "0x99ac8ca7087fa4a2a1fb6357269965a2014abc35",  # WBTC/USDC
    "BNBUSDT":   None,  # BNB 主要在 BSC，暂不监控链上
    "SOLUSDT":   None,  # SOL 不在以太坊
    "MATICUSDT": "0x290a6a7460b308ee3f19023d2d00de604bcf5b42",  # MATIC/USDC
}

# 套利阈值（百分比），超过此值触发报警
ARBITRAGE_THRESHOLD = 0.3

# 邮件配置
EMAIL_FROM = "1519863276@qq.com"
EMAIL_TO   = "1519863276@qq.com"
SMTP_HOST  = "smtp.qq.com"
SMTP_PORT  = 465
SMTP_PASS  = "zbjpoowhlliujdhg"
