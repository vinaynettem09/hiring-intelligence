# VALIDATION-03 — Design Partner Research Playbook

| Field | Value |
|---|---|
| **Document ID** | VALIDATION-03 |
| **Title** | Design Partner Research Playbook (Interview Guide + Discovery Questions, merged) |
| **Owner** | Founder/CEO + whoever runs a given interview |
| **Status** | Draft v0.1 — operational; use it live |
| **Created** | 2026-07-22 |
| **Phase** | Validation Mode |
| **Depends on** | **VALIDATION-01 (Assumptions)** and **VALIDATION-02 (Risks)** — every interview here tests a specific assumption / reduces a specific risk. |
| **Purpose** | A single, self-contained artifact any founder or product leader can use to run a consistent, unbiased design-partner interview. No flipping between documents mid-conversation. |
| **The objective (say it out loud before every interview)** | **We are not here to sell. We are here to discover whether our assumptions survive contact with reality. The interview *succeeds* when we discover we were wrong — early and cheaply.** |

---

## 0. The mindset (read before every single interview)

> The interviewer is **not pitching**. Not validating ego. Not teaching. **Learning.**

You are trying to *disconfirm* your beliefs, not collect reassurance. A pleasant interview where everyone loved the idea and you learned nothing is a **failed** interview. A tense interview where a recruiter told you your core idea is naïve is a **great** interview. Optimize for the second.

This playbook is deliberately structured to make biased interviewing *hard* — because confirmation bias (RK-15, the highest-likelihood existential risk) is the default human failure mode, and it will quietly kill the company by "validating" a false thesis.

---

## 1. Interview Preparation

*Fill this in **before** every interview. Ten minutes of prep prevents a wasted conversation.*

| Prep field | For this interview |
|---|---|
| **Persona** | Candidate / Recruiter / Hiring Manager / CHRO / Security-IT (pick one primary) |
| **Assumptions under test** | The specific AS-x from VALIDATION-01 (e.g., AS-1, AS-10). *Max 2–3 — a scattershot interview tests nothing.* |
| **Risks being reduced** | The RK-x from VALIDATION-02 this maps to. |
| **Target evidence level (VALIDATION-01 R3)** | Interviews yield **L0–L1** (opinion/stated). Be honest: this interview *informs* hypotheses; it does **not** *validate* (that needs L2+ behavior). |
| **Pre-registration link** | If this interview is part of a formal experiment (A/B/C), reference its pre-registration (VALIDATION-01 R2). |
| **What "surprising" would look like** | Write one sentence: *"I would be genuinely surprised if they said ___."* Then listen for exactly that. |

> **Rule:** if you can't name the 2–3 assumptions this interview tests, don't take the interview yet.

---

## 2. Interview Rules (non-negotiable)

1. **Never pitch before understanding.** Understand their world completely before describing anything we might build. Ideally, don't describe it at all in a discovery interview.
2. **Never ask leading questions.** "Don't you hate resume screening?" → instead: "Tell me about how you screen resumes."
3. **Never defend our ideas.** If they criticize the concept, say *"tell me more about why"* — never *"well, actually…"*. Their criticism is the gold.
4. **Ask about past behavior, not future intentions.** "What did you do last time?" beats "What would you do?" People predict their future behavior badly and flatter interviewers.
5. **Follow emotion.** When their voice changes — frustration, relief, anger — stop and dig. Emotion marks what matters.
6. **Ask "why?" until the root cause is exposed.** Three to five "whys." Surface answers are rationalizations; root causes are truth.
7. **Silence is useful.** After they answer, wait. The second thing they say is usually more honest than the first. Do not fill the silence.
8. **Contradictory evidence is valuable.** When they say something that contradicts our thesis, lean *in*, not away. Log it (VALIDATION-01 R4).
9. **Record exact quotes.** Verbatim. "It's a nightmare" is data; "they found it hard" is your paraphrase (and probably softened).
10. **Distinguish observations from interpretations.** *Observation:* "She skipped the resume and opened the take-home first." *Interpretation:* "She values evidence over resumes." Record both, labeled — never fuse them.

---

## 3. Persona-Specific Interview Guides

*Each: Goals · Assumptions under test · Open-ended questions · Follow-up probes · Behaviors to observe · Signals that validate · Signals that invalidate. Questions are behavior-first — never "would you use our product?"*

