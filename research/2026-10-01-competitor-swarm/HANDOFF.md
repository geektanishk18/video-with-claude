# HANDOFF: FiguredOutAI competitor swarm + Instagram lead funnel (2026-10-01)

## ▶ Paste this into Claude Code (local, in the `video-with-claude` repo)

> Resume the FiguredOutAI session from `research/2026-10-01-competitor-swarm/HANDOFF.md`. Read that file, `RESEARCH_DIGEST.md`, and the briefs in `briefs/`. **Do not redo any research in `data/`.** Agents C, D, E and F are finished.
>
> Remaining work, in order:
> 1. Run agents **A** (Kinso AI + AI-native inboxes) and **B** (HighLevel + omnichannel CRM incumbents) from `briefs/` as two parallel subagents. Use my local Chrome. Whenever a page needs a login, **stop and ask me to log in manually**, then continue. Never type credentials.
> 2. Walk me through the **login checklist** at the end of `RESEARCH_DIGEST.md`, one page at a time, and record what I report.
> 3. Write `data/agent_A.json`, `agent_B.json`, `steps_A.json` and `steps_B.json`, update `graph/verdict.json` and `graph/status.json`, run `python graph/build.py`, and open `graph/index.html` (the Jarvis-style Obsidian graph). Keep it live: rebuild after each agent finishes.
> 4. Write the **final verdict** on my claim with evidence and FiguredOutAI's positioning.
> 5. Finalise the **lead funnel**: the exact auto-DM copy for "INBOX" comments and DMs, tool setup (ManyChat or alternatives + Cal.com), and qualification questions. Then write the **SOP for daily/alternate-day organic reels** as a document.

---

## 1. Who and what

- **Founder:** Tanishk (tanishk1440@gmail.com), solo founder of **FiguredOutAI**, an India-based AI/automation agency. GitHub: `geektanishk18`. Repo: `geektanishk18/video-with-claude` (private).
- **Product in progress:** the **Unified AI Inbox**. One inbox for WhatsApp, Instagram DMs and comments, website forms and chat, email and calls. AI reads each conversation, extracts intent, budget, location and timeline, qualifies the lead against the business's own criteria, gives a match score, sorts by priority and routes to the best-fit salesperson, with a CRM behind it.
- **Today's trigger:** the **Peter & Stewie explainer reel** (v3 in `reels/unified-ai-inbox/renders/`) is live on Instagram. Its CTA is "comment INBOX", and people are commenting and DMing.
  - **Nothing is automated yet.** No funnel, no auto-DM copy (the "missing Step 2"), no live waitlist page; the SaaS isn't ready.
  - **Goal:** turn engagement into **booked 20-minute free business audits**, then sell **custom implementation** projects.
  - **Cadence:** reels daily or every other day.

## 2. What the founder asked for today

1. **Before anything else:** a **multi-agent research swarm** on active competitors (KinsoAI, HighLevel, Interakt, Vapi and others), using a real browser and Instagram/LinkedIn. It should test the claim *"an omnichannel AI inbox with proper CRM isn't anyone's product yet"* and correct it with proven research points.
2. Show the swarm's whole procedure as a **Jarvis-style Obsidian graph**, visible live in the in-app browser.
3. **Login rule:** wherever there's a login, **ask the founder to log in manually in Google Chrome**. This was impossible in the cloud session, which is why we're handing off to a local one.
4. Then the funnel: comment/DM → automation → qualification → booked 20-minute audit. Plus funnel options, the auto-DM message, and an **SOP for FiguredOutAI's organic reel marketing**.

## 3. Status

| Item | Status | Where |
|---|---|---|
| Agent C: India WhatsApp-first (Interakt, Wati, AiSensy, Gallabox, LimeChat, Gupshup, Yellow.ai, BotPenguin, Kapture) | ✅ done | `data/agent_C.json`, `steps_C.json` |
| Agent D: Voice AI + AI SDRs (Vapi, Retell, Bland, Synthflow, Qualified Piper, Conversica, 11x, Artisan, Exotel, Haptik) | ✅ done | `data/agent_D.json`, `steps_D.json` |
| Agent E: Enterprise (Fin/Intercom, Zendesk, Salesforce, Freshworks, Sprinklr, Meta Business Agent) | ✅ done | `data/agent_E.json`, `steps_E.json` |
| Agent F: Comment-to-DM funnel (ManyChat, SuperProfile, LinkPlease, Meta rules, Cal.com/Calendly, benchmarks) | ✅ done | `data/agent_F.json`, `steps_F.json` |
| Agent A: Kinso AI + AI-native inboxes | ⏳ **not done.** It was started twice and stopped by interrupts; no results were saved. | `briefs/agent_A_brief.md` |
| Agent B: HighLevel, Kommo, respond.io, Trengo, Zoho, HubSpot | ⏳ **not done.** It was stopped by an interrupt; no results were saved. | `briefs/agent_B_brief.md` |
| Login checklist (33 pages flagged by C–F) | ⏳ needs the founder in Chrome | end of `RESEARCH_DIGEST.md` |
| Jarvis/Obsidian graph | ✅ built from real tool logs: 174 nodes, 324 links | `graph/index.html`; cloud copy: https://claude.ai/artifact/32QZAd61iTRgsoide75Mfq |
| Final verdict | 🟡 provisional (4 of 6 agents) | §4 below, `graph/verdict.json` |
| Auto-DM copy, funnel setup, SOP | ⏳ not written yet. The research inputs are ready (agent F). | §5 below |

