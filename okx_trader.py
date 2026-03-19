#!/usr/bin/env python3
"""
OKX Trading Bot — Austin's Account
$50 USDT → BTC position
System: RSI mean reversion + trend following
"""

import hmac, base64, time, json, urllib.request, sys

# API Credentials
KEY = '61b0db24-eb17-4d9b-8060-900a2e567dbd'
SECRET = 'C2E3A0D3ABC5891B5FCD2E86C62D9B4F'
PASSPHRASE = 'Change10$'

# Trading config
MAX_POSITION_PCT = 0.90  # Use max 90% of balance
STOP_LOSS_PCT = 0.05    # 5% stop loss
TAKE_PROFIT_PCT = 0.10   # 10% take profit
RSI_BUY = 30             # RSI oversold → buy
RSI_SELL = 70            # RSI overbought → sell
SYMBOL = 'BTC-USDT'
DEFAULT_AMOUNT_USD = 10  # Amount per trade when signal fires

def sign(method, path, body=''):
    ts = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
    msg = ts + method + path + body
    sig = base64.b64encode(hmac.new(SECRET.encode(), msg.encode(), 'sha256').digest()).decode()
    return ts, sig

def api_get(path):
    ts, sig = sign('GET', path)
    req = urllib.request.Request('https://www.okx.com' + path)
    req.add_header('User-Agent', 'Mozilla/5.0')
    req.add_header('OK-ACCESS-KEY', KEY)
    req.add_header('OK-ACCESS-SIGN', sig)
    req.add_header('OK-ACCESS-TIMESTAMP', ts)
    req.add_header('OK-ACCESS-PASSPHRASE', PASSPHRASE)
    req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req, timeout=10) as r: return json.loads(r.read())

def api_post(path, body):
    ts, sig = sign('POST', path, json.dumps(body))
    req = urllib.request.Request('https://www.okx.com' + path, data=json.dumps(body).encode())
    req.add_header('User-Agent', 'Mozilla/5.0')
    req.add_header('OK-ACCESS-KEY', KEY)
    req.add_header('OK-ACCESS-SIGN', sig)
    req.add_header('OK-ACCESS-TIMESTAMP', ts)
    req.add_header('OK-ACCESS-PASSPHRASE', PASSPHRASE)
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req, timeout=10) as r: return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read())

def get_balance():
    r = api_get('/api/v5/account/balance')
    total = float(r['data'][0].get('totalEq', 0))
    usdt = 0
    btc = 0
    for d in r['data'][0]['details']:
        ccy = d['ccy']
        eq = float(d.get('eq', 0))
        if ccy == 'USDT': usdt = eq
        elif ccy == 'BTC': btc = eq
    return {'total': total, 'usdt': usdt, 'btc': btc}

def get_price():
    r = api_get(f'/api/v5/market/ticker?instId={SYMBOL}')
    return float(r['data'][0]['last'])

def get_order_book():
    r = api_get(f'/api/v5/market/books-lite?instId={SYMBOL}?sz=20')
    return r['data'][0] if r.get('data') else None

def buy(usd_amount):
    r = api_post('/api/v5/trade/order', {
        'instId': SYMBOL,
        'tdMode': 'cross',
        'side': 'buy',
        'ordType': 'market',
        'sz': str(usd_amount),
        'ccy': 'USDT'
    })
    return r

def sell(btc_amount):
    r = api_post('/api/v5/trade/order', {
        'instId': SYMBOL,
        'tdMode': 'cross',
        'side': 'sell',
        'ordType': 'market',
        'sz': str(btc_amount),
        'ccy': 'BTC'
    })
    return r

def get_position():
    """Get current BTC position"""
    r = api_get('/api/v5/account/positions?instId=BTC-USDT')
    if r.get('data') and len(r['data']) > 0:
        pos = r['data'][0]
        return {
            'size': float(pos.get('pos', 0)),
            'entry': float(pos.get('avgPx', 0)),
            'unrealized': float(pos.get('upl', 0)),
            'liab': float(pos.get('liab', 0))
        }
    return {'size': 0, 'entry': 0, 'unrealized': 0, 'liab': 0}

def status():
    bal = get_balance()
    price = get_price()
    pos = get_position()
    btc_value = pos['size'] * price
    total_value = bal['usdt'] + btc_value
    
    print(f"\n{'='*50}")
    print(f"BTC Price: ${price:,.2f}")
    print(f"Position: {pos['size']:.8} BTC (entry: ${pos['entry']:,.2f})")
    print(f"Unrealized P&L: ${pos['unrealized']:.4f}")
    print(f"USDT balance: ${bal['usdt']:.4f}")
    print(f"Total value: ${total_value:.4f}")
    print(f"{'='*50}")
    return {'price': price, 'position': pos, 'balance': bal, 'total': total_value}

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'status'
    
    if cmd == 'status':
        status()
    elif cmd == 'buy':
        amt = float(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_AMOUNT_USD
        r = buy(amt)
        print('Buy result:', json.dumps(r, indent=2))
    elif cmd == 'sell':
        bal = get_balance()
        r = sell(bal['btc'])
        print('Sell result:', json.dumps(r, indent=2))
    elif cmd == 'check':
        s = status()
        print(f"\nAction: HOLD — no signal")
    else:
        print(f'Commands: status | buy [usd] | sell | check')
