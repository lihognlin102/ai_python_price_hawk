"""
notifier.py
套利机会邮件报警
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import EMAIL_FROM, EMAIL_TO, SMTP_HOST, SMTP_PORT, SMTP_PASS


async def send_alert(opp: dict):
    """发送套利机会邮件"""
    subject = f"⚡ 套利机会 {opp['symbol']} 差价 {opp['diff_pct']}%"
    html = f"""
    <html><body style="font-family:Arial,sans-serif;padding:20px;background:#0d1117;color:#eee">
    <div style="max-width:500px;margin:0 auto;background:#161b22;padding:20px;border-radius:10px;border:1px solid #30363d">
        <h2 style="color:#f0c040;margin-top:0">⚡ 套利机会发现！</h2>
        <table style="width:100%;border-collapse:collapse">
            <tr><td style="padding:8px;color:#8b949e">币种</td>
                <td style="padding:8px;color:#58a6ff;font-weight:bold">{opp['symbol']}</td></tr>
            <tr style="background:#0d1117"><td style="padding:8px;color:#8b949e">CEX 价格（币安）</td>
                <td style="padding:8px">${opp['cex_price']:,.4f}</td></tr>
            <tr><td style="padding:8px;color:#8b949e">DEX 价格（Uniswap）</td>
                <td style="padding:8px">${opp['dex_price']:,.4f}</td></tr>
            <tr style="background:#0d1117"><td style="padding:8px;color:#8b949e">价差</td>
                <td style="padding:8px;color:#f85149;font-weight:bold">{opp['diff_pct']}%</td></tr>
            <tr><td style="padding:8px;color:#8b949e">操作方向</td>
                <td style="padding:8px;color:#3fb950;font-weight:bold">{opp['direction']}</td></tr>
            <tr style="background:#0d1117"><td style="padding:8px;color:#8b949e">发现时间</td>
                <td style="padding:8px">{opp['time']}</td></tr>
        </table>
        <p style="color:#8b949e;font-size:12px;margin-top:15px">
            ⚠️ 注意：实际套利需考虑 Gas 费、滑点、交易手续费，请谨慎操作。
        </p>
    </div>
    </body></html>
    """
    try:
        msg = MIMEMultipart("alternative")
        msg["From"]    = EMAIL_FROM
        msg["To"]      = EMAIL_TO
        msg["Subject"] = subject
        msg.attach(MIMEText(html, "html", "utf-8"))
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as s:
            s.login(EMAIL_FROM, SMTP_PASS)
            s.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        print(f"[通知] 邮件已发送: {subject}")
    except Exception as e:
        print(f"[通知] 邮件发送失败: {e}")
