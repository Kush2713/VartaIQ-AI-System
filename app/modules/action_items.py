import re
import spacy

from app.modules.deduplication import (
    semantic_deduplicate
)

nlp = spacy.load("en_core_web_sm")


# =====================================
# ACTION VERBS
# =====================================

ACTION_VERBS = {
    "complete",
    "finish",
    "submit",
    "prepare",
    "design",
    "implement",
    "integrate",
    "deploy",
    "test",
    "review",
    "create",
    "update",
    "fix",
    "send",
    "optimize",
    "improve",
    "deliver",
    "build"
}


# =====================================
# MODAL / COMMITMENT WORDS
# =====================================

MODAL_WORDS = {
    "will",
    "should",
    "need",
    "must",
    "shall"
}


# =====================================
# DEADLINE PATTERNS
# =====================================

DEADLINE_PATTERNS = [

    r"by\s+\w+",

    r"before\s+\w+",

    r"tomorrow",

    r"tonight",

    r"today",

    r"next week",

    r"this weekend",

    r"monday",

    r"tuesday",

    r"wednesday",

    r"thursday",

    r"friday"
]


# =====================================
# PRIORITY KEYWORDS
# =====================================

PRIORITY_KEYWORDS = {

    "urgent": "High",

    "immediately": "High",

    "asap": "High",

    "critical": "High",

    "important": "Medium",

    "priority": "Medium",

    "later": "Low",

    "eventually": "Low"
}


# =====================================
# DEADLINE DETECTION
# =====================================

def detect_deadline(text):

    lowered = text.lower()

    for pattern in DEADLINE_PATTERNS:

        match = re.search(
            pattern,
            lowered
        )

        if match:
            return match.group()

    return None


# =====================================
# PRIORITY DETECTION
# =====================================

def detect_priority(text):

    lowered = text.lower()

    for keyword, level in (
        PRIORITY_KEYWORDS.items()
    ):

        if keyword in lowered:
            return level

    return "Normal"


# =====================================
# CONTEXTUAL ASSIGNEE DETECTION
# =====================================

def extract_assignee(
    sent,
    default_speaker
):

    # ---------------------------------
    # FIRST PRIORITY:
    # Grammatical subject
    # ---------------------------------

    for token in sent:

        if token.dep_ in {
            "nsubj",
            "nsubjpass"
        }:

            subject = token.text.strip()

            lowered = subject.lower()

            if lowered in {
                "i",
                "we"
            }:
                return default_speaker

            if token.pos_ == "PROPN":
                return subject

    # ---------------------------------
    # SECOND PRIORITY:
    # Named entities
    # ---------------------------------

    for ent in sent.ents:

        if ent.label_ != "PERSON":
            continue

        entity_text = ent.text.strip()

        if entity_text.lower() in {

            "swagger",
            "postgresql",
            "docker",
            "api",
            "backend",
            "frontend",
            "database",
            "github",
            "figma"
        }:
            continue

        return entity_text

    # ---------------------------------
    # FINAL FALLBACK
    # ---------------------------------

    return default_speaker


# =====================================
# CONFIDENCE SCORING
# =====================================

def calculate_confidence(
    has_modal,
    has_action_verb,
    has_deadline,
    has_priority
):

    score = 0.40

    if has_modal:
        score += 0.20

    if has_action_verb:
        score += 0.25

    if has_deadline:
        score += 0.10

    if has_priority:
        score += 0.05

    return round(
        min(score, 1.0),
        2
    )


# =====================================
# TASK CLEANING
# =====================================

def clean_task(task):

    fillers = [
        "yeah",
        "okay",
        "umm",
        "uh",
        "basically",
        "actually"
    ]

    # Preserve original casing — only strip fillers
    cleaned = task

    for filler in fillers:

        # Case-insensitive filler removal
        import re
        cleaned = re.sub(
            r'\b' + filler + r'\b',
            '',
            cleaned,
            flags=re.IGNORECASE
        )

    cleaned = " ".join(
        cleaned.split()
    )

    return cleaned.strip().capitalize()


# =====================================
# ACTIONABILITY DETECTION
# =====================================

def is_actionable(sent):

    text = sent.text.lower()

    has_modal = any(

        word in text

        for word in MODAL_WORDS
    )

    has_action_verb = False

    for token in sent:

        if (
            token.lemma_.lower()
            in ACTION_VERBS
        ):

            has_action_verb = True

            break

    root = sent.root

    imperative = (

        root.pos_ == "VERB"

        and

        root.lemma_.lower()
        in ACTION_VERBS
    )

    actionable = (
        (has_modal and has_action_verb)
        or
        imperative
    )

    return (
        actionable,
        has_modal,
        has_action_verb
    )


