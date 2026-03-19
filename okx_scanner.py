import json
import urllib.request
import time

BASE_URL = 'https://www.okx.com/api/v5'

class MarketScanner:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def _get(self, url):
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return json.loads(r.read())
        except: return {}

    def get_ticker(self, instId='BTC-USDT'):
        r = self._get(f'{BASE_URL}/market/ticker?instId={instId}')
        if 'data' in r and r['data']:
            d = r['data'][0]
            return {
                'last': float(d['last']), 'bid': float(d['bidPx']),
                'ask': float(d['askPx']), 'high24h': float(d['high24h']),
                'low24h': float(d['low24h']), 'vol24h': float(d['vol24h']),
                'change_pct': (float(d['last']) - float(d['sodUtc0'])) / float(d['sodUtc0']) * 100
            }
        return {}

    def get_ohlc(self, instId='BTC-USDT', bar='4H', limit=100):
        r = self._get(f'{BASE_URL}/market/history-candles?instId={instId}&bar={bar}&limit={limit}')
        if 'data' in r and r['data']:
            candles = []
            for c in reversed(r['data']):
                candles.append({
                    'ts': int(c[0]), 'open': float(c[1]), 'high': float(c[2]),
                    'low': float(c[3]), 'close': float(c[4]), 'vol': float(c[5])
                })
            return candles
        return []

    def get_funding(self):
        r = self._get(f'{BASE_URL}/public/funding-rate?instId=BTC-USDT-SWAP')
        if 'data' in r and r['data']:
            return float(r['data'][0]['fundingRate']) * 100
        return 0

    def calc_rsi(self, prices, period=14):
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

    def calc_ema(self, data, period):
        k = 2/(period+1)
        result = [data[0]]
        for d in data[1:]: result.append(d * k + result[-1] * (1-k))
        return result

    def scan(self, coin='BTC-USDT'):
        print(f"\n{'='*65}")
        print(f"OKX SCAN — {coin} | {time.strftime('%Y-%m-%d %H:%M UTC')}")
        print(f"{'='*65}")

        btc = self.get_ticker(coin)
        funding = self.get_funding() if coin == 'BTC-USDT' else 0
        candles = self.get_ohlc(coin, '4H', 100)

        if not candles or not btc:
            print("Error fetching data")
            return 'ERROR', 0

        closes = [c['close'] for c in candles]
        rsi = self.calc_rsi(closes, 14)
        rsi_offset = len(closes) - len(rsi)
        ema20 = self.calc_ema(closes, 20)
        ema50 = self.calc_ema(closes, 50)

        price = closes[-1]
        rsi_curr = rsi[-1] if rsi else 50
        rsi_prev = rsi[-2] if len(rsi) > 1 else 50

        rsi_cross_up = rsi_prev <= 50 and rsi_curr > 50
        rsi_cross_down = rsi_prev >= 50 and rsi_curr < 50
        trend_up = price > ema20[-1] if len(ema20) > 0 else False
        trend_up_50 = price > ema50[-1] if len(ema50) > 0 else False

        print(f"Price: ${price:,.2f} ({btc.get('change_pct', 0):+.2f}% 24h)")
        if funding: print(f"Funding: {funding:+.4f}% ({'✅ neutral' if abs(funding) < 0.02 else '⚠️ HIGH'})")
        print(f"RSI(14): {rsi_curr:.1f} | EMA20: ${ema20[-1]:,.0f} | EMA50: ${ema50[-1]:,.0f}")
        print(f"Trend: {'UP ⬆️' if trend_up_50 else 'DOWN ⬇️'}")

        verdict = 'NO SIGNAL'
        if rsi_cross_up and trend_up_50:
            verdict = 'STRONG LONG ✅'
            sl = price * 0.98
            tp = price * 1.04
            print(f"\n🟢 {verdict}: RSI crossed 50 + above EMA50")
            print(f"   Entry: ${price:,.2f} | SL: ${sl:,.2f} (-2%) | TP: ${tp:,.2f} (+4%)")
        elif rsi_cross_up:
            verdict = 'LONG (LOW CONF) 🟡'
            sl = price * 0.98
            tp = price * 1.04
            print(f"\n🟡 {verdict}: RSI crossed 50 but below EMA50")
            print(f"   Entry: ${price:,.2f} | SL: ${sl:,.2f} (-2%) | TP: ${tp:,.2f} (+4%)")
        elif rsi_cross_down and not trend_up_50:
            verdict = 'SHORT 🔴'
            sl = price * 1.02
            tp = price * 0.96
            print(f"\n🔴 {verdict}: RSI crossed 50 from above + below EMA50")
            print(f"   Entry: ${price:,.2f} | SL: ${sl:,.2f} (+2%) | TP: ${tp:,.2f} (-4%)")
        elif rsi_curr < 30:
            print(f"\n🟡 WAIT — RSI oversold ({rsi_curr:.1f}), need cross above 50")
        elif rsi_curr > 70:
            print(f"\n🟡 WAIT — RSI overbought ({rsi_curr:.1f})")
        else:
            print(f"\n🟡 NO SIGNAL — RSI neutral ({rsi_curr:.1f})")

        if coin == 'BTC-USDT' and funding > 0.03:
            print(f"⚠️ WARNING: High funding ({funding:.4f}%)")

        return verdict, price

if __name__ == '__main__':
    s = MarketScanner()
    print("="*65)
    print("OKX LIVE TRADING SCANNER — DATA-DRIVEN SIGNALS")
    print("Strategy: RSI Cross 50 + EMA confirmation | 4H TF")
    print("="*65)

    v, p = s.scan('BTC-USDT')

    print(f"\n{'='*65}")
    print("ALT COINS")
    print(f"{'='*65}")
    for coin in ['ETH-USDT', 'SOL-USDT', 'ARB-USDT', 'AVAX-USDT', 'LINK-USDT', 'DOGE-USDT']:
        try: s.scan(coin)
        except: pass
