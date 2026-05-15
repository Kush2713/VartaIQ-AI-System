from collections import Counter

from app.services.model_manager import (
    get_summarizer_model
)

# =====================================
# LOAD CENTRALIZED MODEL
# =====================================

summarizer = (
    get_summarizer_model()
)

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
# MODEL SUMMARY
# =====================================

def summarize_chunk(chunk):

    try:
        result = summarizer(

            chunk,

            max_length=
            MAX_SUMMARY_LENGTH,

            min_length=
            MIN_SUMMARY_LENGTH,

            do_sample=False
        )

        return result[0][
            "summary_text"
        ]
    
    except Exception as e:
        print(f"[SUMMARIZER ERROR] {str(e)}")
        # Fallback: return first 100 words
        words = chunk.split()[:100]
        return " ".join(words) + "..."

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

def hierarchical_summarize(
    text
):

    chunks = chunk_text(text)

    summaries = []

    # ---------------------------------
    # Summarize chunks
    # ---------------------------------

    for chunk in chunks:

        summary = summarize_chunk(
            chunk
        )

        summaries.append(
            summary
        )

    # ---------------------------------
    # Merge summaries
    # ---------------------------------

    merged = " ".join(
        summaries
    )

    # ---------------------------------
    # Final abstraction summary
    # ---------------------------------

    final_result = summarizer(

        merged,

        max_length=160,

        min_length=60,

        do_sample=False
    )

    return final_result[0][
        "summary_text"
    ]

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

def summarize(
    transcript
):

    try:
        # ---------------------------------
        # Structured context generation
        # ---------------------------------

        structured_context = (
            build_structured_context(
                transcript
            )
        )

        # ---------------------------------
        # Word count
        # ---------------------------------

        word_count = len(
            structured_context.split()
        )

        # ---------------------------------
        # Small meeting optimization
        # ---------------------------------

        if word_count <= (
            MAX_CHUNK_WORDS
        ):

            result = summarizer(

                structured_context,

                max_length=140,

                min_length=50,

                do_sample=False
            )

            summary = result[0][
                "summary_text"
            ]

        # ---------------------------------
        # Large meeting optimization
        # ---------------------------------

        else:

            summary = (
                hierarchical_summarize(
                    structured_context
                )
            )

        # ---------------------------------
        # Final cleanup
        # ---------------------------------

        summary = clean_summary(
            summary
        )

        return summary
    
    except Exception as e:
        print(f"[SUMMARIZER CRITICAL ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Fallback: Create extractive summary
        important_sentences = extract_important_sentences(transcript)
        if important_sentences:
            fallback_summary = ". ".join(important_sentences[:3]) + "."
            return fallback_summary
        else:
            return "Meeting summary could not be generated. Please check the transcript data."


