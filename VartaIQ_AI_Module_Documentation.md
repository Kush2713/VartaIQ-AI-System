# VartaIQ — AI Part Documentation
### For Team Lead & Team Members
---

## What is the AI Part?

When the meeting bot records a conversation and sends the transcript to our backend, the **AI Part** takes over. It reads every line spoken by every participant and automatically produces a full intelligent analysis — no human effort needed.

The AI Part is built as a **pipeline** — meaning the transcript passes through multiple modules one by one, and each module does one specific job. The final result is a combined JSON response that the frontend can display.

---

## How the Flow Works (Simple View)

```
Transcript (raw text)
        ↓
  Preprocessing
        ↓
  Build AI Context (shared understanding of the meeting)
        ↓
  ┌─────────────────────────────────────────┐
  │  Summary  │  Topics  │  Action Items    │
  │  Decisions│  Useless │  Speaker Analysis│
  │  Sentiment│  Scoring │  Follow-ups      │
  │           │  AI Insights               │
  └─────────────────────────────────────────┘
        ↓
  Format & Save to Database
        ↓
  Final JSON Response → Frontend
```

---

## Modules — What Each One Does

---

### 1. `transcript_preprocessor.py` — Cleaning the Input

**What it does:**
Before any analysis starts, this module cleans up the raw transcript. It removes extra spaces, fixes encoding issues, and makes sure every entry has a proper speaker name and text.

**Simple explanation:**
Think of it as a proofreader who tidies up the raw notes before passing them to the analyst.

**Input:** Raw transcript array from the bot
**Output:** Clean, consistent transcript array

---

### 2. `context_builder.py` + `context_engine.py` — Building Shared Understanding

**What it does:**
This is the brain setup. It converts the entire meeting transcript into a mathematical representation called an **embedding** — a list of numbers that captures the meaning of the whole meeting. Every other module uses this shared context to judge whether a sentence is relevant or not.

**Simple explanation:**
Imagine reading the entire meeting once and forming a mental picture of "what this meeting is about." Every module then compares each sentence against that mental picture to decide if it's important.

**Technology used:** `sentence-transformers` model (`all-MiniLM-L6-v2`)

---

### 3. `summarizer.py` — Meeting Summary

**What it does:**
Reads the most important sentences from the transcript and generates a short, clean paragraph summarizing the entire meeting.

**Simple explanation:**
Like asking someone "what happened in the meeting?" and getting a 3–4 line answer.

**Technology used:** `facebook/bart-large-cnn` (a powerful summarization AI model from Meta)

**How it handles long meetings:**
If the meeting is very long, it splits the text into chunks, summarizes each chunk, then combines them into one final summary.

---

### 4. `topic_detection.py` — What Was the Meeting About?

**What it does:**
Automatically finds the main topics discussed in the meeting. It extracts key phrases, groups similar ones together (clustering), and ranks them by how relevant they are to the overall meeting.

**Simple explanation:**
Like reading meeting notes and writing down: "Main topics discussed were: Docker Deployment, AI Pipeline Optimization, Backend APIs."

**Technology used:** spaCy (noun chunk extraction) + `AgglomerativeClustering` (grouping similar topics)

---

### 5. `action_items.py` — Who Needs to Do What?

**What it does:**
Scans every sentence for commitments and tasks. It detects phrases like "I will...", "We should...", "Please create..." and extracts:
- Who said it (speaker)
- Who is responsible (assignee)
- What the task is
- When it's due (deadline)
- How urgent it is (priority)
- How confident the AI is that this is a real task (confidence score)

**Simple explanation:**
Like a secretary who listens to the meeting and writes down every "to-do" item with the person's name next to it.

**Technology used:** spaCy NLP (dependency parsing, named entity recognition)

---

### 6. `decisions.py` — What Was Decided?

**What it does:**
Identifies sentences where a final decision was made — things like "Docker deployment is officially moved to Monday" or "Authentication APIs must be completed before release." It scores each decision by how confident it is that this is truly a decision (not just a suggestion).

**Simple explanation:**
Separates "we decided X" from "we might do X." Only confirmed decisions are captured.

**Technology used:** spaCy NLP + keyword/phrase matching with confidence scoring

---

### 7. `useless_talk.py` — Filtering Out Noise

**What it does:**
Identifies parts of the conversation that add no value — filler words ("umm", "yeah", "hmm") and off-topic discussions (like talking about the weather). It protects important sentences from being wrongly flagged by checking against the meeting context.

**Simple explanation:**
Like a highlighter that marks the irrelevant parts of the transcript so the team knows what wasted time.

**What it protects:**
- Greetings ("Good morning everyone") — normal, not flagged
- Business statements ("We agreed to improve semantic clustering") — important, not flagged
- Only genuine fillers and truly off-topic talk get flagged

---

### 8. `speaker_analysis.py` — How Did Each Person Contribute?

