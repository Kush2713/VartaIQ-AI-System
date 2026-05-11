from app.modules.summarizer import summarize
from app.modules.action_items import extract_action_items
from app.modules.useless_talk import detect_useless_talk
from app.modules.speaker_analysis import analyze_speakers
from app.modules.scoring import calculate_score
from app.modules.decisions import extract_decisions


def run_pipeline(data):
    transcript = data

    # Summary
    summary = summarize(transcript)

    # Action items
    action_items = extract_action_items(transcript)

    # Useless talk
    useless = detect_useless_talk(transcript)

    # Speaker analysis
    speaker_analysis = analyze_speakers(transcript)

    # Decisions
    decisions = extract_decisions(transcript)

    # Score
    score = calculate_score(
    transcript,
    summary,
    action_items,
    useless,
    speaker_analysis,
    decisions
)

    return {
        "summary": summary,
        "action_items": action_items,
        "decisions": decisions,
        "useless_talk": useless,
        "speaker_analysis": speaker_analysis,
        "score": score
    }