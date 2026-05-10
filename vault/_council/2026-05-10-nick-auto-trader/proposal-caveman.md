---
council_topic: Nick Auto-Trader + Self-Improvement System
proposer: caveman
date: 2026-05-10
---

# Caveman Proposal: Watch First. Touch Later.

## Gut signal: DANGER

Machine that rewrites its own rules = machine that can quietly go wrong in ways you don't see until the damage is done.

## What we give (cost in primal terms)

- Control. You stop seeing each decision before it happens.
- Trust in the loop. If the loop is broken, trades still fire.
- 6 months of learning data written to KB. If it's bad data, KB gets poisoned.

## What we get (reward in primal terms)

Winning looks like: Nick picks good entries, holds them right, and the log teaches you something real. You graduate to real money with actual evidence. Good prize. But reward is 6 months away — depends on the machine not breaking in the middle.

## Simplest version that still works

**Shadow mode first. Month 1: Nick logs what it WOULD do. No execution.**

Every day. Full context. Alpaca touches nothing. Then you read the log. Do the picks look sane? After 30 picks logged — THEN turn on execution. Costs nothing extra. Gives a real sanity check before the machine runs free.

## Danger signals

| Signal | Why it activates |
|---|---|
| Self-improvement touches KB directly | Too few trades = noise becomes signal. KB poisoned. Nick's future picks get dumber. You don't notice for weeks. |
| Kill conditions need earnings call text | Machine can't read a call. It misses the kill. Position stays open when it should be dead. |
| Thesis bot acting daily | Thesis = weeks to months. Daily action = momentum bot in disguise. Different animal. Dangerous confusion. |
| No human gate before rule changes | 10 data points = very confident and very wrong. Machine doesn't know it has too little data. |

## Tribe check

Automated too early = lost control quietly. Watched first, then automated = learned something real. You are in month 1. Zero closed trades. Zero real signal yet. Too early to let the machine touch KB.

## Kill condition (primal)

Nick proposes any KB conviction update before 20 closed trades are logged → human blocks it. Full stop.

## The ONE rule that matters most

**No KB writes until 20+ closed trades exist.** Before that, every "insight" the machine generates is noise wearing signal's clothes.

## Nick vs human — who does what

- Nick: executes entries/exits, logs everything
- Human: reviews every proposed rule change before it touches KB
- Kill conditions needing earnings call text: human-only, no exceptions
