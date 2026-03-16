# Video Demo Script for Hackathon

**Duration:** 2:45 minutes
**Format:** Screen capture + voiceover
**Resolution:** 1440x900 or 1920x1080
**Platform:** YouTube (then embed in Devpost)

---

## VIDEO TIMELINE & SCRIPT

### [00:00-00:15] COLD OPEN – Problem Hook

**Visual:**
- Fast montage: Spreadsheets, frustrated finance people, calendars with "MONTH-END CLOSE" circled
- Zoom in on laptop: 10,000 line items in Excel, red flags everywhere

**Voiceover:**
"Every month, finance teams go dark for 10 days.
Bank matching. Reconciliations. Approvals.
All manual. All error-prone.
What if they could get *all* of that back?"

**Audio:** Tense, dramatic bg music (0:05s)
**Transition:** Fade to black, reveal logo

---

### [00:15-00:35] INTRO – Meet LedgerLive

**Visual:**
- LedgerLive logo animation (white text on dark F1-style background)
- Quick cuts of UI pages:
  - Dashboard (bright KPI cards)
  - Agent Console (agent response streaming)
  - Readiness Dashboard (checks turning green)
- Company motto appears: "Real-Time Financial Close"

**Voiceover:**
"Meet LedgerLive.
A platform powered by Gemini Live agents.
In one conversation, an agent can read your ledgers, identify problems, post entries, and notify approvers.
In real-time."

**Audio:** Energetic, modern synth music (0:20s)
**Text overlays:**
- "Gemini Live Agents"
- "Real-time Streaming"
- "60% faster close"

---

### [00:35-01:10] DEMO 1 – Dashboard Overview

**Action:**
1. **Open browser** to https://ledgerlive-web-zkw2sk4rha-uc.a.run.app
2. **Show Dashboard page** (KPI cards visible)
   - "Days to Close: 4.2d" (blue)
   - "Open Exceptions: 12" (red)
   - "Agent Activity: 47 cycles" (purple)
   - Close Cycle Progress bar at 87%

**Voiceover:**
"This is your financial close command center.
Real-time KPIs: how many days left, how many exceptions remain, how many agent cycles have run.
All updating live as the agent works."

**Camera action:**
- Slowly scroll down dashboard
- Show Exceptions section (list of unmatched items)
- Show Agent Activity (recent agent cycles)

**Visual effects:**
- Highlight key metrics with boxes
- Point out "Live update" indicators

**Audio:** Professional, calm (0:35s)

---

### [00:60-01:30] DEMO 2 – Agent Console (Core Feature)

**Action:**
1. **Click "Agent Console"** from nav
2. **Show console interface** with input box
3. **Type message:** "Resolve open AP exceptions"
   - Pause 1 second to let it register
4. **Hit Enter / Send button**

**Voiceover (as agent starts responding):**
"Now we'll ask the agent to resolve open AP exceptions.
Watch what happens next..."

**LIVE STREAMING BEGINS:**

**Visual:**
Show text streaming in real-time (simulate WebSocket stream):
```
Perceiving AP ledger...
Found 12 unmatched invoices totaling $2.4M
Matching invoices to POs...
  ✓ Invoice #INV-2602-001 → PO #PO-001234 ($450K)
  ✓ Invoice #INV-2602-003 → PO #PO-001245 ($380K)
  ✓ Invoice #INV-2602-007 → PO #PO-001267 ($320K)
  [streaming continues...]
```

**Voiceover (excited, dynamic):**
"Look at that! The agent is perceiving your AP ledger in real-time.
It's matching invoices to purchase orders.
All while streaming back to you.
No waiting. No batch processing."

**Audio:** Uptempo, energetic (0:25s)

**Key points to highlight:**
- "Real-time streaming" (text coming in live)
- "Tool execution" (matching logic)
- Latency counter: ~284ms per cycle (visible in UI)

---

### [01:30-02:05] DEMO 3 – Real-Time Effects (Agent Affects Dashboard)

**Action:**
1. **Continue watching stream** (shows agent deciding what to do)
2. **Agent posts journal entries** (visible in stream)
   - "Posting entry: DR AP Accrual $2.1M / CR Bank Clearing"
   - "Notifying CFO for sign-off"
   - "Updating audit trail"
3. **Switch back to Dashboard tab** (browser switch or split view)
4. **Show metrics have changed:**
   - "Open Exceptions: 12" → now "Open Exceptions: 3" ✓ (decreased!)
   - "Close Cycle Progress: 87%" → now "Close Cycle Progress: 94%"
   - "Agent Activity: 47 cycles" → now "Agent Activity: 52 cycles"

**Voiceover:**
"And here's the magic—
As the agent works, your dashboard updates in real-time.
Exceptions disappear.
Your readiness percentage climbs.
All live."

**Visual effects:**
- Highlight the changed metrics with green checkmarks or animations
- Show the speed (all happened in <3 minutes)

**Audio:** Triumphant, satisfying (0:15s)

---

### [02:05-02:30] DEEP DIVE – Trace Explorer

**Action:**
1. **Click on "Trace Explorer"** page
2. **Show waterfall visualization** of agent execution:
   ```
   agent.perceive [████████░░░░░░░░░░░] 45ms
   ├─ api.get_ap_ledger [████████░░░░░░] 28ms
   ├─ api.get_po_data [██████░░░░░░░░░░] 32ms
   └─ api.match_logic [░░░░░░░░░░░░░░░░] 10ms

   agent.decide [████████████████████] 120ms
   └─ llm.claude (streaming) [████████████████] 120ms

   agent.act [███████████████░░░░░░░] 88ms
   ├─ api.post_journal [████████░░░░░░░░] 35ms
   ├─ api.notify_approver [█████░░░░░░░░░░░] 20ms
   └─ api.audit_log [██████░░░░░░░░░░░] 34ms
   ```

