"""
Omni-Claw Analyst Node v2.1 (Institutional Grade - Master Version)
Author: Demented Capital Research Division

Purpose:
--------
Connect to the public Binance REST API (Klines/Candlestick endpoint) to 
fetch real-time market telemetry for major trading pairs.

Unlike standard 24h tickers, this script analyzes 1-minute candle volumes
to instantly detect abnormal volume spikes, stop-loss cascades, and 
liquidity sweeps in real-time.

Key Features:
-------------
• 1-Minute Kline (Candlestick) monitoring
• Rolling average calculation of the last 10 minutes
• Real-time volume spike detection (Liquidity Hunt flagging)
• Clean modular architecture for GitHub integration
• ISP Bypass via Alternate API Endpoint (api4)
"""

import requests
import time
import statistics
from datetime import datetime, timezone

# =========================
# Institutional Configuration
# =========================

# Note: Using api4.binance.com to bypass local network/ISP blocks in India.
BINANCE_KLINES_URL = "https://api4.binance.com/api/v3/klines"

# Trading pairs to monitor (Pure Execution targets)
# Institutional & Trending pairs to monitor
TRADING_PAIRS = [
    "BTCUSDT",   # Bitcoin - Market Leader
    "ETHUSDT",   # Ethereum - Altcoin Leader
    "BNBUSDT",   # Binance Coin - Essential for the Competition
    "SOLUSDT",   # Solana - High Volatility/Trending
    "XRPUSDT",   # XRP - High Institutional Interest
    "ADAUSDT",   # Cardano - Large Community
    "DOGEUSDT",  # Dogecoin - Major Meme Volatility
    "PEPEUSDT",  # Pepe - Top Trending Meme
    "FETUSDT",   # Artificial Superintelligence (FET) - AI Trend
    "LINKUSDT",  # Chainlink - Critical Infrastructure
    "MATICIUSDT" # Polygon/POL - Key Layer 2
]

# Timeframe for candles
KLINE_INTERVAL = "1m"

# Number of past candles to calculate the "Normal" average
VOLUME_WINDOW = 10 

# Spike threshold: Trigger if current candle volume is 200% (2.0x) of average
VOLUME_SPIKE_MULTIPLIER = 2.0 

# Time delay between checks (seconds)
CHECK_INTERVAL = 60

# =========================
# Data Engine (The Brain)
# =========================

def fetch_and_analyze_data(symbol):
    """
    Fetches the latest klines, separates historical volume from current volume,
    and returns analytical data.
    """
    try:
        # We fetch VOLUME_WINDOW + 1 candles. 
        # The first ones are history, the last one is the current active minute.
        params = {
            "symbol": symbol,
            "interval": KLINE_INTERVAL,
            "limit": VOLUME_WINDOW + 1
        }
        
        response = requests.get(BINANCE_KLINES_URL, params=params, timeout=30)
        data = response.json()

        # Binance Kline format: [0: open_time, 1: open, 2: high, 3: low, 4: close, 5: volume...]
        # Extract volumes of the completed historical candles
        history_volumes = [float(candle[5]) for candle in data[:-1]]
        
        # Extract data for the current active candle
        current_candle = data[-1]
        current_price = float(current_candle[4])
        current_volume = float(current_candle[5])
        
        # Calculate the baseline average volume
        avg_volume = statistics.mean(history_volumes)
        
        # Detect if current volume breaches the institutional threshold
        spike_threshold = avg_volume * VOLUME_SPIKE_MULTIPLIER
        spike_detected = current_volume > spike_threshold

        return {
            "symbol": symbol,
            "price": current_price,
            "current_volume": current_volume,
            "avg_volume": avg_volume,
            "spike_detected": spike_detected,
            "timestamp": datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
        }

    except Exception as e:
        print(f"[ERROR] Analyst Node failed to fetch {symbol}: {e}")
        return None

# =========================
# Output Delivery
# =========================

def print_educational_report(data):
    """Prints the structured output for the Educator Node."""
    
    print("\n=========================================")
    print(" 🛡️ OMNI-CLAW ANALYST REPORT (LIVE)")
    print("=========================================")
    print(f"Time      : {data['timestamp']}")
    print(f"Asset     : {data['symbol']}")
    print(f"Price     : ${data['price']:,.2f}")
    print(f"1m Volume : {data['current_volume']:,.2f} (Avg: {data['avg_volume']:,.2f})")

    if data['spike_detected']:
        print("\n⚠️ ABNORMAL VOLUME SPIKE DETECTED ⚠️")
        print("Omni-Claw Logic Analysis:")
        print(" [>] Potential Liquidity Sweep in progress.")
        print(" [>] Institutional Order Flow entering.")
        print(" [>] Retail stop-losses may have been triggered.")
        print(" Action: Feed data to Educator Node.")
    else:
        print("\n[✓] Market Status: Normal Execution Flow")
        
    print("=========================================\n")

# =========================
# Main Execution Loop
# =========================

def run_omniclaw_node():
    print("🚀 Booting Omni-Claw Analyst Node v2.1...")
    print("Monitoring real-time liquidity via Binance API...\n")
    
    while True:
        for pair in TRADING_PAIRS:
            analysis_data = fetch_and_analyze_data(pair)
            
            if analysis_data:
                print_educational_report(analysis_data)
                
        # Wait before scanning the next minute's data
        time.sleep(CHECK_INTERVAL)

# =========================
# Entry Point
# =========================

if __name__ == "__main__":
    run_omniclaw_node()