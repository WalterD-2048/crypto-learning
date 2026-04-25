# Glassnode On-Chain Metrics: Core Reference Guide

**Compiled from Glassnode Academy (academy.glassnode.com / docs.glassnode.com)**

> These four metrics form the foundation of on-chain market cycle analysis.
> They answer one core question: **Are market participants profitable or not, and by how much?**

---

## 1. Realized Capitalization (Realized Cap)

**Source:** https://academy.glassnode.com/market/realized-capitalization

### What it is

Market Cap values every coin at the **current price**.
Realized Cap values every coin at the **price it last moved on-chain**.

```
Realized Cap = Σ (value of each UTXO × price when that UTXO was created)
```

### Why it matters

- Acts as an estimate of the **aggregate cost basis** of the entire network
- Long-dormant or lost coins are discounted (valued at their last-moved price, often very low)
- More accurately represents **real economic weight** stored in Bitcoin vs. Market Cap
- Serves as the **foundation for MVRV, NUPL**, and many other indicators

### Intuition

If Realized Cap is $400B and Market Cap is $800B, the average coin in circulation was bought at half the current price — the market as a whole is sitting on 2x unrealized profit.

---

## 2. MVRV Ratio (Market Value to Realized Value)

**Source:** https://academy.glassnode.com/market/mvrv/mvrv-ratio

### Formula

```
MVRV = Market Cap / Realized Cap
```

### How to read it

| MVRV Value | Interpretation |
|-----------|---------------|
| > 3.5–4.0 | Historically signals **market top zone** (high unrealized profit → sell pressure) |
| ~1.0 | Coins trading near cost basis — **fair value** |
| < 1.0 | Majority of supply held at a **loss** — signals capitulation / bear market bottom |
| 0.5–0.8 | Historical **deep bottom** territory, strong accumulation signal |

### MVRV-Z Score

A normalized version:
```
MVRV-Z = (Market Cap − Realized Cap) / StdDev(Market Cap)
```
Filters out noise by expressing deviation in standard deviations. Red zone (>7) = historical tops. Green zone (<0) = historical bottoms. Has historically predicted market tops with >90% accuracy when entering red zone.

### LTH-MVRV vs STH-MVRV

- **LTH-MVRV:** Only coins held >155 days (long-term holders). Their behavior signals structural trends.
- **STH-MVRV:** Only coins held <155 days (short-term holders). More sensitive to recent price action; useful for timing entries/exits.

When STH-MVRV drops below 1.0, short-term buyers are underwater — historically precedes local bottoms.

---

## 3. SOPR (Spent Output Profit Ratio)

**Source:** https://academy.glassnode.com/indicators/sopr/sopr-spent-output-profit-ratio

### Formula

```
SOPR = Price when coins were SPENT / Price when coins were CREATED
     = Realized Value / Cost Basis (of all coins moved that day)
```

### How to read it

| SOPR Value | Interpretation |
|-----------|---------------|
| > 1.0 | Coins moved on-chain are, **on average, selling at a profit** |
| = 1.0 | Break-even — coins sold at cost. Key pivot level. |
| < 1.0 | Coins moved are **selling at a loss** (panic, capitulation) |

### Key signals

**Bull market behavior:**
- SOPR stays consistently above 1.0 as holders realize profits
- Dips toward 1.0 often represent **buy-the-dip opportunities** (sellers exhausted)

**Bear market behavior:**
- SOPR repeatedly falls below 1.0 (people selling at losses)
- When SOPR climbs back to 1.0 and gets **rejected** (sellers unload at break-even), that's bearish resistance
- When SOPR **breaks above 1.0 and holds**, potential trend reversal signal

### aSOPR (Adjusted SOPR)

Filters out "same-day" coin movements (very short holds), focusing on economically meaningful transactions. Generally preferred over raw SOPR for signal clarity.

---

## 4. NUPL (Net Unrealized Profit/Loss)

**Source:** https://academy.glassnode.com/indicators/profit-loss-unrealized/net-unrealized-profit-loss

### Formula

```
NUPL = (Market Cap − Realized Cap) / Market Cap
     = Relative Unrealized Profit − Relative Unrealized Loss
```

Range: −1 to +1

### How to read it

| NUPL Zone | Value Range | Market Sentiment | Historical Signal |
|----------|------------|-----------------|------------------|
| Capitulation | < 0 | Net loss | **Bottom zone** — buy signal |
| Hope / Fear | 0 – 0.25 | Recovery | Early accumulation |
| Optimism | 0.25 – 0.5 | Rising confidence | Mid-bull |
| Belief | 0.5 – 0.75 | Strong bull market | Late-bull, watch carefully |
| Euphoria | > 0.75 | Peak greed | **Top zone** — sell signal |

### Relationship to other metrics

NUPL and MVRV tell the same fundamental story from different angles:
- MVRV > 3 corresponds roughly to NUPL entering "Belief/Euphoria" territory
- NUPL < 0 corresponds to MVRV < 1.0

Together with SOPR, these three metrics form a **complete picture of market profitability** at both the aggregate and per-transaction level.

---

## How to Use These Together: Cycle Framework

```
BOTTOM → RECOVERY → MID-BULL → LATE-BULL → TOP

NUPL:    < 0      →   0–0.25  →  0.25–0.5 →  0.5–0.75  → > 0.75
MVRV:    < 1.0    →   1–2     →  2–3      →  3–3.5     → > 3.5
SOPR:    < 1.0    →   ≈ 1.0   →  > 1.0    →  > 1.0     → > 1.0 (declining)
```

**Practical use:**
- Use NUPL/MVRV for **macro positioning** (are we early or late cycle?)
- Use SOPR for **tactical timing** (is today a good entry/exit?)
- Use LTH vs STH variants to understand **who is selling and why**

---

## Tools to Access These Metrics

- **Glassnode Studio:** https://studio.glassnode.com (free tier available for basic metrics)
- **Look Into Bitcoin:** https://www.lookintobitcoin.com (MVRV, NUPL charts, free)
- **Bitcoin Magazine Pro:** https://bitcoinmagazinepro.com (free tier)

---

*Note: These metrics were developed for Bitcoin and work best on Bitcoin. Ethereum adaptations exist but with less historical data. Altcoins generally have insufficient on-chain data for reliable signal.*
