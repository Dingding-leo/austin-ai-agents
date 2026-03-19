# BTC Futures Trading System — v3
## Modern Price Action + Multi-Timeframe + Turtle (Both Sides) + RSI Cross 50

**Version 3.0 | March 20, 2026**
**Account: $50 USDT | Exchange: OKX | Product: USDT-Margined Perpetual Swaps**

---

## CHANGES FROM v2 → v3

### What Changed:
1. **Turtle Strategy: BOTH Long AND Short** — v2 only tested longs, this is wrong
2. **Short Selling Now Included** — crucial for bear markets
3. **Multi-Timeframe Confirmation** — Daily trend + 4H entry
4. **Improved Position Sizing** — volatility-adjusted ATR method
5. **Better Stop Loss Placement** — based on structure, not arbitrary %

---

## PART 1: THE TWO STRATEGIES

### Strategy 1: TURTLE (Classic Breakout — Both Sides)

**Rules:**
- **LONG**: Price breaks ABOVE highest high of last 20 candles (4H) → enter
- **SHORT**: Price breaks BELOW lowest low of last 20 candles (4H) → enter
- **Exit**: Price hits exit-period low (10 candles) OR 2:1 R:R
- **Stop Loss**: Beyond the breakout candle's structure

**Parameters:**
- Entry period: 20 (4H candles = 5 days)
- Exit period: 10 (4H candles = 2.5 days)
- R:R: 2:1

### Strategy 2: RSI Cross 50 (Momentum — Both Sides)

**Rules:**
- **LONG**: RSI crosses ABOVE 50 (momentum shifting bullish) → enter
- **SHORT**: RSI crosses BELOW 50 (momentum shifting bearish) → enter
- **Exit Long**: RSI hits 65 OR 2:1 R:R
- **Exit Short**: RSI hits 35 OR 2:1 R:R
- **Stop Loss**: 2% below/above entry

---

## PART 2: POSITION SIZING

### ATR-Based Dynamic Sizing

```
Account: $50 USDT
Risk per trade: 1% = $0.50 max loss
Leverage: 5x
ATR(14) on 4H = ~$1,200 (approximate)

Position = Risk Amount / (ATR × Multiplier)
Position = $0.50 / ($1,200 × 1.5) = 0.00028 BTC ($19 notional)
Margin (5x) = $3.80
```

### Simplified Version for $50 Account:
```
Base position: $50 notional (1x account)
High confidence: $75-$100 notional (1.5x-2x account)
Leverage: 5x
Max margin used: $20 (40% of account)
```

---

## PART 3: MULTI-TIMEFRAME ANALYSIS

### Daily TF (Trend Direction)
```
Check:
- Price > EMA20 = Uptrend (only take LONG)
- Price < EMA20 = Downtrend (only take SHORT)
- EMA20 > EMA50 = Confirmed trend
```

### 4H TF (Entry Timing)
```
For LONG:
- Daily: Uptrend confirmed
- 4H: Price near support OR pullback to EMA20
- RSI Cross 50 from below = entry trigger

For SHORT:
- Daily: Downtrend confirmed  
- 4H: Price near resistance OR rally to EMA20
- RSI Cross 50 from above = entry trigger
```

---

## PART 4: MARKET CONTEXT FILTER

### Before ANY Trade, Check:
```
1. Daily Trend (above/below EMA20) — direction filter
2. 4H RSI (not overbought/oversold at entry)
3. Funding Rate (avoid > 0.05% — squeeze risk)
4. No major news in next 4 hours
5. DXY direction (if DXY > 105, be careful on longs)
```

---

## PART 5: ENTRY RULES

### Turtle Entry:
```
LONG:
- Daily uptrend confirmed
- 4H: Price breaks above 20-period high
- Wait for pullback to validate breakout
- Entry on pullback retest

SHORT:
- Daily downtrend confirmed
- 4H: Price breaks below 20-period low
- Wait for rally to validate breakdown
- Entry on rally retest
```

### RSI Cross 50 Entry:
```
LONG:
- Daily: Above EMA20
- 4H: RSI crosses above 50
- Entry on close of crossing candle
- Stop below recent swing low

SHORT:
- Daily: Below EMA20
- 4H: RSI crosses below 50
- Entry on close of crossing candle
- Stop above recent swing high
```

---

## PART 6: EXIT RULES

```
STOP LOSS: 2% from entry (fixed, never widen)
TAKE PROFIT: 4% from entry (2:1 R:R)

Trailing Stop (if +2% quickly):
- Move SL to breakeven after +1%
- Take 50% at +2%, let 50% run

Time Stop:
- Exit if no movement after 24 hours
```

---

## PART 7: COIN SELECTION

### Primary (Most Liquid):
- BTC-USDT-SWAP ✅
- ETH-USDT-SWAP ✅

### Secondary (Higher Beta):
- SOL-USDT-SWAP
- ARB-USDT-SWAP
- AVAX-USDT-SWAP

### Avoid:
- Coins with >5% 24h move (overextended)
- Coins with pending news/events
- Coins with funding > 0.05%

---

## PART 8: CURRENT MARKET STATUS (Mar 20, 2026)

*To be filled by scanner*

---

## PART 9: BACKTEST RESULTS (v3 Update)

*Results from 8-coin backtest with both long and short*

---

## PART 10: DAILY LOG

### Mar 20, 2026
- System v3 built
- Turtle now includes shorts
- RSI Cross 50 confirmed as best single strategy
- Waiting for OKX rate limit to clear

*Status: LIVE — monitoring for signals*