**Why the cloud session couldn't use a real browser:**
- Headless Chromium in the container failed TLS through the cloud network proxy. Certificate checks were never disabled.
- So agents used WebFetch, or Node with checks still on. Some excerpts are therefore model summaries rather than verbatim quotes; the JSON says which.
- A cloud session also can't reach the founder's local Chrome. Locally, both problems disappear.

## 4. Provisional verdict (agents C, D, E, F)

**The claim is mostly wrong as stated.** The pieces already exist, and some vendors bundle most of them:
- **Gallabox (India, 4/5):**
  - Pricing: ₹2,399 / ₹5,599 / ₹13,599 per month, annual billing.
  - One inbox for WhatsApp, Instagram DMs and comments, a website widget and WhatsApp/phone calls.
  - AI agents qualify against business rules ("If they fit (5+ users, budget over $500/month)…") and advertise "scoring intent in real time".
  - Round-robin routing and a built-in lead pipeline. The pipeline and field-extraction webhooks need the ₹13,599 plan.
- **Wati (4/5):** "one inbox · every channel". Its Astra AI agents qualify leads, but they're a paid add-on, and its CRM works only through HubSpot, Zoho or Salesforce.
- **Interakt (Jio Haptik, 3–3.5/5):** a unified WhatsApp + Instagram inbox (DMs and comments) and AI agents that "qualify leads". It also has a "Sales CRM with auto-assigned owners and statuses".
- **Gupshup (3/5):** an AI agent that "qualifies and assigns leads based on budget, location and intent". Enterprise, sold through sales.
- **Fin (formerly Intercom, now owned by Salesforce since 10 Sep 2026, 4/5):** qualifies against criteria and routes to sales, at $9.99 per qualified lead plus $29 per seat. Multichannel, but no native CRM and no published match score. Expensive for Indian SMBs.
- **Freshworks (4/5):** a chat inbox plus the Freshsales CRM (~₹1,099–6,099/user) and Freddy AI scoring. But it's two products, and bot qualification is scripted.
- **Salesforce (4/5):** everything is possible, at enterprise cost and complexity.
- **Meta Business Agent (3/5):** free, launched globally in June 2026 after two years of testing in India. It qualifies leads on WhatsApp, Instagram and Messenger. It covers only Meta's own channels, with no score and no real CRM. **It's the biggest threat to the qualification step itself.**
- **Voice AI (Vapi, Retell, Bland, Synthflow) and AI SDRs:** single-channel agents and APIs that write to someone else's CRM. Not inbox products (0.5–2/5).

**The gap no one in the evidence fully covers:**
1. **Email as a full channel** alongside WhatsApp, Instagram, website and calls in an SMB-priced inbox.
2. **A business-defined match score with priority sorting as the core screen.** Others treat scoring as a side feature of a bot.
3. **A native sales CRM in that same inbox at Indian SMB prices**, India-first.

**Positioning to test:** "the lead-priority inbox": every enquiry from every channel, including email and calls, understood, scored against *your* criteria, sorted and routed, with the CRM built in. Benchmark directly against Gallabox.

**Pending:** agents A and B. HighLevel in particular could move this verdict, especially through Indian white-label resellers.

## 5. Funnel: research inputs (agent F) and a draft design

**Meta/Instagram rules that set the flow's shape** (official Meta docs; see the digest):
- **One message per comment.** An automated "private reply" to a comment can send **only one DM**, within **7 days** of the comment.
- **Anything after that needs the person's reply first,** and must go out within **24 hours** of it. The 7-day "human agent" extension is Messenger-only, not Instagram.
- **No follow-gating.** Meta's spam policy lists requiring a follow to get something as spam.
- **Say it's automated.** Meta requires disclosing that the DM is automated.
- **The phone quick-reply only pre-fills a number already on the person's profile.** Collect phone numbers on the booking form instead.

**Recommended stack (agent F; confirm the pricing pages while logged in):**
- **ManyChat Pro**, about $29/month + 18% GST, USD card. It has keyword triggers, a public comment reply, button questions and a Calendly integration. Third-party reports say the free tier was cut to 25 contacts in March 2026, so treat free as a trial only.
- **SuperProfile** is INR-priced, but its AutoDM is reportedly one trigger per post with no multi-step flows, which is too thin for qualification. **LinkPlease** (from about ₹499/month) is the budget fallback.
- **Cal.com free** for booking: unlimited event types, booking questions, Google Meet, SMS/WhatsApp reminders (WhatsApp uses a fixed default message). Calendly free allows only one event type. Google's booking page has no automatic reminders.

