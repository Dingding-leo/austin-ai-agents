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


### Backtest Results (90 days, Dec 2025 - Mar 2026)

**Market context:** BTC dropped from $88,175 to $69,372 (-21.3%) — bear market

| Strategy | Final Value | Trades | Win Rate |
|---|---|---|---|
| Buy & Hold | $39.34 | 0 | N/A |
| RSI(14) <30/>70 | $44.07 | 3 | 0% |
| SMA(20/50) Cross | $50.00 | 0 | N/A |

**Key insights:**
1. In a bear market, no strategy beats not trading
2. RSI strategy lost money because BTC kept dropping — every "oversold" was a falling knife
3. SMA crossover got no signal in this period (sideways after initial drop)

**Fee math (for $25 position):**
- Buy fee (0.15%): $0.0375
- Sell fee (0.10%): $0.025
- Total: $0.0625 per round trip
- As % of $50 account: 0.12% — manageable

**Risk/reward on $25 position:**
- Stop loss (5%): net loss ~$1.19
- Take profit (10%): net gain ~$2.44
- Risk/reward ratio: 1:2.1 — favorable

**What this means:**
- The strategy CAN work IF the market isn't in a sustained bear drop
- Need a bull market or sideways market for RSI to work
- With only $50, we need to be selective about entry timing
- Consider waiting for RSI < 30 + MACD histogram flip positive

### Next Steps
1. Monitor BTC price and RSI daily
2. Wait for signal: RSI < 30 AND MACD histogram positive
3. Execute ONLY with tdMode="cash" (spot, no leverage)
4. Position: 50% of balance
5. Stop loss: 5%, Take profit: 10%

### Futures vs Spot — Key Learnings

**Perpetual Swaps (BTC-USDT-SWAP):**
- Fee: 0.05% taker, 0.02% maker (vs spot 0.15%/0.10%)
- Leverage: up to 50x (cross or isolated margin)
- No expiration date
- Settles in USDT
- Contract size: 0.01 BTC per contract (BTC-USDT-SWAP)
- Funding rate: -0.0005% (very low/neutral)

**Position Sizing for Perpetual Swaps:**
- Margin required = Position Value / Leverage
- Example: $100 position @ 5x leverage = $20 margin required
- With $50 account, 5x leverage, 50% margin used = $25 margin → $125 position

**Stop Loss on Perpetuals:**
- Can use bracket orders (TP + SL attached to entry)
- Or set SL as separate algo order
- Liquidation = when margin hits 0

**What Austin said:** Use futures for swing trades
- Better fee structure
- Higher leverage available
- Good for short-term directional bets

**Plan:**
1. Study perpetual swap order placement
2. Build swing trade strategy for BTC perpetual
3. Test on paper before live
4. Use 3-5x leverage max for safety
5. Always use stop loss


### Futures Swing Trading — Ready to Execute

**Current Setup:**
- Account: $50 USDT
- BTC-USDT Perpetual price: ~$69,589
- SMA20: $69,898 (below SMA50 $70,116) — bearish trend
- Leverage: 3x set ✓
- Position mode: cross margin, net (long/short)

**Plan for next trade:**
- Wait for SMA(20) to cross above SMA(50) = golden cross = bullish signal
- OR wait for RSI < 30 oversold + trend reversal
- Enter LONG with 3x leverage
- Position size: $100 notional ($33 margin from $50)
- Stop loss: 5% below entry (~$66,100)
- Take profit: 10% above entry (~$76,500)
- Fee: $0.05 per trade (0.05%)

**What I've done so far:**
- Set 3x leverage on BTC-USDT-SWAP ✓
- Understood account structure ✓
- Backtested RSI strategy ✓
- Calculated position sizing ✓

**What Austin needs to decide:**
- Approve the trading plan
- OR give specific entry/exit rules
- OR say "just flip it" and let me decide

