import re


# =====================================
# FILLER WORDS
# =====================================

FILLER_WORDS = {

    "umm",
    "uh",
    "hmm",
    "yeah",
    "okay",
    "like",
    "basically",
    "actually"
}


# =====================================
# REMOVE REPETITIVE WORDS
# =====================================

def remove_repeated_words(
    text
):

    words = text.split()

    cleaned = []

    previous = None

    for word in words:

        normalized = (
            word.lower().strip()
        )

        if normalized == previous:
            continue

        cleaned.append(word)

        previous = normalized

    return " ".join(cleaned)


# =====================================
# REMOVE EXCESSIVE FILLERS
# =====================================

def remove_filler_noise(
    text
):

    words = text.split()

    meaningful = []

    filler_streak = 0

    for word in words:

        normalized = (
            word.lower().strip(".,!?")
        )

        if normalized in FILLER_WORDS:

            filler_streak += 1

            # Allow only limited fillers
            if filler_streak > 1:
                continue

        else:

            filler_streak = 0

        meaningful.append(word)

    return " ".join(meaningful)


# =====================================
# CLEAN PUNCTUATION
# =====================================

def normalize_punctuation(
    text
):

    # Remove repeated punctuation
    text = re.sub(
        r"([!?.,])\1+",
        r"\1",
        text
    )

    # Normalize spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    text = text.strip()

    return text


# =====================================
# REMOVE DUPLICATE SENTENCES
# =====================================

def remove_duplicate_sentences(
    transcript
):

    unique_texts = set()

    cleaned = []

    for item in transcript:

        normalized = (

            item["text"]

            .lower()

            .strip()
        )

        if normalized in unique_texts:
            continue

        unique_texts.add(
            normalized
        )

        cleaned.append(item)

    return cleaned


# =====================================
# CLEAN SINGLE UTTERANCE
# =====================================

def clean_utterance(text):

    text = remove_repeated_words(
        text
    )

    text = remove_filler_noise(
        text
    )

    text = normalize_punctuation(
        text
    )

    return text


# =====================================
# MAIN PREPROCESSOR
# =====================================

def preprocess_transcript(
    transcript
):

    cleaned_transcript = []

    # ---------------------------------
    # Remove duplicate utterances
    # ---------------------------------

    transcript = (
        remove_duplicate_sentences(
            transcript
        )
    )

    # ---------------------------------
    # Clean utterances
    # ---------------------------------

    for item in transcript:

        cleaned_text = clean_utterance(
            item["text"]
        )

        # Skip empty text
        if not cleaned_text:
            continue

        cleaned_transcript.append({

            "speaker":
                item["speaker"],

            "text":
                cleaned_text
        })

    return cleaned_transcript