# =====================================
# COMMITMENT DETECTION
# =====================================

def detect_commitment(sent):

    for token in sent:

        if token.dep_ in {
            "nsubj",
            "nsubjpass"
        }:

            head = token.head

            if (

                head.pos_ == "VERB"

                and

                head.lemma_.lower()
                in ACTION_VERBS
            ):

                return True

    return False


# =====================================
# MAIN ACTION ITEM EXTRACTION
# =====================================

def extract_action_items(data):

    actions = []

    for item in data:

        doc = nlp(item["text"])

        for sent in doc.sents:

            (
                actionable,
                has_modal,
                has_action_verb
            ) = is_actionable(sent)

            commitment = detect_commitment(
                sent
            )

            if actionable or commitment:

                deadline = detect_deadline(
                    sent.text
                )

                priority = detect_priority(
                    sent.text
                )

                assignee = extract_assignee(

                    sent,

                    item["speaker"]
                )

                confidence = (
                    calculate_confidence(

                        has_modal,

                        has_action_verb,

                        deadline is not None,

                        priority != "Normal"
                    )
                )

                actions.append({

                    "speaker":
                        item["speaker"],

                    "assignee":
                        assignee,

                    "task":
                        clean_task(
                            sent.text
                        ),

                    "deadline":
                        deadline,

                    "priority":
                        priority,

                    "confidence":
                        confidence
                })

    # =================================
    # SEMANTIC DEDUPLICATION
    # =================================

    actions = semantic_deduplicate(

        actions,

        "task"
    )

    return actions






















# import re
# import spacy

# nlp = spacy.load("en_core_web_sm")


# ACTION_VERBS = {
#     "complete",
#     "finish",
#     "submit",
#     "prepare",
#     "design",
#     "implement",
#     "integrate",
#     "deploy",
#     "test",
#     "review",
#     "create",
#     "update",
#     "fix",
#     "send",
#     "optimize",
#     "improve"
# }


# MODAL_WORDS = {
#     "will",
#     "should",
#     "need",
#     "must",
#     "shall"
# }


# DEADLINE_PATTERNS = [
#     r"by\s+\w+",
#     r"before\s+\w+",
#     r"tomorrow",
#     r"tonight",
#     r"today",
#     r"next week",
#     r"this weekend"
# ]

# PRIORITY_KEYWORDS = {

#     "urgent": "High",
#     "immediately": "High",
#     "asap": "High",
#     "critical": "High",

#     "important": "Medium",
#     "priority": "Medium",

#     "later": "Low",
#     "eventually": "Low"
# }


# def detect_deadline(text):
#     """
#     Extracts basic deadline references.
#     """

#     lowered = text.lower()

#     for pattern in DEADLINE_PATTERNS:

#         match = re.search(pattern, lowered)

#         if match:
#             return match.group()

#     return None

# def detect_priority(text):
#     """
#     Detects task priority.
#     """

#     lowered = text.lower()

#     for keyword, level in PRIORITY_KEYWORDS.items():

#         if keyword in lowered:
#             return level

#     return "Normal"


# def extract_assignee(sent, default_speaker):
#     """
#     Attempts to identify task owner.
#     """

#     for ent in sent.ents:

#         if ent.label_ == "PERSON":
#             return ent.text

#     return default_speaker


# def calculate_confidence(
#     has_modal,
#     has_action_verb,
#     has_deadline
# ):
#     """
#     Confidence estimation for action item.
#     """

#     score = 0.4

#     if has_modal:
#         score += 0.25

#     if has_action_verb:
#         score += 0.25

#     if has_deadline:
#         score += 0.10

#     return round(min(score, 1.0), 2)


# def clean_task(task):

#     fillers = [
#         "yeah",
#         "okay",
#         "umm",
#         "uh"
#     ]

#     cleaned = task.lower()

#     for filler in fillers:
#         cleaned = cleaned.replace(
#             filler,
#             ""
#         )

#     return " ".join(
#         cleaned.split()
#     ).strip().capitalize()


# def is_actionable(sent):
#     """
#     Detects actionable intent.
#     """

#     text = sent.text.lower()

#     has_modal = any(
#         word in text
#         for word in MODAL_WORDS
#     )

