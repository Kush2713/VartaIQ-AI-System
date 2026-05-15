from collections import Counter
import re

# =====================================
# EXTRACTIVE SUMMARIZATION
# No external API needed - pure Python
# =====================================

summarizer = None  # Not using HF API anymore

# =====================================
# CONFIGURATION
# =====================================

MAX_CHUNK_WORDS = 400

MIN_SUMMARY_LENGTH = 40

MAX_SUMMARY_LENGTH = 120

# =====================================
# IMPORTANT KEYWORDS
# =====================================

IMPORTANT_TERMS = {

    "decision",
    "deadline",
    "deploy",
    "deployment",
    "risk",
    "latency",
    "optimization",
    "release",
    "dashboard",
    "api",
    "authentication",
    "testing",
    "database",
    "performance",
    "analytics",
    "pipeline",
    "summary",
    "integration",
    "memory",
    "scaling",
    "frontend",
    "backend"
}

# =====================================
# TRANSCRIPT -> TEXT
# =====================================

def transcript_to_text(
    transcript
):

    parts = []

    for item in transcript:

        speaker = item.get(
            "speaker",
            "Unknown"
        )

        text = item.get(
            "text",
            ""
        )

        parts.append(
            f"{speaker}: {text}"
        )

    return " ".join(parts)

# =====================================
# CHUNK LARGE TEXT
# =====================================

def chunk_text(
    text,
    max_words=MAX_CHUNK_WORDS
):

    words = text.split()

    chunks = []

    current = []

    count = 0

    for word in words:

        current.append(word)

        count += 1

        if count >= max_words:

            chunks.append(
                " ".join(current)
            )

            current = []

            count = 0

    if current:

        chunks.append(
            " ".join(current)
        )

    return chunks

# =====================================
# SENTENCE SCORING
# =====================================

def score_sentence(sentence, important_terms, indicators):
    """
    Score a sentence based on importance indicators
    """
    lowered = sentence.lower()
    score = 0
    
    # Keyword scoring
    for term in important_terms:
        if term in lowered:
            score += 1
    
    # Action/decision indicators
    for indicator in indicators:
        if indicator in lowered:
            score += 2
    
    # Length penalty (too short or too long)
    word_count = len(sentence.split())
    if word_count < 5:
        score -= 2
    elif word_count > 50:
        score -= 1
    
    # Question sentences are less important
    if '?' in sentence:
        score -= 1
    
    return score

# =====================================
# EXTRACTIVE SUMMARIZATION
# =====================================

def extractive_summarize(transcript, max_sentences=4):
    """
    Create summary by extracting most important sentences
    """
    indicators = [
        "we should",
        "we need to",
        "final decision",
        "agreed",
        "officially",
        "must",
        "important",
        "risk",
        "deadline",
        "will complete",
        "will prepare",
        "will implement",
        "decided to",
        "approved",
        "finalized"
    ]
    
    # Score all sentences
    scored_sentences = []
    
    for item in transcript:
        text = item.get("text", "").strip()
        if not text:
            continue
        
        # Split into sentences
        sentences = re.split(r'[.!]+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:  # Skip very short fragments
                continue
            
            score = score_sentence(sentence, IMPORTANT_TERMS, indicators)
            
            if score > 0:  # Only keep sentences with positive score
                scored_sentences.append((score, sentence))
    
    # Sort by score and take top sentences
    scored_sentences.sort(reverse=True, key=lambda x: x[0])
    top_sentences = [sent for score, sent in scored_sentences[:max_sentences]]
    
    # Join into summary
    if top_sentences:
        summary = ". ".join(top_sentences)
        if not summary.endswith('.'):
            summary += "."
        return summary
    else:
        return "Meeting discussion covered various topics and action items."

# =====================================
# MODEL SUMMARY (DEPRECATED - Using extractive now)
# =====================================

def summarize_chunk(chunk):
    """
    Fallback to extractive summarization
    """
    # Parse chunk back to transcript-like format
    lines = chunk.split(". ")
    mock_transcript = [{"text": line} for line in lines if line.strip()]
    
    return extractive_summarize(mock_transcript, max_sentences=2)

# =====================================
# EXTRACT IMPORTANT SENTENCES
# =====================================

def extract_important_sentences(
    transcript
):

    important = []

    for item in transcript:

        text = item.get(
            "text",
            ""
        ).strip()

        lowered = text.lower()

        score = 0

        # -----------------------------
        # Keyword scoring
        # -----------------------------

        for term in IMPORTANT_TERMS:

            if term in lowered:
                score += 1

        # -----------------------------
        # Action/decision indicators
        # -----------------------------

        indicators = [

            "we should",
            "we need to",
            "final decision",
            "agreed",
            "officially",
            "must",
            "important",
            "risk",
            "deadline"
        ]

        for indicator in indicators:

            if indicator in lowered:
                score += 2

        # -----------------------------
        # Sentence qualification
        # -----------------------------

        if score >= 2:

            important.append(text)

    return important

# =====================================
# BUILD STRUCTURED CONTEXT
# =====================================

def build_structured_context(
    transcript
):

    important_sentences = (
        extract_important_sentences(
            transcript
        )
    )

    # ---------------------------------
    # Fallback if extraction weak
    # ---------------------------------

    if not important_sentences:

        important_sentences = [

            item["text"]

            for item in transcript
        ]

    return " ".join(
        important_sentences
    )

# =====================================
# HIERARCHICAL SUMMARIZATION
# =====================================

def hierarchical_summarize(text):
    """
    For large meetings, summarize in chunks then combine
    """
    chunks = chunk_text(text)
    
    summaries = []
    
    # Summarize each chunk
    for chunk in chunks:
        summary = summarize_chunk(chunk)
        summaries.append(summary)
    
    # Combine all summaries
    combined = " ".join(summaries)
    
    return combined

# =====================================
# CLEAN SUMMARY
# =====================================

def clean_summary(summary):

    summary = summary.strip()

    # Strip model-generated "Summary:" prefix
    if summary.lower().startswith("summary:"):
        summary = summary[len("summary:"):].strip()

    replacements = {

        "will discuss":
            "discussed",

        "will work on":
            "worked on",

        "will finalize":
            "finalized",

        "will deploy":
            "deployment planning included",

        "will improve":
            "improvements focused on",

        "going to":
            "",

        "today":
            ""
    }

    lowered = summary.lower()

    for old, new in (
        replacements.items()
    ):

        lowered = lowered.replace(
            old,
            new
        )

    # Capitalize properly
    if len(lowered) > 1:

        lowered = (
            lowered[0].upper()
            + lowered[1:]
        )

    return lowered

# =====================================
# MAIN SUMMARIZATION
# =====================================

def summarize(transcript):
    """
    Main summarization function using extractive approach
    """
    try:
        # Use extractive summarization (no API needed)
        summary = extractive_summarize(transcript, max_sentences=5)
        
        # Clean up the summary
        summary = clean_summary(summary)
        
        return summary
    
    except Exception as e:
        print(f"[SUMMARIZER CRITICAL ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Ultimate fallback
        return "Meeting summary: Discussion covered key topics, decisions, and action items."