**What it does:**
Analyzes every participant's contribution across multiple dimensions:
- How many words they spoke
- What percentage of the meeting they participated in
- How relevant their sentences were to the meeting topic
- How many productive/action-oriented sentences they had
- How many decisions they contributed to
- Their overall effectiveness score and engagement level

**Simple explanation:**
Like a report card for each participant — who was actively contributing, who was passive, and who drove the decisions.

**Engagement Levels:**
- **High** — Effectiveness score ≥ 55
- **Medium** — Effectiveness score ≥ 30
- **Low** — Below 30

---

### 9. `sentiment_analysis.py` — What Was the Mood?

**What it does:**
Analyzes the emotional tone of the meeting. It detects:
- Whether each sentence is Positive, Neutral, or Negative
- Operational risks (mentions of failures, latency, bugs, deployment issues)
- Conflicts or disagreements between participants
- An overall meeting sentiment score (0–100)

**Simple explanation:**
Like reading the room — was the meeting tense, optimistic, or neutral? Were there any red flags raised?

**Technology used:** `cardiffnlp/twitter-roberta-base-sentiment-latest` (a sentiment AI model)

**Important note:** Technical risk words ("latency", "slow", "optimization") are NOT treated as negative — they're just flagged as operational risks, which is normal in a tech meeting.

---

### 10. `scoring.py` — Overall Meeting Score

**What it does:**
Combines all the analysis into a single meeting quality score (0–100) with a rating.

**Score Breakdown:**

| Component | Weight | What it measures |
|---|---|---|
| Action Score | 25% | Quality of action items extracted |
| Decision Score | 20% | Quality of decisions made |
| Balance Score | 15% | How evenly participants contributed |
| Productivity Score | 15% | How task-focused the discussion was |
| Relevance Score | 15% | How on-topic the conversation was |
| Conversation Score | 10% | How little filler/off-topic talk there was |

**Ratings:**
- **Excellent** — Score ≥ 75
- **Good** — Score ≥ 58
- **Average** — Score ≥ 40
- **Poor** — Below 40

---

### 11. `followup_generator.py` — Follow-Up Reminders

**What it does:**
Converts action items, decisions, and risks into clean, readable follow-up sentences that can be sent to participants after the meeting.

**Simple explanation:**
Automatically writes the "meeting minutes" follow-up email content.

**Example output:**
- "Akshay should deploy the updated summarization engine this weekend. This is a high-priority task."
- "Ensure alignment and execution for decision: Docker deployment is officially moved to Monday."
- "Monitor operational risk: PostgreSQL queries are becoming a problem."

---

### 12. `llm_enhancer.py` — AI Insights

**What it does:**
Generates human-readable insight statements about the meeting — how productive it was, how each speaker performed, what risks were detected, and what the main focus areas were.

**Simple explanation:**
The "executive summary" layer — gives a quick, plain-English verdict on the meeting quality.

**Technology used:** `google/flan-t5-base` (a text generation AI model from Google)

---

### 13. `deduplication.py` — Removing Duplicates

**What it does:**
After all modules run, there can be duplicate action items or decisions that mean the same thing but are worded differently. This module uses semantic similarity to detect and remove near-duplicate entries.

**Simple explanation:**
If two action items say "finalize the backend APIs" and "complete the backend API work," it keeps only one.

---

### 14. `validators.py` — Quality Gate

**What it does:**
Filters out low-confidence results before they reach the final response. For example, action items with confidence below 0.55 are dropped, and decisions with confidence below 0.60 are removed.

**Simple explanation:**
A quality checker that removes uncertain or weak results so the final output is clean and reliable.

---

## Understanding the Full Response

Here is every part of the JSON response explained:

---

### `summary`
A 3–5 sentence paragraph summarizing the entire meeting. Generated by the BART AI model from the most important sentences.

```json
"summary": "We need to finalize the VartaIQ backend APIs and complete 
authentication integration before Friday. Docker deployment is officially 
moved to Monday..."
```

---

### `topics`
The top meeting topics ranked by relevance. Each topic has a relevance score (0 to 1) showing how central it was to the meeting.

```json
"topics": [
  { "topic": "Docker Deployment", "relevance_score": 0.41 },
  { "topic": "Ai Pipeline Optimization", "relevance_score": 0.36 }
]
```
Higher score = more central to the meeting discussion.

---

### `action_items`
Every task or commitment extracted from the meeting. Each item includes:

| Field | Meaning |
|---|---|
| `speaker` | Who said it |
| `assignee` | Who is responsible |
| `task` | What needs to be done |
| `deadline` | When it's due |
| `priority` | Normal / Medium / High |
| `confidence` | How sure the AI is (0 to 1) |

```json
{
  "speaker": "Akshay",
  "assignee": "Akshay",
  "task": "Deploy the updated summarization engine this weekend",
  "deadline": "This weekend",
  "priority": "High",
  "confidence": 1.0
}
```

---

### `decisions`
Confirmed decisions made during the meeting. Each has a `decision_confidence` score — closer to 1.0 means it was very clearly a final decision.

