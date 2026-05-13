import spacy
import numpy as np

from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity

from app.modules.context_engine import (

    embedding_model,

    generate_sentence_embedding,

    generate_meeting_embedding,

    calculate_semantic_similarity
)

from app.modules.deduplication import (
    semantic_deduplicate
)

nlp = spacy.load("en_core_web_sm")


# =====================================
# CONFIGURATION
# =====================================

from app.config.ai_config import (

    MIN_TOPIC_LENGTH,

    MAX_TOPICS,

    TOPIC_SIMILARITY_THRESHOLD
)


# =====================================
# EXTRACT CANDIDATE PHRASES
# =====================================

def extract_candidate_topics(transcript):

    phrases = []

    for item in transcript:

        doc = nlp(item["text"])

        # Extract noun phrases
        for chunk in doc.noun_chunks:

            phrase = chunk.text.strip().lower()

            # Remove very short phrases
            if len(phrase) < MIN_TOPIC_LENGTH:
                continue

            # Remove pronouns
            if phrase in {
                "i",
                "we",
                "it",
                "this",
                "that",
                "they"
            }:
                continue

            phrases.append(phrase)

    return list(set(phrases))


# =====================================
# GENERATE EMBEDDINGS
# =====================================

def generate_topic_embeddings(topics):

    if not topics:
        return []

    embeddings = embedding_model.encode(
        topics
    )

    return embeddings


# =====================================
# CLUSTER SIMILAR TOPICS
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
            1 - TOPIC_SIMILARITY_THRESHOLD
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
            clustered_topics[label] = []

        clustered_topics[label].append(
            topic
        )

    final_topics = []

    for cluster in clustered_topics.values():

        # Pick shortest representative phrase
        representative = min(
            cluster,
            key=len
        )

        final_topics.append(
            representative
        )

    return final_topics


# =====================================
# SCORE TOPICS BY MEETING RELEVANCE
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

        score = calculate_semantic_similarity(

            topic_embedding,

            meeting_embedding
        )

        scored_topics.append(
            (topic, score)
        )

    scored_topics.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return scored_topics[:MAX_TOPICS]


# =====================================
# MAIN TOPIC DETECTION
# =====================================

def detect_meeting_topics(transcript):

    # ---------------------------------
    # Step 1 - Extract candidate topics
    # ---------------------------------

    candidate_topics = (
        extract_candidate_topics(
            transcript
        )
    )

    # ---------------------------------
    # Step 2 - Generate embeddings
    # ---------------------------------

    embeddings = generate_topic_embeddings(
        candidate_topics
    )

    # ---------------------------------
    # Step 3 - Cluster semantic topics
    # ---------------------------------

    clustered_topics = cluster_topics(

        candidate_topics,

        embeddings
    )

    # ---------------------------------
    # Step 4 - Generate meeting context
    # ---------------------------------

    meeting_embedding = (
        generate_meeting_embedding(
            transcript
        )
    )

    # ---------------------------------
    # Step 5 - Rank topics
    # ---------------------------------

    ranked_topics = rank_topics(

        clustered_topics,

        meeting_embedding
    )

    # ---------------------------------
    # Step 6 - Build final topics
    # ---------------------------------

    final_topics = []

    for topic, score in ranked_topics:

        if score >= 0.30:

            final_topics.append({

                "topic":
                    topic,

                "relevance_score":
                    round(score, 2)
            })

    # ---------------------------------
    # Step 7 - Semantic deduplication
    # ---------------------------------

    final_topics = semantic_deduplicate(

        final_topics,

        "topic"
    )

    # ---------------------------------
    # Final output
    # ---------------------------------

    return {

        "topics":
            final_topics,

        "meeting_embedding":
            meeting_embedding
    }