### 3.1 CANDIDATE (Alex) — *the mission's ground truth; include rejected candidates (Experiment C)*
- **Goals:** understand their real hiring experience; learn what *"fair"* actually means; gauge whether they'd complete a richer evaluation; understand how rejection feels.
- **Assumptions under test:** AS-3 (completion/adoption), AS-10 (fair chance incl. rejected), AS-11 (explainability→trust); Unknowns (voice vs. text; tolerable length). **Risks:** RK-3.
- **Open-ended questions:**
  - "Walk me through the last few jobs you applied for. What actually happened at each step?"
  - "Tell me about a time you were rejected. What did you hear back — if anything? How did it feel?"
  - "When you applied and never heard back at all, what went through your mind?"
  - "Tell me about a hiring process that felt *unfair*. What specifically made it unfair?"
  - "Now tell me about one that felt *fair*. What made the difference?"
  - "Describe the last take-home / coding test / assessment you did. How long did it take? How did you feel doing it?"
  - "Have you ever abandoned an application partway through? What made you quit?"
  - "You may have been evaluated by an automated system somewhere. Tell me about that experience."
- **Follow-up probes:** "Why did that matter to you?" · "What did you do next?" · "How long did you actually spend?" · "What would 'a fair chance' have looked like there?"
- **Behaviors to observe:** emotional charge when rejection comes up; whether they've *actually* abandoned processes (and at what effort threshold); whether "fair" means *ability-based* or something else.
- **Signals that VALIDATE:** they describe resume black holes as genuinely painful; they've completed substantial evaluations before without complaint when they felt it was fair; they light up at "being evaluated on what I can do."
- **Signals that INVALIDATE:** they're content with resume-first; they'd refuse an AI-run evaluation on principle; effort tolerance is far below what a real evaluation requires; "fair" to them means *fast*, not *ability-based*.

### 3.2 RECRUITER / TALENT ACQUISITION (Rina) — *(Experiment B: shadow, don't just ask)*
- **Goals:** learn how they *actually* screen and decide (vs. what they say); whether they'd trust/act on evidence; whether they'd champion it.
- **Assumptions under test:** AS-1 (baseline: what actually predicts good hires), AS-2 (act on evidence), AS-8 (trust in days), AS-18 (champion), AS-22 (integration friction). **Risks:** RK-1, RK-5, RK-12.
- **Open-ended questions:**
  - "Walk me through the last role you filled — from req open to hire. What happened at each step?"
  - "Show me how you decide who moves forward. If you have your ATS open, walk me through a real req." *(Shadow — watch what they click, not what they narrate.)*
  - "Tell me about the last time a hiring manager rejected your shortlist. What happened, and why?"
  - "How do you find out whether a hire actually worked out? Do you ever find out?"
  - "When you hand over a shortlist, how do you justify your picks to the manager?"
  - "Tell me about a bad hire that came through your pipeline. What did you miss, in hindsight?"
  - "What part of your job is the biggest time sink? Walk me through yesterday."
- **Follow-up probes:** "Why *that* candidate over the others?" · "What would have changed your mind?" · "What do you actually look at first?" · "How confident were you, honestly?"
- **Behaviors to observe:** do they screen on keywords/pedigree/school; time pressure; whether they *ever* get outcome feedback; defensiveness about their own process.
- **Signals that VALIDATE:** they admit distrust of their own screening; they get little/no outcome feedback (a gap we fill); they lean in and *volunteer* to pilot/champion; visible relief at "defensible shortlist."
- **Signals that INVALIDATE:** genuine confidence in resume screening; no interest in changing behavior; passive or threatened ("is this going to replace me?"); no authority or energy to champion.

### 3.3 HIRING MANAGER (David)
- **Goals:** understand how they *really* decide; whether they'd stop re-screening; whether their "bar" is capturable.
- **Assumptions under test:** AS-9 (stop re-screening), AS-12 (calibration captures the bar), AS-2 (act on evidence), AS-1 (what predicts good hires in their experience). **Risks:** RK-5, RK-7.
- **Open-ended questions:**
  - "Tell me about your best hire and your worst hire. What actually distinguished them?"
  - "Walk me through your last hiring decision. What tipped it?"
  - "When a recruiter sends you a shortlist, what do you do with it?" *(Probe re-screening without naming it.)*
  - "How would you describe your bar for this role? Could you hand it to someone else and trust them to apply it?"
  - "Tell me about a debrief that went well — and one that went badly. What made the difference?"
  - "How much of your team's week goes into interviewing? How do you feel about that?"
