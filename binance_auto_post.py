"""
🛡️ Demented Capital: Auto-Post Generator v3.0 (Rulebook Compliant)
Author: Samrat Akash Maurya
"""

import requests
import random
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---------------- DEMENTED BRAND DATABASE ---------------- #

INTROS = [
    "🚨 Demented Capital: Real-Time Market Intelligence!",
    "📊 High-IQ Educational Analysis is LIVE",
    "⚡ Pure Execution: Demented Flash Report",
    "📢 Demented Family, verify this market structure!",
    "🧠 Institutional Data: Read before you trade."
]

TRADE_LOGICS = [
    "Our Educational Analysis suggests this asset is approaching a critical liquidity zone.",
    "Market Structure is shifting. We are observing potential institutional accumulation.",
    "Price action shows tight consolidation. A volatility expansion aligns with our Pure Execution strategy.",
    "Order flow indicates changing momentum. Always map out your support/resistance.",
    "Volume analysis hints at a possible liquidity sweep. Watch the previous highs/lows."
]

# ---------------- BINANCE TRENDING LOGIC ---------------- #

def get_trending_coin():
    """Fetches high-volume USDT pairs automatically."""
    url = "https://api.binance.com/api/v3/ticker/24hr"
    try:
        res = requests.get(url, verify=False).json()
        usdt_pairs = [t for t in res if t['symbol'].endswith('USDT') and float(t['quoteVolume']) > 5000000]
        top_coin = random.choice(usdt_pairs)
        symbol = top_coin['symbol']
        return symbol, symbol.replace("USDT", "")
    except:
        return "TRBUSDT", "TRB"

def get_live_price(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        res = requests.get(url, verify=False).json()
        return res["price"]
    except:
        return "0.00"

# ---------------- BRAND POST GENERATOR ---------------- #

def generate_demented_post():
    symbol, name = get_trending_coin()
    price = round(float(get_live_price(symbol)), 3)
    
    intro = random.choice(INTROS)
    logic = random.choice(TRADE_LOGICS)
    
    # ⚠️ STRICT RULEBOOK: Exactly 3 Cashtags
    cashtags = f"${name} $BTC $ETH"
    
    # ⚠️ STRICT RULEBOOK: Exactly 5 Trending Hashtags
    hashtags = "#BinanceSquare #CryptoEducation #TradeSharing #MarketAnalysis #DementedCapital"

    # Narrative building with specific engagement and safety constraints
    content = f"""{intro}

📊 Educational Analysis: {name} ({symbol})
💰 Current Price: ${price}

📈 Market Intelligence (Pure Execution):
{logic}

[📸 Attach Real Screenshot of {symbol} Chart Here to verify the structure]

🎁 Interactive Quiz: What's your next move based on this analysis? 
A) Long 📈 | B) Short 📉 | C) Wait ⏳
Drop your answers below! Top engagers will receive Red Packets in the next update. Help us hit 300K views for our verification checkmark! ✔️

💡 Support the Vision: If this Educational Analysis helped you, use the Tip feature below. Your tips fuel our Write to Earn journey (50% commission goals) and keep the Demented Capital Research Division running!

⚠️ Safety First: This is strictly for Educational Analysis. Pure Execution. No Gambling. Zero spam policy. Always do your own research (DYOR) and follow Binance Community Safety Guidelines.

{cashtags}
{hashtags}"""

    return content

# ---------------- TEST EXECUTION ---------------- #

if __name__ == "__main__":
    print("\n" + "="*60)
    print(" 📢 GENERATING VIRAL NARRATIVE (RULEBOOK COMPLIANT)")
    print("="*60 + "\n")
    print(generate_demented_post())
    print("\n" + "="*60)