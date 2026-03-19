# OKX Systematic Trading Framework

## Overview

A complete trading system for Austin's $50 USDT account on OKX using BTC-USDT perpetual swaps.
High leverage (5-10x), small margin, notional size 1-2x account size, risk max 1% per trade.

---

## Part 1: Position Sizing

### Rules
- **Account size:** $50 USDT
- **Risk per trade:** Max 1% of account = $0.50
- **Leverage:** 5-10x (high leverage, low margin)
- **Notional size:** 1-2x account = $50-$100 per trade
- **Max contracts:** 1-2 contracts (0.01 BTC each = $692-$1380 notional at $69k BTC)

### Calculation
```
Account = $50
Risk = $0.50 (1%)
Stop Loss = 1% of entry price
Leverage = 5-10x

Position = Risk / Stop Loss %
Position = $0.50 / 0.01 = $50 notional (1x)
Position = $0.50 / 0.005 = $100 notional (2x)

With 10x leverage:
Margin required = $50 / 10 = $5 (10% of account)
```

### Entry Example
- BTC price: $69,500
- Entry: LONG @ $69,500
- Notional: $50 (1x account)
- Margin: $5 (10x leverage)
- Stop loss: $68,805 (-1% from entry)
- Take profit: $70,195 (+1% from entry)
- Liquidation: $62,550 (only if BTC drops 10%)

---

## Part 2: Macro Economic Analysis

### Weekly Checklist (Before Any Trade)

#### 2.1 Federal Reserve Policy
- [ ] Fed rate decision: HOLD / HIKE / CUT
- [ ] Fed statement tone: HAWKISH / NEUTRAL / DOVISH
- [ ] Dot plot projections: rate cut expectations
- [ ] Impact on BTC: NEGATIVE / NEUTRAL / POSITIVE

**Key rules:**
- Rate HIKE = Risk-off = BTC down
- Rate CUT = Risk-on = BTC up
- Rate HOLD with hawkish tone = BTC mixed

#### 2.2 US Economic Data
| Indicator | Frequency | Impact on BTC |
|---|---|---|
| CPI (inflation) | Monthly | High — hot CPI = rate hikes = BTC down |
| NFP (jobs) | Monthly | High — strong jobs = rate hikes = BTC down |
| GDP | Quarterly | Medium |
| PMI | Monthly | Medium |
| Retail Sales | Monthly | Low |

**Rule:** If CPI > 3% AND NFP > 200K → DON'T LONG BTC

#### 2.3 Global Liquidity
- [ ] US Dollar Index (DXY): Stronger = BTC weaker
- [ ] Treasury yields (2Y, 10Y): Rising = BTC mixed
- [ ] Global central bank policy: Easing = BTC up

**Rule:** DXY > 105 → Reduce BTC position or don't enter new longs

#### 2.4 Crypto-Specific Macro
- [ ] Bitcoin halving cycle position (where are we in 4-year cycle)
- [ ] ETF inflows/outflows (BlackRock, Fidelity BTC funds)
- [ ] Institutional adoption news

**Current context (Mar 2026):**
- Fed held rates → BTC dropped 5% (risk-off)
- Inflation forecasts rising → more rate pressure
- DXY strengthening → headwind for BTC
- BTC ETF flows: need to check daily

---

## Part 3: Market Sentiment

### 3.1 Fear & Greed Index
- Source: alternative.me/fear-and-greed-index/
- **Rule:** Below 30 (Extreme Fear) = potential long entry
- **Rule:** Above 80 (Extreme Greed) = potential exit / reversal

### 3.2 Funding Rates (OKX/Bybit/Binance)
- **Rule:** Funding > 0.01% per 8h (bullish funding) = many long positions = correction risk
- **Rule:** Funding < -0.01% per 8h (bearish funding) = many shorts = squeeze risk
- **Rule:** Neutral funding (-0.01% to +0.01%) = healthy market

### 3.3 Open Interest
- [ ] OI rising + price rising = bullish confirmation
- [ ] OI falling + price rising = short covering (reversal risk)
- [ ] OI rising + price falling = capitulation incoming

### 3.4 Long/Short Ratio
- OKX: Long/Short ratio > 1.2 = too many longs = squeeze risk
- OKX: Long/Short ratio < 0.8 = too many shorts = squeeze long risk

---

## Part 4: On-Chain Flow Analysis

### 4.1 Exchange Flows
- [ ] Net flow to exchanges (CoinGlass/Glassnode): Positive = selling pressure
- [ ] Net flow from exchanges: Negative = accumulation

**Rule:** If exchange wallets receiving massive BTC → expect selling pressure

### 4.2 Whale Activity
- [ ] Large BTC wallets (>100 BTC) accumulating or distributing
- [ ] Exchange whale deposits (>100 BTC coming to exchanges = selling)
- [ ] Watch for wallet clusters: support/resistance from whale levels

### 4.3 Stablecoin Flow
- [ ] USDT market cap growth: More USDT = potential buying power
- [ ] Stablecoin flows into exchanges: Buying pressure
- [ ] Stablecoin flows out: Selling pressure

### 4.4 Realized Cap / MVRV
- [ ] MVRV < 2.5 = undervalued
- [ ] MVRV > 3.5 = overvalued
- [ ] Realized price vs current price spread

---

## Part 5: Market Structure

### 5.1 Trend Analysis
**Multi-Timeframe Approach:**

**Daily TF:**
- [ ] BTC above or below EMA 20? → Trend direction
- [ ] BTC above or below EMA 50? → Medium trend
- [ ] 200 EMA as final trend filter

**Rule:** Only trade in direction of higher timeframe trend
- Daily uptrend → only LONG
- Daily downtrend → only SHORT or NO TRADE

