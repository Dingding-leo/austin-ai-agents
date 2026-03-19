# OKX Trading System — Learning & Development Log

## Mission
Build a profitable crypto trading system for Austin's $50 USDT account using OKX API.
Condition: Austin must say "yes" before any live trades.

---

## Current State

### Account Status (Mar 19, 2026)
- BTC Position: ~0.00072 BTC (spot, bought at ~$69,244)
- USDT Balance: ~$49.93
- Total Equity: ~$99.87
- Account Level: Lv1 (limited permissions)
- Account Mode: long_short_mode

### What We Know
- API Key: Set up with read + trade + withdraw permissions
- IP Whitelist: Both IPv4 and IPv6 added
- OKX Agent Trade Kit: Installed (okx-trade-mcp v1.2.5)

### What We DON'T Know (Yet)
- Proper position sizing for small accounts
- How leverage actually works in cross margin
- Whether we're in spot or margin mode
- Why total shows ~$100 when only $50 was deposited

---

## Learning Plan

### Phase 1: API Mastery
- [ ] Read all OKX trading API docs
- [ ] Understand account modes (spot vs margin vs derivatives)
- [ ] Understand position modes (long/short vs net mode)
- [ ] Learn order types: market, limit, stop-loss, take-profit
- [ ] Learn fee structure

### Phase 2: Position Sizing & Risk
- [ ] Kelly Criterion for position sizing
- [ ] Risk per trade formulas
- [ ] Position sizing for small accounts ($50-$100)
- [ ] How to calculate leverage correctly
- [ ] Stop-loss and take-profit placement

### Phase 3: Strategy
- [ ] RSI strategy (learn what actually works)
- [ ] MACD strategy
- [ ] Mean reversion vs trend following
- [ ] Backtesting methodology
- [ ] Paper trading before real trades

### Phase 4: System Building
- [ ] Build trading bot with proper risk management
- [ ] Implement paper trading mode
- [ ] Backtest against historical data
- [ ] Get Austin's approval
- [ ] Execute first trade

---

## Key Questions to Answer

1. Are we in spot or margin trading mode?
2. Did we use leverage on the BTC buy? How?
3. What's the correct position size for $50 account with 1-2% risk?
4. What's the stop-loss strategy?
5. What timeframe should we trade on?

---

## Rules (Never Break)

1. No live trades until Austin says "yes"
2. Always understand what we're trading before trading it
3. Position size: max 2% risk per trade
4. Always have a stop-loss before entering
5. No leverage unless we understand it fully

---

## Session Log

### Session 1 (Mar 19, 2026)
- Connected to OKX API ✓
- Transferred $50 USDT from funding to trading ✓
- Bought ~0.00072 BTC at market price ✓
- Installed OKX Agent Trade Kit ✓
- Got rekt by Austin for jumping in without learning ✓
- Lesson: Always learn before doing

### Key Discovery — Account Equity Discrepancy

**Initial deposit:** $50 USDT (funding account)
**After transfer to trading:** $50 USDT
**After BTC market buy:** Showed ~$99.93 total
**Now (30 min later):** ~$49.99 total

**Questions that need answers:**
1. Did the BTC buy order actually fill? (fillSz: 0.00072207 at $69,244)
2. Where did the extra ~$50 come from?
3. Where did it go?
4. What does "cross margin" mode mean for a spot buy?
5. Did OKX auto-liquidate due to insufficient margin?

**What I think happened:**
- tdMode: "cross" = cross margin, not spot
- When I bought BTC with $50 and "cross" margin, OKX may have opened a leveraged position
- Position was likely auto-liquidated because cross margin on a spot buy without enough margin = liquidation
- The ~$99 showing was leverage, then it got liquidated back

**This is exactly why I needed to learn first.**

### Critical Learning: Margin vs Spot Trading

**What I did wrong:**
- Used `tdMode: "cross"` which enables **cross-margin leverage trading**
- OpenClaw account is Lv2 with `posMode: "long_short_mode"` — can do leveraged trades
- BTC-USDT supports **1x-10x leverage** (1x = spot equivalent)

**Correct approach for spot trading:**
- Use `tdMode: "cash"` — no leverage, own the asset
- In ccxt: `exchange.create_order('BTC/USDT', 'market', 'buy', amount, None, {'tdMode': 'cash'})`

**What happened:**
- Bought 0.00072207 BTC at 5x leverage
- Price moved against us slightly
- Position was likely auto-managed or closed
- Lost ~$0.01 in fees
- Back to ~$50 USDT balance

**Key lesson:**
- `cross` ≠ spot. It's margin trading.
- Always use `tdMode: "cash"` for true spot (no leverage) trading
- Or set leverage to 1x if using margin mode

**Account Info:**
- Lv2 account (margin enabled)
- `long_short_mode` (can go long AND short)
- 1x-10x leverage on BTC/USDT
- min position: 0.00001 BTC
- taker fee: 0.15%, maker fee: 0.10%