#     has_action_verb = False

#     for token in sent:

#         if (
#             token.lemma_.lower()
#             in ACTION_VERBS
#         ):
#             has_action_verb = True
#             break

#     # Imperative detection
#     root = sent.root

#     imperative = (
#         root.pos_ == "VERB"
#         and
#         root.lemma_.lower()
#         in ACTION_VERBS
#     )

#     actionable = (
#         (has_modal and has_action_verb)
#         or
#         imperative
#     )

#     return (
#         actionable,
#         has_modal,
#         has_action_verb
#     )

# def detect_commitment(sent):
#     """
#     Uses dependency parsing to detect
#     strong commitment intent.
#     """

#     for token in sent:

#         # Subject + future action structure
#         if token.dep_ in {"nsubj", "nsubjpass"}:

#             head = token.head

#             if (
#                 head.pos_ == "VERB"
#                 and
#                 head.lemma_.lower()
#                 in ACTION_VERBS
#             ):
#                 return True

#     return False

# def extract_action_items(data):

#     actions = []

#     for item in data:

#         doc = nlp(item["text"])

#         for sent in doc.sents:

#             (
#                 actionable,
#                 has_modal,
#                 has_action_verb
#             ) = is_actionable(sent)

#             if actionable:

#                 deadline = detect_deadline(
#                     sent.text
#                 )

#                 assignee = extract_assignee(
#                     sent,
#                     item["speaker"]
#                 )

#                 confidence = (
#                     calculate_confidence(
#                         has_modal,
#                         has_action_verb,
#                         deadline is not None
#                     )
#                 )

#                 actions.append({

#                     "speaker":
#                         item["speaker"],

#                     "assignee":
#                         assignee,

#                     "task":
#                         clean_task(sent.text),

#                     "deadline":
#                         deadline,

#                     "confidence":
#                         confidence
#                 })

#     return actions


















































# # # import spacy

# # # nlp = spacy.load("en_core_web_sm")


# # # def extract_action_items(data):
# # #     actions = []

# # #     for item in data:
# # #         doc = nlp(item["text"])

# # #         for sent in doc.sents:
# # #             if any(token.dep_ == "ROOT" and token.pos_ == "VERB" for token in sent):
# # #                 if "will" in sent.text.lower() or "should" in sent.text.lower():
# # #                     actions.append({
# # #                         "speaker": item["speaker"],
# # #                         "task": sent.text.strip()
# # #                     })

# # #     return actions

# # import spacy

# # nlp = spacy.load("en_core_web_sm")

# # ACTION_VERBS = {
# #     "complete",
# #     "finish",
# #     "submit",
# #     "prepare",
# #     "design",
# #     "implement",
# #     "integrate",
# #     "deploy",
# #     "test",
# #     "review",
# #     "create",
# #     "update",
# #     "fix",
# #     "send"
# # }

# # MODAL_WORDS = {
# #     "will",
# #     "should",
# #     "need",
# #     "must",
# #     "shall"
# # }


# # def is_actionable(sent):
# #     """
# #     Determines whether a sentence contains actionable intent.
# #     """

# #     text = sent.text.lower()

# #     # Rule 1: Modal commitment language
# #     if any(word in text for word in MODAL_WORDS):

# #         # Check if meaningful action verb exists
# #         for token in sent:
# #             if token.lemma_.lower() in ACTION_VERBS:
# #                 return True

# #     # Rule 2: Imperative task detection
# #     root = sent.root

# #     if root.pos_ == "VERB":
# #         if root.lemma_.lower() in ACTION_VERBS:
# #             return True

# #     return False


# # def clean_task(task):
# #     fillers = ["yeah", "okay", "umm", "uh"]

# #     cleaned = task

# #     for filler in fillers:
# #         cleaned = cleaned.replace(filler, "")

# #     return " ".join(cleaned.split()).strip().capitalize()


# # def extract_action_items(data):
# #     actions = []

# #     for item in data:
# #         doc = nlp(item["text"])

# #         for sent in doc.sents:

# #             if is_actionable(sent):

# #                 actions.append({
# #                     "speaker": item["speaker"],
# #                     "task": clean_task(sent.text)
# #                 })

# #     return actions


# # # This module is already better than decisions.py, because it uses spaCy parsing.

# # # But it still has major limitations:

# # # too dependent on "will" and "should", missed: "Akshay needs to complete backend integration"
# # # weak semantic understanding
# # # misses many real tasks
# # # generates noisy tasks sometimes