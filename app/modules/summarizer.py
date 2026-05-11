# from app.services.model_loader import get_summarizer

# def summarize(texts):

#     summarizer = get_summarizer()

#     full_text = " ".join(texts)

#     max_len = max(30, int(len(full_text.split()) * 0.6))
#     min_len = max(15, int(len(full_text.split()) * 0.3))

#     result = summarizer(
#         full_text,
#         max_length=max_len,
#         min_length=min_len,
#         do_sample=False
#     )

#     return result[0]["summary_text"]

from app.services.model_loader import get_summarizer


MAX_CHUNK_WORDS = 400


def create_chunks(text, chunk_size=MAX_CHUNK_WORDS):
    """
    Splits long meeting text into manageable chunks.
    """

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def format_transcript(data):
    """
    Preserves speaker structure for better meeting summarization.
    """

    formatted_lines = []

    for item in data:
        speaker = item["speaker"]
        text = item["text"]

        formatted_lines.append(f"{speaker}: {text}")

    return "\n".join(formatted_lines)


def summarize(data):

    summarizer = get_summarizer()

    # Speaker-aware transcript formatting
    formatted_text = format_transcript(data)

    # Split into chunks for long meetings
    chunks = create_chunks(formatted_text)

    partial_summaries = []

    for chunk in chunks:

        word_count = len(chunk.split())

        max_len = min(120, max(40, int(word_count * 0.5)))
        min_len = min(60, max(20, int(word_count * 0.25)))

        result = summarizer(
            chunk,
            max_length=max_len,
            min_length=min_len,
            do_sample=False
        )

        partial_summaries.append(result[0]["summary_text"])

    # Combine chunk summaries
    final_summary = " ".join(partial_summaries)

    return final_summary
