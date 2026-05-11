from collections import defaultdict


def analyze_speakers(data):

    word_count = defaultdict(int)

    for item in data:
        word_count[item["speaker"]] += len(
            item["text"].split()
        )

    total = sum(word_count.values())

    if total == 0:
        return {}

    result = {}

    for speaker, count in word_count.items():

        result[speaker] = {
            "word_count": count,
            "percentage": round(
                (count / total) * 100,
                2
            )
        }

    return result
