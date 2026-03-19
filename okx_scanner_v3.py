#!/usr/bin/env python3
"""
OKX Live Scanner v3 — Multi-Timeframe + Turtle + RSI Cross
Uses web_fetch or exec for data
"""
import json
import subprocess
import re

def get_ohlc_data():
    """Fetch 4H candles from OKX API"""
    cmd = ['curl', '-s', '--max-time', '10', 
           'https://www.okx.com/api/v5/market/history-candles?instId=BTC-USDT&bar=4H&limit=60']
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=12)
        data = json.loads(result.stdout)
        if 'data' in data and data['data']:
            candles = []
            for c in reversed(data['data']):
                candles.append({
                    'ts': int(c[0]),
                    'open': float(c[1]),
                    'high': float(c[2]),
                    'low': float(c[3]),
                    'close': float(c[4]),
                    'vol': float(c[5])
                })
            return candles
    except:
        pass
    return None

def get_ticker_data():
    """Fetch ticker from OKX"""
    cmd = ['curl', '-s', '--max-time', '10',
           'https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT']
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=12)
        data = json.loads(result.stdout)
        if 'data' in data and data['data']:
            d = data['data'][0]
            return {
                'last': float(d['last']),
                'change': (float(d['last']) - float(d['sodUtc0'])) / float(d['sodUtc0']) * 100
            }
    except:
        pass
    return None

def calc_rsi(prices, period=14):
    deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    rsi = []
    for i in range(period, len(deltas)):
        if i > period:
            avg_gain = (avg_gain * (period-1) + gains[i]) / period
            avg_loss = (avg_loss * (period-1) + losses[i]) / period
        rs = avg_gain / avg_loss if avg_loss != 0 else 100
        rsi.append(100 - (100 / (1 + rs)))
    return rsi

def calc_ema(data, period):
    k = 2/(period+1)
    result = [data[0]]
    for d in data[1:]:
        result.append(d * k + result[-1] * (1-k))
    return result

def scan():
    print("=" * 65)
    print("OKX LIVE SCAN v3 — Multi-Timeframe")
    print("Strategies: Turtle + RSI Cross 50 | TF: 4H")
    print("=" * 65)
    
    ticker = get_ticker_data()
    candles = get_ohlc_data()
    
    if not candles:
        print("ERROR: Cannot reach OKX API. Try again in 5 minutes.")
        return
    
    closes = [c['close'] for c in candles]
    highs = [c['high'] for c in candles]
    lows = [c['low'] for c in candles]
    
    price = closes[-1]
    rsi = calc_rsi(closes, 14)
    rsi_offset = len(closes) - len(rsi)
    rsi_curr = rsi[-1] if rsi else 50
    rsi_prev = rsi[-2] if len(rsi) > 1 else 50
    ema20 = calc_ema(closes, 20)
    ema50 = calc_ema(closes, 50)
    
    # RSI Cross signals
    rsi_cross_up = rsi_prev <= 50 and rsi_curr > 50
    rsi_cross_down = rsi_prev >= 50 and rsi_curr < 50
    
    # Turtle signals (20 period high/low)
    period_high_20 = max(highs[-20:])
    period_low_20 = min(lows[-20:])
    turtle_long = price > period_high_20
    turtle_short = price < period_low_20
    
    # Trend
    trend_up = price > ema20[-1] if len(ema20) > 0 else False
    trend_up_50 = price > ema50[-1] if len(ema50) > 0 else False
    
    # Funding (simplified)
    funding_ok = True  # Would need another API call
    
    change = ticker['change'] if ticker else 0
    
    print(f"\nBTC: ${price:,.0f} ({change:+.2f}% 24h)")
    print(f"RSI: {rsi_curr:.1f} | EMA20: ${ema20[-1]:,.0f} | EMA50: ${ema50[-1]:,.0f}")
    print(f"Trend: {'UP ⬆️' if trend_up_50 else 'DOWN ⬇️'}")
    
    print(f"\n--- SIGNALS ---")
    
    # Check all signals
    signals = []
    
    # Turtle LONG
    if turtle_long:
        signals.append(('TURTLE LONG', f'Price broke 20-high (${period_high_20:,.0f})'))
    
    # Turtle SHORT
    if turtle_short:
        signals.append(('TURTLE SHORT', f'Price broke 20-low (${period_low_20:,.0f})'))
    
    # RSI Cross LONG
    if rsi_cross_up:
        conf = 'STRONG' if trend_up_50 else 'WEAK'
        signals.append(('RSI LONG', f'Crossed 50 from below [{conf}]'))
    
    # RSI Cross SHORT
    if rsi_cross_down:
        conf = 'STRONG' if not trend_up_50 else 'WEAK'
        signals.append(('RSI SHORT', f'Crossed 50 from above [{conf}]'))
    
    if signals:
        for sig, reason in signals:
            print(f"  ⚡ {sig}: {reason}")
    else:
        print("  🟡 No signals — waiting")
    
    print(f"\n--- VERDICT ---")
    
    # Determine trade
    long_signals = [s for s in signals if 'LONG' in s[0]]
    short_signals = [s for s in signals if 'SHORT' in s[0]]
    
    if long_signals and trend_up_50:
        print(f"  🟢 READY TO LONG")
        print(f"  Entry: ${price:,.0f} | SL: ${price*0.98:,.0f} (-2%) | TP: ${price*1.04:,.0f} (+4%)")
        print(f"  Risk: $0.50 (1% of $50)")
    elif short_signals and not trend_up_50:
        print(f"  🔴 READY TO SHORT")
        print(f"  Entry: ${price:,.0f} | SL: ${price*1.02:,.0f} (+2%) | TP: ${price*0.96:,.0f} (-4%)")
        print(f"  Risk: $0.50 (1% of $50)")
    elif rsi_curr < 30:
        print(f"  🟡 WAIT — RSI oversold ({rsi_curr:.1f}), need cross above 50")
    elif rsi_curr > 70:
        print(f"  🟡 WAIT — RSI overbought ({rsi_curr:.1f}), need cross below 50")
    else:
        print(f"  🟡 NO TRADE — No clear signal")
    
    return price, rsi_curr, trend_up_50

if __name__ == '__main__':
    scan()
