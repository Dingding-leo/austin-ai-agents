import json
import urllib.request

def get(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read()).get('data', [])
    except:
        return []

coins = {'BTC': 'BTC-USDT', 'ETH': 'ETH-USDT', 'SOL': 'SOL-USDT',
         'DOGE': 'DOGE-USDT', 'ARB': 'ARB-USDT', 'AVAX': 'AVAX-USDT',
         'LINK': 'LINK-USDT', 'XRP': 'XRP-USDT'}

all_data = {}
for k, v in coins.items():
    d = get(f'https://www.okx.com/api/v5/market/history-candles?instId={v}&bar=4H&limit=500')
    if d:
        all_data[k] = list(reversed(d))

def hi(data, period):
    result = []
    for i in range(period - 1, len(data)):
        result.append(max(data[i - period + 1:i + 1]))
    return result

def lo(data, period):
    result = []
    for i in range(period - 1, len(data)):
        result.append(min(data[i - period + 1:i + 1]))
    return result

def calc_rsi(prices, period=14):
    deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    rsi = []
    for i in range(period, len(deltas)):
        if i > period:
            avg_gain = (avg_gain * (period - 1) + gains[i]) / period
            avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        rs = avg_gain / avg_loss if avg_loss != 0 else 100
        rsi.append(100 - (100 / (1 + rs)))
    return rsi

def turtle_both(entry_period, exit_period, data, initial=50):
    closes = [float(c[4]) for c in data]
    highs = [float(c[2]) for c in data]
    lows = [float(c[3]) for c in data]
    eh = hi(highs, entry_period)
    el = lo(lows, entry_period)
    xh = hi(highs, exit_period)
    xl = lo(lows, exit_period)
    offset = max(entry_period, exit_period)
    pos = 0
    entry = 0
    bal = initial
    trades = []
    for i in range(offset, len(closes) - 1):
        p = closes[i]
        if pos == 0 and p > eh[i - offset]:
            pos = 1
            entry = p
            sl = xl[i - offset]
            tp = p + 2 * (p - sl)
        elif pos == 0 and p < el[i - offset]:
            pos = -1
            entry = p
            sl = xh[i - offset]
            tp = p - 2 * (sl - p)
        elif pos == 1:
            pn = (p - entry) / entry
            if p <= sl or p >= tp or p < xl[i - offset]:
                bal *= (1 + pn)
                trades.append({'dir': 'LONG', 'pn': pn})
                pos = 0
        elif pos == -1:
            pn = (entry - p) / entry
            if p >= sl or p <= tp or p > xh[i - offset]:
                bal *= (1 + pn)
                trades.append({'dir': 'SHORT', 'pn': pn})
                pos = 0
    if pos:
        p = closes[-1]
        pn = (p - entry) / entry if pos == 1 else (entry - p) / entry
        bal *= (1 + pn)
        trades.append({'dir': 'LONG' if pos == 1 else 'SHORT', 'pn': pn})
    return bal, trades

def rsi_cross_both(data, initial=50):
    closes = [float(c[4]) for c in data]
    rsi = calc_rsi(closes, 14)
    offset = len(closes) - len(rsi)
    pos = 0
    entry = 0
    bal = initial
    trades = []
    for i in range(14, len(closes) - 1):
        p = closes[i]
        rv = rsi[i - offset] if 0 <= i - offset < len(rsi) else 50
        rp = rsi[i - 1 - offset] if 0 <= i - 1 - offset < len(rsi) else 50
        if pos == 0 and rp <= 50 and rv > 50:
            pos = 1
            entry = p
            sl = p * 0.98
            tp = p * 1.04
        elif pos == 0 and rp >= 50 and rv < 50:
            pos = -1
            entry = p
            sl = p * 1.02
            tp = p * 0.96
        elif pos == 1:
            pn = (p - entry) / entry
            if p <= sl or p >= tp or rv > 65:
                bal *= (1 + pn)
                trades.append({'dir': 'LONG', 'pn': pn})
                pos = 0
        elif pos == -1:
            pn = (entry - p) / entry
            if p >= sl or p <= tp or rv < 35:
                bal *= (1 + pn)
                trades.append({'dir': 'SHORT', 'pn': pn})
                pos = 0
    if pos:
        p = closes[-1]
        pn = (p - entry) / entry if pos == 1 else (entry - p) / entry
        bal *= (1 + pn)
        trades.append({'dir': 'LONG' if pos == 1 else 'SHORT', 'pn': pn})
    return bal, trades

# Run backtests
print(f"\n{'='*90}")
print(f"TURTLE (BOTH SIDES) vs RSI CROSS 50 | 8 COINS | 300x 4H candles | Jan-Mar 2026")
print(f"{'='*90}")
print(f"{'Coin':<6} | {'Turtle 20/10':<22} | {'Turtle 55/20':<22} | {'RSI Cross 50':<22}")
print(f"{'':6} | {'Return   L  S  WR':<22} | {'Return   L  S  WR':<22} | {'Return   L  S  WR':<22}")
print(f"{'-'*90}")

results = {'t1': [], 't2': [], 'rsi': []}

for coin, data in all_data.items():
    t1, t1_tr = turtle_both(20, 10, data)
    t2, t2_tr = turtle_both(55, 20, data)
    rc, rc_tr = rsi_cross_both(data)

    w1 = len([t for t in t1_tr if t['pn'] > 0]) / max(1, len(t1_tr)) * 100
    w2 = len([t for t in t2_tr if t['pn'] > 0]) / max(1, len(t2_tr)) * 100
    wr = len([t for t in rc_tr if t['pn'] > 0]) / max(1, len(rc_tr)) * 100

    l1 = len([t for t in t1_tr if t['dir'] == 'LONG'])
    s1 = len([t for t in t1_tr if t['dir'] == 'SHORT'])
    l2 = len([t for t in t2_tr if t['dir'] == 'LONG'])
    s2 = len([t for t in t2_tr if t['dir'] == 'SHORT'])
    lr = len([t for t in rc_tr if t['dir'] == 'LONG'])
    sr = len([t for t in rc_tr if t['dir'] == 'SHORT'])

    r1 = (t1 / 50 - 1) * 100
    r2 = (t2 / 50 - 1) * 100
    rr = (rc / 50 - 1) * 100

    results['t1'].append(t1)
    results['t2'].append(t2)
    results['rsi'].append(rc)

    print(f"{coin:<6} | ${t1:.2f} ({r1:+.0f}%) L:{l1} S:{s1} {w1:.0f}% | ${t2:.2f} ({r2:+.0f}%) L:{l2} S:{s2} {w2:.0f}% | ${rc:.2f} ({rr:+.0f}%) L:{lr} S:{sr} {wr:.0f}%")

print(f"{'-'*90}")
avg1 = sum(results['t1']) / len(results['t1'])
avg2 = sum(results['t2']) / len(results['t2'])
avgr = sum(results['rsi']) / len(results['rsi'])
print(f"{'AVG':<6} | ${avg1:.2f} ({avg1/50-1)*100:+.0f}%             | ${avg2:.2f} ({avg2/50-1)*100:+.0f}%             | ${avgr:.2f} ({avgr/50-1)*100:+.0f}%")

print(f"\nNote: Turtle = buy at N-high breakout, sell at M-low exit (classic system)")
print(f"      RSI Cross 50 = buy when RSI crosses above 50, sell when below 50")
print(f"      All use 2:1 R:R | Initial: $50 | No fees included")