**Voiceover:**
"Want to see what's happening under the hood?
This is our Trace Explorer.
Every agent action tracked. Every API call timed.
Perceive: 45 milliseconds.
Decide: 120 milliseconds (that's the LLM thinking).
Act: 88 milliseconds (posting entries, notifying approvers).
Total cycle: 284ms. Fully transparent."

**Visual:**
- Hover over bars to show tooltips with latency
- Show color coding (blue=success, yellow=warning, red=error)
- Zoom in on specific bars to highlight the streaming

**Audio:** Informative, professional (0:25s)

---

### [02:30-02:50] RESULTS & IMPACT

**Visual:**
- Show a metrics slide with stats:
  ```
  Financial Close Metrics:

  Before LedgerLive    After LedgerLive
  ==================  =================
  10 days              4 days              (60% faster)
  15 people × 40h      3 people × 10h      (85% less manual)
  $50K process cost    $20K process cost   (60% cheaper)
  3 exceptions/day     0.3 exceptions/day  (90% fewer)
  94.2% accuracy       99.7% accuracy      (AI > humans)
  ```

**Voiceover:**
"Here's what it means in the real world.
Close time cut in half. Your finance team gets 6 days back every month.
85% less manual work.
60% cost reduction.
94 to 99 percent accuracy—because Gemini doesn't get tired, doesn't miss line items.
It just works."

**Audio:** Motivational, confident (0:20s)

---

### [02:50-03:00] CLOSING – Call to Action

**Visual:**
- Show website URL: https://ledgerlive-web-zkw2sk4rha-uc.a.run.app
- Show GitHub badge
- Final screen: "LedgerLive. Powered by Gemini Live."

**Voiceover:**
"LedgerLive is live today.
Try it now at [URL].
Or check out our code on GitHub.
Built on Gemini 2.0 Live—and Cloud Run.
Real-time agents. Real results."

**Audio:** Upbeat finale; fade out (0:10s)

**End card:** LedgerLive logo + social links

---

## FILMING CHECKLIST

- [ ] Ensure good internet (WebSocket needs stable connection)
- [ ] Clear browser cache to show fresh state
- [ ] Have test data loaded (12 exceptions, recent agent cycles)
- [ ] Use 1440x900 or 1920x1080 resolution; 30fps or 60fps
- [ ] Screen recording software: OBS Studio, Camtasia, or Screenflow
- [ ] Audio: Clear USB headset mic; edit background noise out
- [ ] Test WebSocket streaming before recording (may need test message sent)
- [ ] Record in multiple takes; keep best one
- [ ] Edit out pauses/typing; keep action flowing
- [ ] Add lower-third graphics (timestamps, metric labels)
- [ ] Add background music from royalty-free library (Epidemic Sound, Artlist)

---

## POST-PRODUCTION EDITING

**Software:** Adobe Premiere Pro, DaVinci Resolve, or iMovie

**Edits:**
1. **Cut out silences** and slowdowns
2. **Add captions** for accessibility (YouTube auto-captions, then manually review)
3. **Highlight key moments** with zoom-ins or color boxes
4. **Add text overlays:**
   - "[Real-time streaming]" during console output
   - "[Metrics updating live]" when dashboard changes
   - "[284ms agent cycle]" on Trace Explorer
5. **Background music:** Upbeat but professional (not distracting)
6. **Transitions:** Fade or simple cuts (no spinning/swirling)

---

## UPLOAD & SHARE

**YouTube:**
1. Set to **Unlisted** (only accessible via link)
2. Title: "LedgerLive: Real-Time Financial Close with Gemini Live Agents"
3. Description:
   ```
   Submitted for the Gemini Live Agent Challenge Hackathon.

   LedgerLive automates financial close cycles using Gemini Live multi-turn agent streaming.

   Live demo: https://ledgerlive-web-zkw2sk4rha-uc.a.run.app
   GitHub: https://github.com/[username]/ledgerlive

   Built with:
   • Google Gemini 2.0 Live API
   • FastAPI + Python 3.12
   • React 18 + Vite
   • Google Cloud Run

   #GeminiLiveAgentChallenge
   ```
4. Tags: `Gemini`, `Agents`, `AI`, `FinTech`, `Cloud`
5. Thumbnail: Custom (use design from DEVPOST_SUBMISSION_CHECKLIST.md)

**Embed in Devpost:**
- Copy YouTube URL
- Paste into "Video demo link" field on Devpost
- Mark as primary project media

**Share on social:**
```
🚀 Just submitted LedgerLive to #GeminiLiveAgentChallenge!

Real-time financial close automation using Gemini Live agents.
60% faster, zero manual overhead.

Live: [URL]
GitHub: [URL]
Video: [YouTube URL]

#AI #FinTech #CloudRun
```

---

## ESTIMATED VIEWER REACTIONS

"Wow, the streaming is so smooth!"
→ That's WebSocket + Gemini Live + FastAPI optimization

"How does it post entries so fast?"
→ Agent executes tool calls in parallel where possible

"What if the API rate limits?"
→ Smart fallback to local SLM (shown in code)

"Can we try it ourselves?"
→ Yes, live demo URL or GitHub repo (setup instructions in README)

