# ai_python_price_hawk 🦅

实时监控主流币 CEX（币安）vs DEX（Uniswap V3）价差，自动发现套利机会。

## 监控币种
- BTC、ETH、BNB、SOL、MATIC

## 功能
- 🔴 币安 WebSocket 实时价格（毫秒级）
- 🟢 Uniswap V3 链上价格（每12秒轮询）
- ⚡ 自动计算 CEX/DEX 价差，差价 > 0.3% 触发报警
- 📧 邮件报警通知
- 🌐 HTTP API 供前端调用

## API 接口
| 接口 | 说明 |
|------|------|
| `GET /api/prices` | 所有实时价格 |
| `GET /api/arbitrage` | 最新套利机会列表 |
| `GET /api/status` | 服务状态 |

## 启动

```bash
# Docker 启动（推荐）
docker-compose up -d

# 本地启动
pip install -r requirements.txt
python main.py
```

## 删除

```bash
docker-compose down --rmi all
```