- **Follow-up probes:** "Why do you re-check the recruiter's work?" · "What signal do you trust most, and why?" · "Where does your bar come from?" · "What did the bad hire cost you?"
- **Behaviors to observe:** whether they re-screen (almost always yes) and *why*; how implicit/explicit their bar is; whether debriefs are evidence-based or gut/memory.
- **Signals that VALIDATE:** re-screening is driven by *distrust* they'd drop if evidence were trustworthy; their bar is articulable enough to capture; bad hires are vivid and costly to them.
- **Signals that INVALIDATE:** they'll re-screen regardless of any tool ("I trust only my own read"); their bar is pure, unarticulable gut; they don't feel the cost of bad hires.

### 3.4 CHRO / CHIEF PEOPLE OFFICER (Sofia)
- **Goals:** whether they'd fund a pilot; whether they value quality/defensibility enough to pay; regulatory and risk posture.
- **Assumptions under test:** AS-4 (pay for quality), AS-19 (sponsor/fund), AS-7 (regulation), AS-17 (fairness matters), AS-24 (ROI). **Risks:** RK-4, RK-6, RK-12.
- **Open-ended questions:**
  - "How do you measure hiring quality today? What happens when you *can't*?"
  - "Tell me about a time hiring created legal, compliance, or brand risk here. What happened?"
  - "Walk me through how a new hiring tool actually gets budgeted and approved in your org."
  - "What hiring tools have you bought in the last two years? Which do you regret, and why?"
  - "What would you need to be able to defend your hiring to the board — or a regulator?"
  - "How do you think about AI in hiring right now? What specifically worries you?"
- **Follow-up probes:** "Why did *that* tool get funded?" · "What killed the last one?" · "Who else had to say yes?" · "What's the cost of a bad hire to you, really?"
- **Behaviors to observe:** whether quality is *actually* measured (usually not); budget authority; risk-aversion; where the real veto sits.
- **Signals that VALIDATE:** they can't currently prove quality and feel exposed; they'd fund a pilot; fairness/defensibility is a live, funded concern; ROI-on-quality resonates.
- **Signals that INVALIDATE:** only cost/speed matter; no budget or appetite; deeply skeptical of *any* AI in hiring; "we handle fairness with a policy doc" and consider it solved.

### 3.5 SECURITY / IT (Marcus)
- **Goals:** whether our (planned) model can clear review in acceptable time; deal-breakers; neutrality preference vs. incumbents.
- **Assumptions under test:** AS-20 (approval timelines), AS-25 (procurement fit), AS-22/AS-26 (integration), AS-5 (would they trust a conflicted incumbent as judge?). **Risks:** RK-9, RK-13, RK-14.
- **Open-ended questions:**
  - "Walk me through how you evaluate a new SaaS vendor that would touch candidate or employee data."
  - "Tell me about the last vendor you rejected or slowed down. What was the dealbreaker?"
  - "What does your security review timeline actually look like, start to finish?"
  - "How do you feel about a tool that integrates with your ATS and reads its data?"
  - "When a capability could come from your existing ATS vendor *or* from a specialist, how do you think about that trade-off?" *(Neutral phrasing — do not lead toward 'specialist'.)*
- **Follow-up probes:** "What's the single fastest way to get a *no* from you?" · "What would you need to see to get comfortable?" · "Who else is in that decision?"
- **Behaviors to observe:** strictness; what triggers an instant no; whether they default to incumbent-native features for safety.
- **Signals that VALIDATE:** a clearable path exists in acceptable time; they'd genuinely consider a neutral specialist; our isolation/reference-only model addresses their top concerns.
- **Signals that INVALIDATE:** chronic multi-quarter blocking; they'd *always* default to the ATS's native feature regardless of quality (a direct AS-5 / RK-9 warning).

---

## 4. Discovery Questions (by theme)

*Cross-persona, behavior-first. Use to go deeper on any theme. **Never** ask "Would you use our product?" — it produces polite lies. Ask about what they've actually done.*

