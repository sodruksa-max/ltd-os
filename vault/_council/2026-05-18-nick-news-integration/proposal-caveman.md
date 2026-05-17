---
council_topic: nick-news-integration
proposer: caveman
date: 2026-05-18
---

# Caveman Proposal: Run Script. Drop File. Done.

## What is this, really?
Nick cannot see the world. So we run a script before Nick wakes up. Script fetches news. Drops it in Nick's folder as a file. Nick reads file. That is the whole thing.

## Gut signal
SAFE
Tool already exists. Food is already in the trap. We just need to drag it to Nick's cave.

## What we give (cost in primal terms)
One script call before each weekly review. Maybe 2 minutes. No new API key. No new code from scratch.

## What we get (reward in primal terms)
Nick sees headlines before deciding. Earnings miss, CEO fired, Fed surprise — Nick reads it, not us. Kill conditions fire faster. Money saved.

## The simplest version of this
Run news-snapshot.py. Also call yfinance for each holding Nick owns. Write both outputs to one file: `vault/Knowledge/nick-news-latest.md`. Nick reads it at the start of /nick-weekly. Done.

## Danger signals
| Signal | Why it activates |
|---|---|
| Too many headlines, no filter | Nick drowns in noise, thesis focus breaks |
| Macro news has no ticker | Easy to miss a war or a rate cut |
| File goes stale | Nick reads 3-week-old news like it is today's |

## Tribe check
Every fund manager reads news before trading. Nick is last. We are not early. We are fixing a hole that should not exist.

## Kill condition (primal)
If the news file is older than 7 days when /nick-weekly runs — the system failed. Stop and fix the trigger before Nick reads anything.
