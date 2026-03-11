"""
🛡️ Demented Capital: The Ultimate Square Bot v4.0 (Merged Masterpiece)
Author: Samrat Akash Maurya
Purpose: Fetches Global News, Calculates RSI, Scans Volume Momentum, 
and Auto-Posts a Rulebook Compliant Viral Narrative to Binance Square.
"""

import requests
import random
import os
import re
import time
import urllib3
import xml.etree.ElementTree as ET

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==========================================
# ⚙️ Institutional Configuration
# ==========================================
API_KEY = os.getenv("BINANCE_API_KEY")
# Note: Using your provided endpoint logic
BAPI_URL = "https://www.binance.com/bapi/composite/v1/public/pgc/openApi/content/add"

def fetch_with_retry(url, headers=None, is_json=True):
    for i in range(3):
        try:
            res = requests.get(url, headers=headers, timeout=10, verify=False)
            return res.json() if is_json else res.content
        except Exception:
            time.sleep(3)
    return None

# ==========================================
# 🧠 Data Engines (News, Momentum & RSI)
# ==========================================

def get_latest_news():
    """Fetches real-time crypto news headlines."""
    headers = {"User-Agent": "Mozilla/5.0"}
    content = fetch_with_retry("https://cointelegraph.com/rss", headers=headers, is_json=False)
    
    if content:
        try:
            root = ET.fromstring(content)
            items = root.findall('.//item')
            if items:
                news = random.choice(items[:5])
                return news.find('title').text
        except:
            pass
    return "Massive crypto volatility detected! Institutional liquidity sweeping underway."

def get_top_trending_coins():
    """Scans for Top 3 Momentum Coins (Volume x Price Change)."""
    res = fetch_with_retry("https://api.binance.com/api/v3/ticker/24hr")
    
    fallback_data = (
        {"symbol": "BTCUSDT", "lastPrice": "68000", "priceChangePercent": "1.5"},
        {"symbol": "ETHUSDT"}, 
        {"symbol": "BNBUSDT"}
    )
    
    if not res or isinstance(res, dict):
        return fallback_data
        
    usdt_pairs = [t for t in res if isinstance(t, dict) and t.get('symbol', '').endswith('USDT')]
    ignore_list = ['USDCUSDT', 'FDUSDUSDT', 'TUSDUSDT', 'BUSDUSDT', 'EURUSDT']
    valid_pairs = [t for t in usdt_pairs if t.get('symbol') not in ignore_list]
    
    if not valid_pairs: 
         return fallback_data

    # Sort by Momentum (Volume * Price Change)
    valid_pairs.sort(key=lambda x: float(x.get('quoteVolume', 0)) * abs(float(x.get('priceChangePercent', 0))), reverse=True)
    
    top_pool = valid_pairs[:10]
    main_coin = random.choice(top_pool[:3])
    
    # Ensure we get 2 other unique coins for the 3 Cashtags rule
    other_coins = random.sample([c for c in top_pool if c.get('symbol') != main_coin.get('symbol')], 2)
    
    return main_coin, other_coins[0], other_coins[1]

def get_14h_rsi(symbol):
    """Calculates Real 14H RSI."""
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=15"
    klines = fetch_with_retry(url)
    
    if not klines or len(klines) < 15: return "Neutral Data"
        
    closes = [float(k[4]) for k in klines]
    gains, losses = [], []
    for i in range(1, len(closes)):
        change = closes[i] - closes[i-1]
        if change > 0:
            gains.append(change); losses.append(0)
        else:
            gains.append(0); losses.append(abs(change))
            
    avg_gain = sum(gains) / 14
    avg_loss = sum(losses) / 14
    
    if avg_loss == 0: return "99.9 (Overbought 🔥)"
        
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    if rsi > 70: return f"{round(rsi, 1)} (Overbought 🔴)"
    elif rsi < 30: return f"{round(rsi, 1)} (Oversold 🟢)"
    else: return f"{round(rsi, 1)} (Neutral ⚪)"

# ==========================================
# 📝 Rulebook Compliant Content Generator
# ==========================================

