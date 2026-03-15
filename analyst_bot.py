import requests
import random
import hashlib
import json
import os
import urllib3
from datetime import datetime

# 🚨 SSL WARNINGS BYPASS (For smooth execution)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- SYSTEM CONFIGURATION ---
# GitHub Actions se API Key automatically fetch hogi (Secure method)
API_KEY = os.getenv("BINANCE_API_KEY") 
DB_PATH = "post_memory.json"
BINANCE_URL = "https://www.binance.com/bapi/composite/v1/public/pgc/openApi/content/add"

class AnalystNode:
    """Scans market data to find top volatile coins."""
    def get_market_data(self):
        print("📊 Analyst Node: Scanning Binance 24h Ticker...")
        try:
            url = "https://api.binance.com/api/v3/ticker/24hr"
            data = requests.get(url, verify=False).json()
            
            # Filter valid USDT pairs with high volume
            alts = [c for c in data if c['symbol'].endswith('USDT') and float(c['quoteVolume']) > 10000000]
            top_movers = sorted(alts, key=lambda x: abs(float(x['priceChangePercent'])), reverse=True)[:10]
            selected = random.choice(top_movers)
            
            coin_name = selected['symbol'].replace('USDT', '')
            price = round(float(selected['lastPrice']), 4)
            change = round(float(selected['priceChangePercent']), 2)
            trend = "sweeping liquidity downside" if change < 0 else "expanding with high volume"
            
            return {"coin": coin_name, "trend": trend, "price": price, "change": change}
        except Exception as e:
            print(f"🚨 Analyst Error: {e}")
            return {"coin": "BTC", "trend": "consolidating heavily", "price": 0, "change": 0}

class EducatorNode:
    """Translates raw data into the 'Golden Format' Educational Narrative."""
    def generate_narrative(self, market_data):
        print("🧠 Educator Node: Crafting Educational Narrative...")
        coin = market_data['coin']
        price = market_data['price']
        change = market_data['change']
        trend = market_data['trend']
        
        # Golden Format Template
        post_text = (
            f"🚨 MARKET ALERT: LIQUIDITY SHIFT 🚨\n\n"
            f"📊 LIVE DATA:\n"
            f"🔹 Asset: ${coin}\n"
            f"🔹 Current Price: ${price}\n"
            f"🔹 24H Action: {change}%\n\n"
            f"🧠 INSTITUTIONAL INSIGHT:\n"
            f"Current market structure shows {coin} is {trend}. "
            f"This is exactly where retail traders get trapped by emotions, while smart money executes their planned strategy. Volume always precedes price.\n\n"
            f"⚔️ THE WAR ROOM QUESTION:\n"
            f"Are you adding to your position here, or waiting for a clearer setup? Let me know below! 👇\n\n"
            f"${coin} $BTC $ETH\n"
            f"#CryptoEducation #MarketAlpha #DementedCapital #BinanceSquare"
        )
        return post_text

class DiversityEngine:
    """Ensures 0% spam rate by maintaining unique cryptographic hashes."""
    def is_unique(self, content):
        print("🛡️ Diversity Engine: Verifying Cryptographic Uniqueness...")
        post_hash = hashlib.md5(content.encode()).hexdigest()
        
        if not os.path.exists(DB_PATH):
            with open(DB_PATH, 'w') as f:
                json.dump([], f)
                
        with open(DB_PATH, 'r') as f:
            memory = json.load(f)
            
        if post_hash in memory:
            return False
            
        memory.append(post_hash)
        # Keep memory light (last 1000 posts)
        with open(DB_PATH, 'w') as f:
            json.dump(memory[-1000:], f)
            
        return True

class PublisherNode:
    """Executes the final payload via Binance Square API."""
    def publish(self, content):
        if not API_KEY:
            print("🚨 FATAL ERROR: BINANCE_API_KEY is missing! GitHub Secrets check kijiye.")
            return False
            
        print("🚀 Publisher Node: Transmitting to Binance Square...")
        headers = {
            "X-Square-OpenAPI-Key": API_KEY,
            "Content-Type": "application/json",
            "clienttype": "binanceSkill"
        }
        data = {"bodyTextOnly": content}
        
        try:
            response = requests.post(BINANCE_URL, headers=headers, json=data, verify=False)
            result = response.json()
            if result.get('success'):
                print("✅ OMNI CLAW SUCCESS: Post is live on Binance Square!")
                return True
            else:
                print(f"❌ API REJECTION: {result}")
                return False
        except Exception as e:
            print(f"🚨 Network Failure: {e}")
            return False

def run_demented_bot():
    print(f"\n--- ⚙️ INITIATING DEMENTED ANALYST BOT | {datetime.now()} ---")
    reports_generated = 0  # Counter tracker
    
    analyst = AnalystNode()
    educator = EducatorNode()
    diversity = DiversityEngine()
    publisher = PublisherNode()
    
    market_data = analyst.get_market_data()
    final_post = educator.generate_narrative(market_data)
    
    if diversity.is_unique(final_post):
        success = publisher.publish(final_post)
        if success:
            reports_generated += 1
    else:
        print("⚠️ Diversity Collision: Post matched existing hash. Aborting to prevent spam flag.")
        
    print(f"📈 Total Reports Generated this session: {reports_generated}")
    print("--- 🛑 EXECUTION COMPLETE ---\n")

if __name__ == "__main__":
    run_demented_bot()
