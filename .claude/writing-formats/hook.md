# Hook format (video openings, first lines)

A hook is the first 3-8 seconds of a video or the first sentence of anything written. Its job: make stopping feel like a mistake.

## Output format
Produce **3-5 hook variants** per request, labeled by pattern. User picks.

## Length
- **Video hook**: 3-8 seconds spoken = ~10-20 words
- **Written hook**: 1-2 sentences, ≤ 30 words
- **Thread hook**: see thread.md

## Patterns (use these, label which one)

### 1. Contrarian
"Everyone says X. They're wrong."
- Must actually be contrarian, not fake contrarian
- Example: "ทุกคนบอกให้ซื้อ index fund และ hold. ผมจะบอกว่าทำไมแย่."

### 2. Numbered specificity
"I <action>ed for <specific time>. Here's what I found."
- The specificity is what sells it
- Example: "I read 47 earnings calls in 30 days. Here's the pattern."

### 3. Stake / loss
"I lost <amount> learning <lesson>. You don't have to."
- Works because loss > gain in attention
- Example: "เสียเงิน 3 แสนจากบทเรียนเดียว. ผมจะสรุปให้ฟังฟรี."

### 4. Paradox
"<Thing A> makes <unexpected thing B> happen."
- Must land — if not surprising, cut
- Example: "The cheapest stocks are often the most expensive."

### 5. Named enemy / insight
"<Famous person> said X. <Y happened because of it>."
- Concrete person/event = credibility
- Example: "Buffett's 1996 letter predicted exactly this market."

### 6. Question that demands answer
"Why do <group> always <surprising behavior>?"
- Question must be genuinely interesting, not rhetorical filler
- Example: "ทำไมหุ้นถูกของ Thailand ถึง underperform กลับมาตลอด 10 ปี?"

### 7. In-medias-res scene (for video)
"[specific visual/action]. [tension/question]."
- Example: "[holding 3 papers] These three 10-Ks say the same lie."

## Anti-patterns (DO NOT USE)

Dead on arrival:
- "Have you ever wondered..."
- "Today I'm going to show you..."
- "In this video we'll cover..."
- "As you may know..."
- "Let's dive in"
- Greetings ("Hey guys", "สวัสดีครับ" at start — save for after hook)
- "AI is changing everything"
- "In today's fast-paced world"

## Test each hook against
1. **Would I keep watching?** — honest answer from yourself
2. **Can it be googled?** — if yes, what's the payoff for watching?
3. **Is it true?** — contrarian-for-clicks dies once trust burns
4. **Does the video actually deliver?** — hook promises must match content
5. **Can it be said in one breath?** — if no, cut words

## Thai hook notes
- Short particles ("นี่", "แบบนี้", "จริงๆ") can amplify — use 1, not 3
- Avoid starting with "สวัสดีครับ" — kills retention
- Mix English technical terms — reads more authoritative
- Tonal rhythm matters: end hook on stressed/assertive syllable if possible

## Output format for writer agent

When generating hooks, output like:

```
Topic: <what the piece is about>

HOOK VARIANTS:

1. [Contrarian]
   "<hook text>"

2. [Stake/loss]
   "<hook text>"

3. [Paradox]
   "<hook text>"

4. [Named enemy]
   "<hook text>"

5. [Numbered specificity]
   "<hook text>"

Recommendation: #<n> because <reason — 1 line>
```