### 5.2 Range Identification
- [ ] BTC in consolidation range? → Buy near support, sell near resistance
- [ ] Range width: >5% of price = significant range
- [ ] Volume profile: High vol at support/resistance = confirmed levels

### 5.3 Support & Resistance
**Identify:**
- [ ] Horizontal S/R levels (check 4H, Daily, Weekly)
- [ ] Trendline S/R
- [ ] Fib retracement levels (0.382, 0.5, 0.618)
- [ ] Round numbers ($70,000, $65,000, $60,000)

### 5.4 Order Block Analysis
- [ ] Identify recent order blocks on 4H/Daily
- [ ] Order blocks followed by displacement = high probability trades

---

## Part 6: Technical Analysis

### 6.1 Indicators
| Indicator | Use | Signal |
|---|---|---|
| RSI(14) | Overbought/Oversold | <30 = buy, >70 = sell |
| MACD | Trend/Momentum | Histogram flip = entry |
| EMA 20/50 | Trend | Cross = direction |
| VWAP | Fair value | Price above = bullish |
| Bollinger Bands | Volatility | Squeeze = breakout coming |

### 6.2 Entry Signals (Require ALL)
1. [ ] Macro: No major risk events next 24h
2. [ ] Sentiment: Funding neutral or favorable
3. [ ] Structure: Price near support (for longs) or resistance (for shorts)
4. [ ] Technical: RSI + MACD confirm entry direction
5. [ ] Trend: Aligned with higher timeframe direction

### 6.3 Exit Rules
- **Take profit:** +1% to +2% (small targets for high leverage)
- **Stop loss:** -1% from entry (hard stop, never widen)
- **Time stop:** Exit if no movement in 4 hours
- **Trailing stop:** Move stop to breakeven after +0.5% profit

---

## Part 7: Liquidation Analysis

### 7.1 Liquidation Heatmap
- [ ] Check Binance/Bybit/OKX liquidation heatmap
- [ ] Clusters below/above price = magnetic levels
- [ ] Large walls = potential support/resistance

**Rule:** If large liquidation cluster above price, expect resistance at that level

### 7.2 Liquidation Levels
- [ ] Estimated long liquidation level: Below entry
- [ ] Estimated short liquidation level: Above entry
- [ ] Total long/short liquidation zones (CoinGlass)

**Rule:** Don't enter if you're placing stop just below/above major liquidation cluster

---

## Part 8: Daily Pre-Trade Checklist

### Before Every Trade:
```
□ 1. Macro: Fed policy? No high-impact news in next 24h?
□ 2. DXY: Below 105 for longs?
□ 3. Funding rates: Neutral (-0.01% to +0.01%)?
□ 4. Fear & Greed: Not Extreme Greed (not > 80)?
□ 5. Trend: Aligned with daily TF direction?
□ 6. Entry: Near support (longs) or resistance (shorts)?
□ 7. RSI: < 40 for longs, > 60 for shorts?
□ 8. No major exchange maintenance?
□ 9. Weekend check: Lower volume = wider stops
□ 10. Position size: Does max loss = < $0.50 (1% of $50)?
```

---

## Part 9: Trade Execution

### Entry Order
```
Symbol: BTC-USDT-SWAP
Type: MARKET (enter immediately) or LIMIT (better price)
Side: BUY (long) / SELL (short)
Notional: $50-$100
Leverage: 5-10x
```

### Attach Stop Loss Immediately After Entry
```
Type: STOP
Side: SELL (for long) / BUY (for short)
Price: Entry - 1%
```

### Attach Take Profit
```
Type: TAKE PROFIT
Side: SELL (for long) / BUY (for short)
Price: Entry + 1% to +2%
```

---

## Part 10: Risk Management Rules

1. **Max 1% risk per trade** — $0.50 on $50 account
2. **Max 3 trades per day** — No overtrading
3. **Daily max loss 3%** — Stop trading if -$1.50 in one day
4. **Never average down** — If trade goes wrong, exit
5. **Always attach SL before entry** — Never trade without stop
6. **No news trades** — Don't enter 30 min before/after major news
7. **Weekend rule** — Reduce size 50%, wider stops (crypto illiquid weekends)

---

## Part 11: Current Market Assessment (Mar 19, 2026)

### Macro
- Fed held rates → BTC dropped 5% → Bearish
- Inflation forecasts rising → More pressure → Bearish
- DXY strengthening → BTC headwind

### Sentiment
- Fear & Greed: Extreme Fear (confirm)
- Funding: Need to check
- Trend: Below EMA 20, EMA 50 → DOWNTREND

### Technical
- BTC: ~$69,500
- Below EMA 20 and EMA 50 → Bearish
- RSI: Need to check (likely around 40-50 = neutral)
- Range: Was $88k-$90k top, now dropping

### Assessment: **NO TRADE**
- Market in clear downtrend
- Macro headwinds
- Only consider LONG when:
  1. Fed turns dovish OR
  2. BTC holds $65,000-$67,000 support AND
  3. RSI drops below 30 (oversold) AND
  4. Funding turns negative (short squeeze potential)

---

## Part 12: Research Areas to Develop

### Still Need to Research:
- [ ] BTC correlation with tech stocks ( Nasdaq)
- [ ] BTC correlation with gold
- [ ] Option flow impact on BTC price
- [ ] Futures basis / contango analysis
- [ ] On-chain metric: SOPR (Spent Output Profit Ratio)
- [ ] On-chain metric: Stock-to-Flow model
- [ ] Mempool congestion and fee analysis
- [ ] Lightning Network capacity as macro signal
- [ ] Bitcoin dominance chart for altcoin season

---

*Version 1.0 | Mar 19, 2026 | Austin's Systematic Trading System*
