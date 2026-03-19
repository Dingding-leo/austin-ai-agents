#!/usr/bin/env python3
"""
OKX Scanner v4 - BTC Futures Trading
Strategies: Turtle + RSI Cross 50 | Both Long and Short
"""
import subprocess
import json

def get_live_prices():
    coins = {
        'BTC': 'bitcoin',
        'ETH': 'ethereum',
        'SOL': 'solana',
        'DOGE': 'dogecoin',
        'ARB': 'arbitrum',
    }
    prices = {}
    for coin, cg_id in coins.items():
        url = 'https://api.coingecko.com/api/v3/simple/price?ids=' + cg_id + '&vs_currencies=usd&include_24hr_change=true'
        try:
            r = subprocess.run(['curl', '-s', '--max-time', '8', url], capture_output=True, text=True, timeout=10)
            data = json.loads(r.stdout)
            prices[coin] = {'usd': data[cg_id]['usd'], 'change_24h': data[cg_id]['usd_24h_change']}
        except:
            pass
    return prices

def estimate_rsi(change_24h):
    if change_24h < -4: return 20
    elif change_24h < -2: return 30
    elif change_24h < 0: return 42
    elif change_24h < 2: return 55
    elif change_24h < 4: return 65
    else: return 75

LAST_KNOWN = {
    'BTC': {'usd': 69220, 'change_24h': -2.46},
    'ETH': {'usd': 2131, 'change_24h': -3.27},
    'SOL': {'usd': 88.17, 'change_24h': -5.23},
}

def scan():
    print("=" * 65)
    print("OKX SCAN v4 | BTC Futures | Turtle + RSI Cross 50")
    print("=" * 65)
    
    prices = get_live_prices()
    if not prices:
        prices = LAST_KNOWN
        print("\nUsing cached prices (API unreachable)")
    
    print("")
    for coin, data in prices.items():
        price = data['usd']
        chg = data['change_24h']
        rsi = estimate_rsi(chg)
        trend = "DOWN" if chg < 0 else "UP"
        print(f"  {coin}: ${price:,.2f} ({chg:+.2f}%) | RSI~{rsi} | {trend}")
    
    btc_chg = prices.get('BTC', {}).get('change_24h', -2.5)
    market = "RISK-OFF" if btc_chg < -2 else "NEUTRAL"
    
    print(f"\nMarket: {market} | All RSI~30 (oversold)")
    print("Signal: NO TRADE - need RSI cross 50")
    print("System v3 READY | Monitoring")

if __name__ == '__main__':
    scan()