- **Current workflow:** "Walk me through your actual hiring process for the last role — step by step, tools and all." · "Where does it get stuck?"
- **Current pain:** "What's the most frustrating part of hiring for you? Tell me about the last time it bit you." · "If you could delete one part of your hiring process, what would it be?"
- **Decision process:** "How do you *actually* decide who advances? Who has the real say?" · "Tell me about a decision you got wrong."
- **Trust:** "The last time you trusted a tool's recommendation — what earned that trust?" · "When have you *stopped* trusting a tool? Why?"
- **Fairness:** "Tell me about a hiring decision you weren't comfortable defending." · "What does a 'fair' process look like to you, concretely?"
- **Evidence:** "What information do you *most* wish you had about a candidate but don't?" · "What signal has actually predicted good hires for you?"
- **AI:** "Where does AI already touch your hiring? How's that going?" · "What would make you distrust an AI hiring tool immediately?"
- **Buying process:** "Walk me through how the last hiring tool got bought — who, what steps, how long." · "What kills a deal here?"
- **Security:** "What's your bar for a vendor touching candidate data?" (Security persona; also ask recruiters "has security ever blocked a tool you wanted?")
- **Competition:** "What are you using today for this? What almost got the job instead?" · "What would you go back to if a new tool disappeared?"
- **Behavior change:** "Tell me about the last time you changed how you hire. What made you actually change?" · "What made a past tool *stick* vs. get abandoned?"

---

## 5. Interview Red Flags (catch yourself)

If you notice any of these *during* the interview, correct course immediately:

- **Talking more than listening.** (Target: interviewer speaks <25% of the time.)
- **Explaining the solution too early.** You're now selling, not learning.
- **Accepting vague answers.** "It's inefficient" → "Tell me exactly what happened last time."
- **Ignoring uncomfortable evidence.** You felt a flicker of "I'll skip that" — that's the most important thread.
- **Mistaking politeness for demand.** "That sounds cool!" is not demand. Demand is what they've *paid for* or *hacked together themselves*.
- **Confirmation bias (RK-15).** You only remember the parts that support the thesis. (Antidote: §6 template forces a Contradictory-evidence field.)
- **Asking hypothetical questions.** "Would you…" / "Could you imagine…" produce fiction.
- **Treating opinions as evidence.** An opinion is L0 (VALIDATION-01 R3). It's a hypothesis, not proof.

---

## 6. Evidence Capture Template

*Fill in for **every** interview, immediately after (memory decays fast). This is the raw material that flows back into VALIDATION-01 and the Counter-Evidence Register (R4).*

```
INTERVIEW RECORD
────────────────────────────────────────────────────────
Metadata:        date · interviewer · duration · company (size/segment) · role/title
Persona:         Candidate / Recruiter / HM / CHRO / Security-IT
Assumptions tested:   AS-__ , AS-__
Risks touched:        RK-__ , RK-__
Target evidence level: L0–L1 (interview) — remember: informs, does not validate

EXACT QUOTES (verbatim — the most valuable field):
  • "…"
  • "…"

OBSERVED BEHAVIORS (what they did, not said):
  • …

SUPPORTING EVIDENCE (for which assumption):
  • AS-__ : …

CONTRADICTORY EVIDENCE (for which assumption) ← log with EQUAL rigor (R4):
  • AS-__ : …

NEW ASSUMPTIONS DISCOVERED (things we didn't know we were assuming):
  • …

UNKNOWN UNKNOWNS surfaced (not assumptions — gaps):
  • …

CONFIDENCE CHANGE (per assumption, this interview):
  • AS-__ : ↑ / ↓ / unchanged — and why

RECOMMENDED ACTIONS:
  • …
────────────────────────────────────────────────────────
```

> **Discipline:** the **Contradictory Evidence** field must not be left blank by default. If it's empty, ask yourself whether you actually listened, or whether you ran a pitch. (An interview with zero contradictory evidence is itself a red flag — RK-15.)

---

## 7. Interview Scoring

After each interview, classify **each assumption tested** on this 5-point scale:

