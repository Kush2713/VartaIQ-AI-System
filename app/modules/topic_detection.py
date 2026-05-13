import spacy

from sklearn.cluster import AgglomerativeClustering

from app.modules.context_engine import (

    embedding_model,

    generate_sentence_embedding,

    generate_meeting_embedding,

    calculate_semantic_similarity
)

from app.modules.deduplication import (
    semantic_deduplicate
)

from app.config.ai_config import (

    MIN_TOPIC_LENGTH,

    MAX_TOPICS,

    TOPIC_SIMILARITY_THRESHOLD
)

nlp = spacy.load("en_core_web_sm")


# =====================================
# TOPIC NOISE BLOCKLIST
# Overly specific phrases that are
# details, not meeting topics
# =====================================

TOPIC_BLOCKLIST = {

    "all swagger endpoints",
    "swagger endpoints",
    "all endpoints",
    "the latest fixes",
    "latest fixes",
    "the next release",
    "next release",
    "the qa team",
    "qa team",
    "more testing time",
    "the client",
    "the team",
    "the meeting",
    "the weekend",
    "tomorrow evening",
    "tonight",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "the demo",
    "demo performance",
    "client presentation",
    "the model",
    "the database",
    "the backend",
    "the frontend"
}


# =====================================
# STOP PREFIXES
# =====================================

STOP_PREFIXES = {

    "the",
    "a",
    "an"
}


# =====================================
# CLEAN TOPIC
# =====================================

def clean_topic_text(topic):

    words = topic.split()

    while (
        len(words) > 1
        and words[0].lower()
        in STOP_PREFIXES
    ):

        words.pop(0)

    cleaned = " ".join(words)

    return cleaned.strip()


# =====================================
# EXTRACT CANDIDATE TOPICS
# =====================================

def extract_candidate_topics(transcript):

    phrases = []

    for item in transcript:

        doc = nlp(item["text"])

        for chunk in doc.noun_chunks:

            phrase = (
                chunk.text
                .strip()
                .lower()
            )

            if len(phrase) < (
                MIN_TOPIC_LENGTH
            ):
                continue

            if phrase in {

                "i",
                "we",
                "it",
                "this",
                "that",
                "they"
            }:
                continue

            # Skip blocklisted noise phrases
            if phrase in TOPIC_BLOCKLIST:
                continue

            cleaned = clean_topic_text(
                phrase
            )

            if cleaned:
                phrases.append(
                    cleaned
                )

    return list(set(phrases))


# =====================================
# EMBEDDINGS
# =====================================

def generate_topic_embeddings(topics):

    if not topics:
        return []

    return embedding_model.encode(
        topics
    )


# =====================================
# CLUSTER TOPICS
# =====================================

def cluster_topics(
    topics,
    embeddings
):

    if len(topics) <= 1:
        return topics

    clustering = AgglomerativeClustering(

        n_clusters=None,

        distance_threshold=(

            1 -
            TOPIC_SIMILARITY_THRESHOLD
        ),

        metric="euclidean",

        linkage="ward"
    )

    labels = clustering.fit_predict(
        embeddings
    )

    clustered_topics = {}

    for idx, label in enumerate(labels):

        topic = topics[idx]

        if label not in clustered_topics:

            clustered_topics[
                label
            ] = []

        clustered_topics[
            label
        ].append(topic)

    final_topics = []

    for cluster in (
        clustered_topics.values()
    ):

        representative = min(
            cluster,
            key=len
        )

        final_topics.append(
            representative
        )

    return final_topics


# =====================================
# RANK TOPICS
# =====================================

def rank_topics(
    topics,
    meeting_embedding
):

    scored_topics = []

    for topic in topics:

        topic_embedding = (
            generate_sentence_embedding(
                topic
            )
        )

        score = (
            calculate_semantic_similarity(

                topic_embedding,

                meeting_embedding
            )
        )

        scored_topics.append({

            "topic":
                topic.title(),

            "relevance_score":
                round(score, 2)
        })

    scored_topics.sort(

        key=lambda x: x[
            "relevance_score"
        ],

        reverse=True
    )

    return scored_topics[:MAX_TOPICS]


# =====================================
# MAIN TOPIC DETECTION
# =====================================

def detect_meeting_topics(transcript):

    candidate_topics = (
        extract_candidate_topics(
            transcript
        )
    )

    embeddings = (
        generate_topic_embeddings(
            candidate_topics
        )
    )

    clustered_topics = cluster_topics(

        candidate_topics,

        embeddings
    )

    meeting_embedding = (
        generate_meeting_embedding(
            transcript
        )
    )

    ranked_topics = rank_topics(

        clustered_topics,

        meeting_embedding
    )

    final_topics = []

    for topic in ranked_topics:

        if topic[
            "relevance_score"
        ] >= 0.30:

            final_topics.append(
                topic
            )

    final_topics = semantic_deduplicate(

        final_topics,

        "topic"
    )

    return {

        "topics":
            final_topics,

        "meeting_embedding":
            meeting_embedding
    }