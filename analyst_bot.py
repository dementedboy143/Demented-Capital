"""
🛡️ Omni-Claw Analyst Node v2.2 (Institutional Grade - Ultimate Master)
Author: Demented Capital Research Division | Samrat Akash Maurya

Purpose: Fetch real-time market telemetry for major pairs to detect
abnormal volume spikes and potential institutional liquidity sweeps.
"""

import requests
import time
import statistics
from datetime import datetime, timezone

# ==========================================
# ⚙️ Institutional Configuration
# ==========================================

# 🛡️ Anti-Block Protocol: Using api1 to bypass ISP latency/blocks in India
BASE_URL = "https://api1.binance.com/api/v3"
KLINES_ENDPOINT = f"{BASE_URL}/klines"

# ⚔️ The Full Army of "Yoddha" (Top 11 Trending & Famous Pairs)
TRADING_PAIRS = [
    "BTCUSDT",   # Bitcoin - Market Leader
    "ETHUSDT",   # Ethereum - Altcoin Leader
    "BNBUSDT",   # Binance Coin - Essential for the Competition
    "SOLUSDT",   # Solana - High Volatility
    "XRPUSDT",   # XRP - High Institutional Interest
    "ADAUSDT",   # Cardano - Large Community
    "DOGEUSDT",  # Dogecoin - Major Meme Volatility
    "PEPEUSDT",  # Pepe - Top Trending Meme
    "FETUSDT",   # Artificial Superintelligence - AI Trend
    "LINKUSDT",  # Chainlink - Critical Infrastructure
    "MATICUSDT"  # Polygon - Key Layer 2
]

# Timeframe (1-minute candles)
INTERVAL = "1m"

# Number of past candles to calculate the "Normal" baseline average
WINDOW_SIZE = 10 

# Trigger if current volume is 250% (2.5x) of average (More Strict)
SPIKE_MULTIPLIER = 2.5 

# Network Dhairya (Timeout in seconds for slow connections)
NETWORK_TIMEOUT = 30

# Time delay between full checks (seconds)
CHECK_INTERVAL = 60

# ==========================================
# 🧠 Core Analytics Engine
# ==========================================

def fetch_and_analyze_data(symbol):
    """Fetches Kline data, calculates average, and detects spikes."""
    try:
        params = {
            "symbol": symbol,
            "interval": INTERVAL,
            "limit": WINDOW_SIZE + 1
        }
        
        # Connect to Binance API
        response = requests.get(KLINES_ENDPOINT, params=params, timeout=NETWORK_TIMEOUT)
        response.raise_for_status() 
        data = response.json()

        if not data or len(data) < WINDOW_SIZE:
            print(f"[!] Insufficient data for {symbol}")
            return None

        # historical candles volume
        history_volumes = [float(candle[5]) for candle in data[:-1]]
        
        # Current active candle data
        current_candle = data[-1]
        current_price = float(current_candle[4])
        current_volume = float(current_candle[5])
        
        # Baseline average volume
        avg_volume = statistics.mean(history_volumes)
        
        # Threshold logic
        spike_threshold = avg_volume * SPIKE_MULTIPLIER
        is_spike = current_volume > spike_threshold

        return {
            "symbol": symbol,
            "price": current_price,
            "current_volume": current_volume,
            "avg_volume": avg_volume,
            "is_spike": is_spike,
            "time": datetime.now(timezone.utc).strftime('%H:%M:%S UTC')
        }

    except requests.exceptions.Timeout:
        print(f"[ERROR] Timeout fetching {symbol}. (Network lag, retrying next cycle)")
        return None
    except Exception as e:
        print(f"[ERROR] System failure for {symbol}: {e}")
        return None

# ==========================================
# 📢 Analyst Output Delivery
# ==========================================

def print_structured_report(data):
    """Prints the analysis in an institutional format."""
    header = f"[{data['time']}] {data['symbol']} @ ${data['price']:,.4f}"
    
    if data['is_spike']:
        print("\n⚡" + "="*45)
        print(f"📡 {header} (URGENT ALERT)")
        print("="*47)
        print(f"📊 Volume Spike: {data['current_volume']:.2f} (Avg: {data['avg_volume']:.2f})")
        print("Omni-Claw Analytics Logic:")
        print(" [>] Potential Institutional Liquidity Sweep Detected.")
        print(" [>] Stop-Loss Hunt in Progress - Retail at Risk.")
        print(" [Action]: Alerting Educator Node (Phase 2).")
        print("="*47 + "\n")
    else:
        # 🛡️ Sab kuch normal hone par ek choti line print karega taaki aapko tasalli rahe ki data aa raha hai
        print(f"[✓] {header} | Flow: Normal")

# ==========================================
# ⚔️ Main Execution Loop
# ==========================================

if __name__ == "__main__":
    print("\n🚀 Booting Omni-Claw Analyst Node v2.2 (Anti-Block Edition)...")
    print(f"Brand : Demented Capital Research Division")
    print(f"Targeting {len(TRADING_PAIRS)} Institutional Assets.")
    print(f"Status: Monitoring Real-Time Liquidity via Binance API\n")
    print("-" * 50)
    
    while True:
        reports_generated = 0
        for pair in TRADING_PAIRS:
            analysis = fetch_and_analyze_data(pair)
            
            if analysis:
                print_structured_report(analysis)
                reports_generated += 1
            
            # 🛡️ BRAHMASTRA: Har coin check karne ke baad 2 second ka gap, taaki ISP block na kare!
            time.sleep(2)
                
        print("-" * 50)
        print(f"⏳ Waiting {CHECK_INTERVAL} seconds for the next minute's data cycle...")
        print("-" * 50)
        # Wait for the next minute's data
        time.sleep(CHECK_INTERVAL)