| Score | Meaning |
|---|---|
| **Strongly Supported** | Multiple behavioral signals (not just opinions) point the same way. |
| **Weakly Supported** | Some signal, but soft or opinion-based. |
| **Neutral** | Genuinely inconclusive. (This is an honest, common result — don't force it up.) |
| **Weakly Contradicted** | Some disconfirming signal. |
| **Strongly Contradicted** | Clear behavioral evidence against the assumption. |

**Hard rules:**
- **Never mark an assumption "Validated" from interviews alone.** Interviews are **L0–L1** (VALIDATION-01 R3). The most an interview can do is move an assumption to *Weakly/Strongly Supported* as a hypothesis — validation requires **L2+ behavior** (shadowing, pilots, outcomes).
- One glowing interview ≠ support. Look for the **pattern across interviews**, and weight *behavioral* evidence over *stated* opinion.
- **Strongly Contradicted signals get escalated immediately** to the Counter-Evidence Register and re-scored against the assumption's failure criteria — especially for Core-Thesis assumptions.

---

## 8. Interview Exit Checklist

Ask these before closing **every** interview — they consistently produce the highest-value learning:

1. **"What didn't I ask about that I should have?"**
2. **"What do you think I'm misunderstanding about your world?"**
3. **"Who else should I talk to — especially someone who'd disagree with you?"**
4. **"If you were building this company, what would you do differently?"**
5. **"What would make you tell a peer *not* to use something like this?"**

> #5 is the most valuable question in the playbook. A confident, specific answer is worth ten "sounds greats."

---

## 9. Research Ethics *(a direct extension of Principle P7)*

We treat research participants exactly as we treat candidates: as first-class humans, never as subjects to be extracted from.

- **We are learning *with* people, not experimenting *on* them.**
- **Respect candidate dignity** — especially rejected candidates in Experiment C; the topic is emotionally raw. Never make them relive humiliation for our data.
- **Never deceive participants** about who we are or what we're doing.
- **Explain how their data will be used**, and honor it.
- **Obtain informed consent** — including for recording and quoting.
- **Participants should leave with value**, not just us — genuine hiring/career insight, a useful conversation, respect for their time. (If a candidate gives us their rejection story, they deserve something real back.)

> This section is not boilerplate. A company whose mission is *fairness and dignity* that runs *extractive, deceptive research* has already failed its own Constitution (P7). How we research is a test of whether we mean it.

---

## 10. Success Criteria

> **A successful interview is NOT one where people liked the idea.**

An interview succeeds when we:
- **Uncover truth** about how hiring actually works,
- **Reduce uncertainty** on a specific assumption,
- **Refine or correct** an assumption,
- **Discover a contradiction** we hadn't seen, or
- **Identify a new risk or unknown.**

If you walk out feeling *reassured and comfortable*, be suspicious — you may have run a pitch. If you walk out *unsettled, with your model of the world changed*, you did it right.

> **The uncomfortable truth this playbook enforces:** we are trying to *falsify* our company on purpose, cheaply, now — because the alternative is falsifying it expensively, later, after we've built it.

---

## Appendix — "Questions We Are Afraid to Ask"

*The most valuable questions are the ones we instinctively avoid because we fear the answer. Ask them anyway — they deliberately seek disconfirming evidence instead of reassurance. Work at least two into every interview.*

- **"Why *wouldn't* you buy this?"**
- **"What would make you stop using it after three months?"**
- **"What part of this sounds unrealistic or naïve to you?"**
- **"If this company failed, why would it have failed?"**
- **"Who inside your company would kill this deal — and why?"**
- **"What have we completely misunderstood about your world?"**
- **"What's the real reason hiring is broken that we probably haven't figured out yet?"**
- **"If I came back in a year and we'd changed nothing about how you hire, what would that tell you?"**

> If an interview never gets uncomfortable, you didn't ask these. The discomfort is where the learning is.

---

## Summary & the pivot to execution

- **KD-V03.1** — One merged, self-contained **Research Playbook** — usable live, no document-flipping.
- **KD-V03.2** — Every interview **tests named assumptions (AS-x) and reduces named risks (RK-x)**; questions are **behavior-first**, never "would you use it?"
- **KD-V03.3** — The playbook is **engineered against confirmation bias (RK-15)**: mandatory contradictory-evidence capture, behavior-over-opinion, the "afraid to ask" appendix, and "success = discovering we're wrong."
- **KD-V03.4** — **Interviews never "validate"** (L0–L1 only); they generate/score hypotheses. Validation needs L2+ behavior (shadowing, pilots, outcomes).
- **KD-V03.5** — **Research ethics = P7 applied to ourselves**; participants leave with value.

> **This is the last must-have-before-you-start artifact.** Per CTO direction: **stop writing documentation now unless a validation finding creates a clear need for a new artifact.** The remaining planned artifacts — JTBD Validation Checklist, Customer Journey Validation Script, Prototype Validation Plan, Evidence Collection Framework — are lightweight and are **better drafted *after* the first interviews**, informed by real conversations (the Evidence Capture Template §6 and Scoring §7 already cover the immediate need).
>
> **The highest-return next action is no longer writing — it is:** recruit design partners (**AS-21**), schedule interviews, run the three parallel experiments (retrospective / shadowing / rejected-candidate), and feed results back into VALIDATION-01 (assumptions) and VALIDATION-02 (risks). *That* is where the next real progress lives.

*End of VALIDATION-03 v0.1 — operational. Go talk to customers.*
