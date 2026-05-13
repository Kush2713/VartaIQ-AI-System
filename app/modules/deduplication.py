from sklearn.metrics.pairwise import cosine_similarity

from app.modules.context_engine import (
    generate_sentence_embedding
)

from app.config.ai_config import (
    DEDUPLICATION_THRESHOLD
)


# =====================================
# SEMANTIC DEDUPLICATION
# =====================================

def semantic_deduplicate(
    items,
    text_key
):
    """
    Removes semantically duplicate items
    using embedding similarity.
    """

    # ---------------------------------
    # Empty safety
    # ---------------------------------

    if not items:
        return []

    unique_items = []

    embeddings = []

    # ---------------------------------
    # Iterate through items
    # ---------------------------------

    for item in items:

        # Safety check
        if text_key not in item:
            continue

        text = item[text_key]

        # Skip empty text
        if not text:
            continue

        # Generate embedding
        current_embedding = (
            generate_sentence_embedding(
                text
            )
        )

        duplicate_found = False

        # ---------------------------------
        # Compare with existing embeddings
        # ---------------------------------

        for existing_embedding in embeddings:

            similarity = cosine_similarity(

                [current_embedding],

                [existing_embedding]

            )[0][0]

            # Semantic duplicate detected
            if similarity >= (
                DEDUPLICATION_THRESHOLD
            ):

                duplicate_found = True

                break

        # ---------------------------------
        # Keep only unique semantic items
        # ---------------------------------

        if not duplicate_found:

            unique_items.append(item)

            embeddings.append(
                current_embedding
            )

    return unique_items