**Draft flow (agent F, refined), not yet approved by the founder:**
1. **Comment "INBOX"** → automatic public reply under the comment, e.g. "Sent you a DM 📩".
2. **The one allowed DM:** say it's automated, a one-line hook, and a **"Yes, audit my business"** button. The tap opens the conversation window.
3. **Two button questions:** business type, and the task eating the most time. Optionally a third: monthly enquiry volume.
4. **Cal.com link** for a 20-minute audit, showing **same-day and next-day slots**. The booking form collects name, email, WhatsApp number and a one-line problem.
5. **Reminders** the day before and the day of. **The founder replies personally within 1 hour** to anyone who doesn't book.

**Draft DM copy, a starting point to refine with the founder:**
> "Hey {first_name} 👋 (automated reply from FiguredOutAI). Thanks for commenting INBOX! We set up exactly what you saw in the reel: every enquiry from WhatsApp, Instagram, your website and calls in one inbox, with AI telling you which leads to call first. Want a free 20-min audit of how your leads come in today?"
> Button: **Yes, audit my business**
> Then: "What kind of business do you run?" [Real estate] [Clinic/healthcare] [Coaching/education] [Agency/services] [Other]
> Then: "What eats most of your team's time?" [Replying to enquiries] [Following up] [Figuring out who's serious] [Updating the CRM/sheets]
> Then: "Perfect. Pick a slot that suits you (takes 20 mins, no pitch deck): {cal.com link}"

**Evidence behind the design** (details and sources in the digest):
- **Book sooner:** show rate is about 81% when the meeting is 1 day out, and about 60% at 14 days (Chili Piper; medium-quality source). Offer near slots.
- **Show the scheduler instantly:** 66.7% of qualified form fills booked, against about 30% typical (Chili Piper; medium).
- **Reply fast:** responding within 1 hour makes a lead about 7× more likely to qualify (HBR; medium).
- **Don't rely on WhatsApp reminders alone:** an Indian randomised trial in healthcare found no significant effect.
- **DM benchmarks are weak** (vendor blogs). One coach example converted about 0.7% of commenters into booked calls.
- **The founder's assumption that a PDF or guide won't work:** no evidence was found either way. Treat it as a hypothesis to A/B test.

**Funnel options still to lay out for the founder:**
- **(a)** IG DM → Cal.com. This is the recommended start.
- **(b)** IG DM → a WhatsApp handoff that demos the product's own automation, the "wow" option.
- **(c)** IG DM → a landing page with a Loom video and lead form, until the waitlist is live.
- **(d)** Hybrid: book directly, or chat on WhatsApp.
- Plus a manual fallback for today: reply by hand with the same script while the automation is being set up.

## 6. Login checklist summary

There are 33 items (C: 14, D: 7, E: 7, F: 5), with exact URLs and what to check, at the end of `RESEARCH_DIGEST.md`. They are mostly Instagram and LinkedIn pages for the competitors, plus ManyChat, SuperProfile and LinkPlease pricing, Cal.com reminders to +91 numbers, and the Gallabox trial.

## 7. Graph (Jarvis-style Obsidian view)

- `graph/index.html` is a self-contained page (fonts come from Google Fonts): a force-directed graph with an orchestrator core, the 6 agents, every search, every website visited, the competitors with 0–5 closeness rings, login-gated pages in red, and verdict/SOP synthesis nodes.
- **Controls:** drag to pan, scroll to zoom, press F to recentre, click a node for details. The legend toggles node types.
- **Rebuild:** `python graph/build.py`. It reads `data/agent_*.json` and `data/steps_*.json`, plus `graph/status.json` (agent status) and `graph/verdict.json` (verdict text).
- **For live updates from new local agents,** either point `TASKS_DIR` at their transcript folder or write `steps_<X>.json`. Then rebuild and refresh the page in Chrome.
- The cloud copy (snapshot 2) is at https://claude.ai/artifact/32QZAd61iTRgsoide75Mfq.

## 8. Other context from this project (don't redo)

- **Reel pipeline:**
  - Two Claude Code skills are in `skills/`: `figuredout-reel` (Peter/Stewie) and `figuredout-reel-rick-morty` (looks system, portal reveal).
  - Setup is in `setup/`: `setup-windows.ps1`, `setup.sh`, `check.py`, `WORKFLOW.md`.
  - The Unified AI Inbox reel's approved version is **v3**: 60 fps, a calm mellow music bed, and dialogue about 18 dB above the music.
- **Brand system (locked):**
  - Colours: ink `#030A0E`, panel `#08171D`, teal `#1B6579`, sky `#90C2E7`, peak `#C9E4F5`, paper `#F0EDEF`.
  - Type: Poppins for display, Inter for body.
  - Glow rule: a radial gradient that goes sky → teal → transparent, with 24 px blur.
  - Copy: "enquiry", ₹ pricing, no exclamation marks in brand copy, never invent stats or clients.
- **Company facts:** FiguredoutAI LLP, LLPIN ACZ-0822, Noida. hello@figuredoutai.com. Founders: Tanishk Singhal (CEO) and Yashvardhan Awasthi (CTO). Primary CTA style: "Get your intake audit". There's no Calendly on the website by design: the site uses a lead form that emails the founder. **Ask the founder whether a booking link in DMs is acceptable, given this earlier website decision.**
