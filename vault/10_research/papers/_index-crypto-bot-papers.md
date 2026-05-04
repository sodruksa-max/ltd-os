---
title: "Crypto Bot Research Papers — Index"
tags: [crypto-bot, research, index]
created: 2026-05-04
---

# Crypto Bot Research Papers

Papers อ่านและบันทึกสำหรับ BTC/crypto trading bot project รัน local (GPU available)

## Tier 1 — ใส่ใน bot ได้เลย

| Paper | File | ใส่ตรงไหน |
|-------|------|-----------|
| VP-MACD | [[2604.26063-vp-macd]] | crypto-screener.py — แทน MACD ธรรมดา |
| LOB Microstructure (BTC/USDT) | [[2604.20949-lob-microstructure-regimes]] | entry filter ก่อน place order |
| Constrained LLM Crypto Factors | [[2604.26747-constrained-llm-crypto-factors]] | LLM analysis layer |
| Multi-Agent Architecture | [[2604.17327-multi-agent-llm-stocks]] | blueprint 4 specialist + 1 synthesizer |
| QRAFTI Agentic Framework | [[2604.18500-qrafti-agentic-quant]] | data pipeline + reflection planning |
| Interpretable Systematic Risk | [[2604.13458-interpretable-systematic-risk]] | 24/7 news jump detector |
| Behavioral AI Biases | [[2604.18373-dissecting-ai-trading-biases]] | prompt rules ป้องกัน bias |
| Machine Spirits (model selection) | [[2604.18602-machine-spirits-llm-bubbles]] | เลือก LLM ที่ไม่ bubble |
| OOM-RL Alignment | [[2604.11477-oom-rl-market-alignment]] | PnL-based feedback loop |
| PolySwarm Voting | [[2604.03888-polyswarm-multi-agent-voting]] | confidence-weighted multi-model vote |
| SBBTS Synthetic Data | [[2604.07159-sbbts-synthetic-timeseries]] | stress-test backtest ก่อน deploy |
| MPC Trade Execution | [[2603.28898-mpc-trade-execution]] | optimal order placement, ลด slippage |
| Kalshi Macro→Crypto Vol | [[2604.01431-kalshi-macro-crypto-vol]] | Fed/CPI event calendar filter |
| Debiasing LLM LoRA | [[2604.02921-debiasing-llm-lora]] | fine-tune local model ลด bias |
| CAViaR Tail Risk Spillover | [[2603.25217-caviar-tail-risk-spillover]] | cross-asset tail risk warning |

## Tier 2 — blueprint / reference

| Paper | File | ใช้ทำอะไร |
|-------|------|-----------|
| Adversarial Price+Sentiment | [[2604.22801-adversarial-price-sentiment]] | hybrid model architecture |
| Sentiment Spillover Networks | [[2604.26811-sentiment-spillover-networks]] | transfer entropy method |
| ExsdHawkes LOB | [[2604.23961-exsd-hawkes-lob]] | deep order book modeling |
| Satoshi Overhang | [[2604.27694-satoshi-overhang]] | macro risk parameter |
| Motif Risk Spillover | [[2604.25406-motif-risk-spillover]] | cross-asset network alert |
| Self-Driving Portfolio | [[2604.02279-self-driving-portfolio]] | large-scale agent architecture |
| HF Duration Point Process | [[2604.00346-hf-duration-point-process]] | trade timing model |
| Which Voices Move Markets | [[2604.13260-which-voices-move-markets]] | source-credibility weighting |

## Tier 3 — อ่านเพื่อ context

| Paper | File | เหตุผล |
|-------|------|--------|
| ValueAlpha Stress Test | [[2604.25224-valuealpha-llm-stress-test]] | validate LLM rationale ก่อน execute |
| SoK A2A Blockchain | [[2604.03733-sok-a2a-blockchain-payments]] | future infrastructure reference |

## Build Order แนะนำ

```
Phase 1 — Core signal (สัปดาห์ 1-2):
  VP-MACD → LOB Regime → Kalshi macro filter → MPC execution

Phase 2 — Intelligence layer (สัปดาห์ 3-4):
  Multi-Agent architecture → Behavioral prompt rules → Model selection
  SBBTS synthetic backtest

Phase 3 — Advanced (เดือน 2+):
  LoRA fine-tuning → OOM-RL alignment → PolySwarm voting
  CAViaR risk spillover
```