def generate_viral_post():
    main_coin, coin2, coin3 = get_top_trending_coins()
    news_headline = get_latest_news()
    
    c1_name = main_coin['symbol'].replace("USDT", "")
    c2_name = coin2['symbol'].replace("USDT", "")
    c3_name = coin3['symbol'].replace("USDT", "")
    
    price = round(float(main_coin['lastPrice']), 4)
    change = float(main_coin['priceChangePercent'])
    trend_icon = "📈" if change > 0 else "📉"
    
    rsi_status = get_14h_rsi(main_coin['symbol'])
    
    # ⚠️ EXACTLY 3 CASHTAGS
    dynamic_cashtags = f"${c1_name} ${c2_name} ${c3_name}"
    
    # ⚠️ EXACTLY 5 HASHTAGS (Fixed as per rulebook for safety)
    rulebook_hashtags = "#BinanceSquare #CryptoEducation #TradeSharing #MarketAnalysis #DementedCapital"

    intros = [
        "🚨 URGENT MARKET INTELLIGENCE 🚨", 
        "🔥 DEMENTED CAPITAL: EDUCATIONAL ANALYSIS 🔥", 
        "⚠️ PURE EXECUTION: MARKET UPDATE ⚠️"
    ]

    content = f"""{random.choice(intros)}

🌐 *Global Market Pulse:*
"{news_headline}"

📊 *Educational Analysis: {c1_name}/USDT*
💰 Live Price: ${price} ({change}% {trend_icon})
📉 RSI (14H): {rsi_status}

🧠 *Market Intelligence:*
We are tracking an institutional liquidity sweep. Market Structure is actively testing critical zones. Watch the order flow and avoid trading the false breakouts. 

[📸 Attach Real Screenshot here to map the structure]

🎁 *Interactive Check:*
What is your move? A) Bullish Accumulation 📈 | B) Bearish Distribution 📉
Drop your analysis below! Top engagers will receive Quiz rewards or Red Packets. Help us secure that 300K views target for our Verification checkmark! ✔️

💡 *Support the Vision:*
If this Educational Analysis keeps you ahead of the market, use the Tips feature below! It fuels our Write to Earn journey (aiming for 50 percent commission) and supports the Demented Capital Research Division.

⚠️ *Safety First:*
Pure Execution. No Gambling. Zero spam policy. Always strictly DYOR and adhere to Binance Community Safety Guidelines.

{dynamic_cashtags}
{rulebook_hashtags}"""

    # Failsafe character limit for Binance Square
    if len(content) > 950:
        content = content[:900] + f"...\n⚠️ DYOR.\n{dynamic_cashtags}\n{rulebook_hashtags}"

    return content

# ==========================================
# 🚀 Direct Binance Execution (The Cannon)
# ==========================================

def post_to_square():
    print("\n" + "🔥"*25)
    print(" 🚀 INITIATING DEMENTED SQUARE BOT v4.0")
    print("🔥"*25 + "\n")

    content = generate_viral_post()
    
    if not API_KEY or len(API_KEY) < 20:
        print("❌ Error: Valid BINANCE_API_KEY missing from Secrets!")
        print("Running in [SIMULATION MODE]:\n")
        print("-" * 50)
        print(content)
        print("-" * 50)
        return

    print(f"Post Length: {len(content)} chars. Firing to Binance...")
    
    headers = {
        "X-Square-OpenAPI-Key": API_KEY,
        "Content-Type": "application/json",
        "clienttype": "binanceSkill"
    }
    
    for i in range(3):
        try:
            # Using bodyTextOnly payload format as per your previous setup
            resp = requests.post(BAPI_URL, headers=headers, json={"bodyTextOnly": content}, timeout=15)
            result = resp.json()
            if result.get("code") == "000000":
                print("✅ VIJAYI BHAVA! Institutional Post Sent Successfully to Binance Square.")
                break
            else:
                print(f"⚠️ Binance Error: {result.get('message')}")
                time.sleep(3)
        except Exception as e:
            print(f"🚨 Connection Error: {e}")
            time.sleep(3)

if __name__ == "__main__":
    post_to_square()