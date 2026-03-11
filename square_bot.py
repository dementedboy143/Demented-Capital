"""
🛡️ Demented Capital: Square Traffic Bot v3.0 (Telegram to Binance Bridge)
Author: Samrat Akash Maurya
Purpose: Routes Telegram audience to Binance Square Master Roadmaps using
rulebook-compliant Viral Educational Narratives.
"""

import requests
import os
import random

# ==========================================
# ⚙️ Institutional Configuration
# ==========================================
# GitHub Secrets se Telegram Bot Token aayega
SQUARE_TOKEN = os.getenv("SQUARE_BOT_TOKEN")
CHAT_ID = "@DementedCapital"

def generate_educational_content():
    """Generates strictly compliant Viral Narrative for Telegram."""
    
    lessons = [
        {
            "title": "🧠 The Psychology of Liquidity & Pure Execution",
            "body": "Retail traders place Stop-Losses below obvious support. Institutions hunt these levels. Our Educational Analysis focuses on Pure Execution—identifying these sweeps before the violent reversal. [📸 Check the Trade Sharing with real screenshots in our Master Roadmap below!]"
        },
        {
            "title": "📊 Support/Resistance vs. Order Blocks",
            "body": "Retail trades lines; institutions trade volume blocks. When the market hits an institutional order block, the reaction is immediate. We do Trade Sharing with real screenshots to prove this. Stop guessing, start analyzing."
        },
        {
            "title": "⚖️ Risk Management is the Empire's Shield",
            "body": "A 40% win rate is highly profitable with a strict Risk:Reward ratio. Capital preservation is our top priority. We maintain a strict Zero spam policy here—just pure data. Are you managing your risk correctly?"
        }
    ]
    
    selected = random.choice(lessons)
    
    # ⚠️ EXACTLY 3 Cashtags & 5 Trending Hashtags (Strict Constraint)
    cashtags = "$BTC $ETH $BNB"
    hashtags = "#BinanceSquare #CryptoEducation #TradingStrategy #MarketAnalysis #DementedCapital"
    
    report = f"""📚 **DEMENTED CAPITAL: VIRAL EDUCATION SERIES** 📚

{selected['title']}

{selected['body']}

🎁 **Interactive Check:** We regularly drop Quiz and Red Packets for top engagers on our Square articles! Help us hit the 300K views target for our Verification checkmark! ✔️

💡 **Support the Vision:** If this Educational Analysis helped you, please use the Tips features on our Binance Square articles! It directly supports our Write to Earn journey (aiming for that 50 percent commission) and keeps this high-IQ content flowing.

⚠️ **Safety First:** Pure Execution. No Gambling. Always strictly DYOR. Follow Binance Community Safety Guidelines.

👇 *Master the market structure by reading our Ultimate Roadmap series below!*

{cashtags}
{hashtags}"""
    
    return report

def deploy_square_promo():
    """Fires the payload to Telegram with Inline Keyboard Buttons."""
    
    print("\n" + "🔥"*25)
    print(" 🚀 INITIATING TELEGRAM -> SQUARE BRIDGE")
    print("🔥"*25 + "\n")

    msg = generate_educational_content()
    url = f"https://api.telegram.org/bot{SQUARE_TOKEN}/sendMessage"
    
    # Tikdam: Dual Buttons pointing directly to the Master Roadmaps
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🗺️ Ultimate Master Roadmap (Part 1)", "url": "https://app.binance.com/uni-qr/cart/291638915366145?l=en&r=H6FLXIJP&uc=web_square_share_link&uco=M9U5rFxykWDbG29Ts2pIfQ&us=copylink"}
            ],
            [
                {"text": "🗺️ Ultimate Master Roadmap (Part 2)", "url": "https://app.binance.com/uni-qr/cart/290109321221457?l=en&r=H6FLXIJP&uc=web_square_share_link&uco=M9U5rFxykWDbG29Ts2pIfQ&us=copylink"}
            ]
        ]
    }
    
    payload = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown",
        "reply_markup": keyboard
    }
    
    # Execution & Safety Check
    if not SQUARE_TOKEN:
        print("[!] SECURITY WARNING: 'SQUARE_BOT_TOKEN' not found!")
        print("[!] Running in 'Simulation Mode':\n")
        print(msg)
        print("\n[✓] Keyboard Buttons Active. Add Token to go live.")
        return

    try:
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code == 200:
            print("✅ Square Bot Mission Success: Traffic routed to Master Roadmaps!")
        else:
            print(f"❌ Mission Failed: Telegram API Error -> {r.text}")
    except Exception as e:
        print(f"❌ Network Error: {e}")

if __name__ == "__main__":
    deploy_square_promo()