```json
{
  "speaker": "Akshay",
  "decision": "Docker deployment is officially moved to Monday.",
  "decision_confidence": 1.0
}
```

---

### `useless_talk`
Segments of the conversation that were either filler or off-topic. Each segment shows:
- Who said it
- What they said
- Why it was flagged (Filler conversation / Off-topic discussion)
- Its relevance score (0 = completely irrelevant)

```json
{
  "speaker": "Rahul",
  "text": "Hmm",
  "reason": "Filler conversation",
  "relevance_score": 0.0
}
```

---

### `speaker_analysis`
A detailed breakdown for each participant:

| Field | Meaning |
|---|---|
| `word_count` | Total words spoken |
| `participation_percentage` | % of total meeting words |
| `relevance_ratio` | % of their sentences that were on-topic |
| `productivity_ratio` | % of their sentences that were task-oriented |
| `average_relevance` | Average semantic relevance score (0–1) |
| `effectiveness_score` | Combined score of all above metrics |
| `engagement_level` | High / Medium / Low |
| `dominant_speaker` | True if they spoke > 35% of the meeting |
| `passive_participant` | True if they spoke < 10% of the meeting |

---

### `sentiment_analysis`
The emotional and risk analysis of the meeting:

| Field | Meaning |
|---|---|
| `overall_sentiment` | Positive / Neutral / Negative |
| `overall_score` | 0–100 (50 = neutral, 100 = very positive) |
| `operational_risk_level` | Low / Medium / High |
| `risk_count` | Number of risk-related statements |
| `conflict_count` | Number of conflict/disagreement signals |
| `risks` | List of risky statements with the risk terms highlighted |
| `conflicts` | List of conflict statements |
| `conversation_sentiments` | Per-sentence sentiment with confidence |

---

### `score`
The overall meeting quality score:

```json
{
  "final_score": 73.02,
  "rating": "Good",
  "breakdown": {
    "productivity_score": 33.57,
    "relevance_score": 31.0,
    "balance_score": 80.97,
    "action_score": 91.43,
    "decision_score": 100.0,
    "conversation_score": 83.33
  }
}
```

The `final_score` is a weighted combination of all breakdown scores. Rating is Good here because action items and decisions were strong, and participation was balanced.

---

### `followups`
Ready-to-send follow-up reminders generated from action items, decisions, and risks:

```json
[
  "Akshay should deploy the updated summarization engine this weekend. This is a high-priority task.",
  "Ensure alignment and execution for decision: Docker deployment is officially moved to Monday.",
  "Monitor operational risk: PostgreSQL queries are becoming a problem.",
  "Meeting productivity was good, with clear technical discussion and execution planning."
]
```

---

### `ai_insights`
Plain-English observations about the meeting quality and participants:

```json
[
  "Meeting was productive with clear task ownership and actionable outcomes.",
  "Strong actionable commitments were identified with clear ownership.",
  "Decisions were well-defined and confirmed during the meeting.",
  "Akshay, Riya, Sneha contributed meaningfully to the discussion.",
  "Rahul had limited participation. Encouraging more structured input could help.",
  "3 operational or technical risk discussions were detected.",
  "Primary meeting focus areas included: Docker Deployment, AI Pipeline Optimization."
]
```

---

## Technology Stack Summary

| Technology | Purpose |
|---|---|
| **FastAPI** | Web framework — handles the POST /analyze API |
| **spaCy** (`en_core_web_sm`) | NLP — sentence parsing, dependency analysis, named entities |
| **BART** (`facebook/bart-large-cnn`) | AI summarization model |
| **FLAN-T5** (`google/flan-t5-base`) | Text generation for insights |
| **RoBERTa** (`cardiffnlp/twitter-roberta-base-sentiment-latest`) | Sentiment analysis model |
| **Sentence Transformers** (`all-MiniLM-L6-v2`) | Semantic embeddings for relevance scoring |
| **scikit-learn** | Topic clustering (AgglomerativeClustering) |
| **SQLAlchemy + PostgreSQL** | Database — stores every meeting analysis |
| **Pydantic** | Request/response validation |

---

## Quick Reference — Module to Response Field

| Response Field | Module Responsible |
|---|---|
| `summary` | `summarizer.py` + `llm_enhancer.py` |
| `topics` | `topic_detection.py` |
| `action_items` | `action_items.py` + `validators.py` |
| `decisions` | `decisions.py` + `validators.py` |
| `useless_talk` | `useless_talk.py` |
| `speaker_analysis` | `speaker_analysis.py` |
| `sentiment_analysis` | `sentiment_analysis.py` |
| `score` | `scoring.py` |
| `followups` | `followup_generator.py` |
| `ai_insights` | `llm_enhancer.py` |

---

*Document prepared for VartaIQ — AI Meeting Analyzer*
*AI Part developed using FastAPI, HuggingFace Transformers, spaCy, and Sentence Transformers*
