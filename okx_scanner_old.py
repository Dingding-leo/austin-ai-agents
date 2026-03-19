#!/usr/bin/env python3
"""
OKX Live Market Scanner
Systematic pre-trade analysis for Austin's trading system
"""

import json
import urllib.request
import time
import sys

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
        except Exception as e:
            return {'error': str(e)}
    
    def get_btc_price(self, spot=True):
        inst = 'BTC-USDT' if spot else 'BTC-USDT-SWAP'
        r = self._get(f'{BASE_URL}/market/ticker?instId={inst}')
        if 'data' in r and r['data']:
            d = r['data'][0]
            return {
                'last': float(d['last']),
                'bid': float(d['bidPx']),
                'ask': float(d['askPx']),
                'high24h': float(d['high24h']),
                'low24h': float(d['low24h']),
                'vol24h': float(d['vol24h']),
                'change24h': float(d['sodUtc0']),
                'change_pct24h': (float(d['last']) - float(d['sodUtc0'])) / float(d['sodUtc0']) * 100
            }
        return None
    
    def get_funding_rate(self):
        r = self._get(f'{BASE_URL}/public/funding-rate?instId=BTC-USDT-SWAP')
        if 'data' in r and r['data']:
            d = r['data'][0]
            return {
                'rate': float(d['fundingRate']) * 100,  # as percentage
                'next_funding': d['nextFundingTime']
            }
        return None
    
    def get_orderbook(self, instId='BTC-USDT-SWAP', depth=20):
        r = self._get(f'{BASE_URL}/market/books-lite?instId={instId}&sz={depth}')
        if 'data' in r and r['data']:
            d = r['data'][0]
            bids = [[float(p), float(s)] for p, s in zip(d['bids'][:10], d['bsz'][:10])]
            asks = [[float(p), float(s)] for p, s in zip(d['asks'][:10], d['asz'][:10])]
            return {'bids': bids, 'asks': asks}
        return None
    
    def get_ohlc(self, instId='BTC-USDT', bar='4H', limit=100):
        r = self._get(f'{BASE_URL}/market/history-candles?instId={instId}&bar={bar}&limit={limit}')
        if 'data' in r and r['data']:
            candles = []
            for c in reversed(r['data']):
                candles.append({
                    'ts': int(c[0]),
                    'open': float(c[1]),
                    'high': float(c[2]),
                    'low': float(c[3]),
                    'close': float(c[4]),
                    'vol': float(c[5])
                })
            return candles
        return []
    
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
        return rsi[-1] if rsi else 50
    
    def calc_sma(self, prices, period):
        if len(prices) < period:
            return None
        return sum(prices[-period:]) / period
    
    def run_full_scan(self):
        print("=" * 60)
        print("OKX LIVE MARKET SCAN")
        print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print("=" * 60)
        
        # Price
        btc = self.get_btc_price(spot=True)
        btc_swap = self.get_btc_price(spot=False)
        if btc:
            print(f"\nBTC Price: ${btc['last']:,.2f}")
            print(f"  24h High: ${btc['high24h']:,.2f}")
            print(f"  24h Low: ${btc['low24h']:,.2f}")
            print(f"  24h Change: {btc['change_pct24h']:+.2f}%")
            print(f"  Spot/Ask Spread: ${btc['ask'] - btc['bid']:.2f}")
        
        if btc_swap:
            print(f"\nBTC Perpetual Swap: ${btc_swap['last']:,.2f}")
            print(f"  Premium/Discount to spot: ${btc_swap['last'] - btc['last']:+.2f}")
        
        # Funding
        funding = self.get_funding_rate()
        if funding:
            print(f"\nFunding Rate: {funding['rate']:+.4f}%")
            if funding['rate'] > 0.01:
                print("  ⚠️ HIGH BULLISH FUNDING — many longs, squeeze risk")
            elif funding['rate'] < -0.01:
                print("  ⚠️ HIGH BEARISH FUNDING — many shorts, squeeze potential")
            else:
                print("  ✅ Neutral funding — healthy market")
        
        # RSI (4H)
        candles_4h = self.get_ohlc('BTC-USDT', '4H', 50)
        if candles_4h:
            closes = [c['close'] for c in candles_4h]
            rsi_4h = self.calc_rsi(closes, 14)
            sma20_4h = self.calc_sma(closes, 20)
            sma50_4h = self.calc_sma(closes, 50) if len(closes) >= 50 else None
            
            print(f"\n4H Technical (BTC):")
            print(f"  RSI(14): {rsi_4h:.1f}")
            if rsi_4h < 30:
                print("    ⚠️ OVERSOLD — potential long entry")
            elif rsi_4h > 70:
                print("    ⚠️ OVERBOUGHT — potential exit/short")
            else:
                print("    ✅ Neutral")
            
            if sma20_4h:
                trend = "ABOVE" if closes[-1] > sma20_4h else "BELOW"
                print(f"  Price is {trend} SMA20 (${sma20_4h:,.0f})")
            if sma50_4h:
                trend = "ABOVE" if closes[-1] > sma50_4h else "BELOW"
                print(f"  Price is {trend} SMA50 (${sma50_4h:,.0f})")
        
        # Daily RSI
        candles_d = self.get_ohlc('BTC-USDT', '1D', 30)
        if candles_d:
            closes_d = [c['close'] for c in candles_d]
            rsi_d = self.calc_rsi(closes_d, 14)
            sma20_d = self.calc_sma(closes_d, 20)
            
            print(f"\n1D Technical (BTC):")
            print(f"  RSI(14): {rsi_d:.1f}")
            if sma20_d:
                trend = "ABOVE" if closes_d[-1] > sma20_d else "BELOW"
                print(f"  Price is {trend} SMA20 (${sma20_d:,.0f})")
                print(f"  Trend: {'UP' if closes_d[-1] > sma20_d else 'DOWN'}")
        
        # Entry signals
        print(f"\n{'='*60}")
        print("PRE-TRADE SIGNAL CHECK")
        print("=" * 60)
        
        signals = []
        
        # Macro (hardcoded — need to add live Fed/CPI data)
        print("\nMACRO (manual check):")
        print("  Fed policy: CHECK before trade")
        print("  DXY: CHECK (< 105 for longs)")
        
        # Technical signals
        if rsi_4h < 35:
            signals.append("✅ RSI4H oversold")
        elif rsi_4h > 65:
            signals.append("⚠️ RSI4H overbought")
        
        if btc and btc_swap:
            premium = btc_swap['last'] - btc['last']
            if abs(premium) < 5:
                signals.append("✅ Funding neutral")
            elif premium > 10:
                signals.append("⚠️ High perp premium (correction risk)")
            elif premium < -10:
                signals.append("⚠️ High perp discount (squeeze risk)")
        
        if funding and abs(funding['rate']) < 0.01:
            signals.append("✅ Funding neutral")
        
        for s in signals:
            print(f"  {s}")
        
        # Verdict
        print(f"\n{'='*60}")
        print("TRADE VERDICT")
        print("=" * 60)
        
        long_signals = sum(1 for s in signals if '✅' in s and 'overbought' not in s)
        short_signals = sum(1 for s in signals if '⚠️' in s and 'overbought' in s)
        
        print(f"  Long signals: {long_signals}")
        print(f"  Short signals: {short_signals}")
        
        if long_signals >= 2 and short_signals == 0:
            print("  🟢 SIGNAL: Consider LONG")
        elif short_signals >= 2 and long_signals == 0:
            print("  🔴 SIGNAL: Consider SHORT or NO TRADE")
        else:
            print("  🟡 SIGNAL: NO CLEAR EDGE — WAIT")
        
        print(f"\nAccount: $50 USDT")
        print(f"Max risk: $0.50 (1%)")
        print(f"Recommended notional: $50-100")
        print(f"Max leverage: 5-10x")

if __name__ == '__main__':
    scanner = MarketScanner()
    scanner.run_full_scan()
