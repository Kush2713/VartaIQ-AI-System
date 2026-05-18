
from app.modules.context_builder import (
    build_ai_context
)

from app.modules.transcript_preprocessor import (
    preprocess_transcript
)

from app.modules.summarizer import (
    summarize
)

from app.modules.action_items import (
    extract_action_items
)

from app.modules.useless_talk import (
    detect_useless_talk
)

from app.modules.speaker_analysis import (
    analyze_speakers
)

from app.modules.scoring import (
    calculate_score
)

from app.modules.decisions import (
    extract_decisions
)

from app.modules.sentiment_analysis import (
    analyze_sentiment
)

from app.modules.followup_generator import (
    generate_followups
)

from app.modules.llm_enhancer import (

    refine_summary,

    generate_meeting_insights
)

from app.modules.validators import (

    validate_action_items,

    validate_decisions,

    validate_topics,

    validate_useless_talk
)

from app.modules.response_formatter import (

    format_summary,

    format_topics,

    format_action_items,

    format_decisions,

    format_useless_talk,

    format_followups,

    format_ai_insights,

    format_speaker_analysis,

    format_sentiment_analysis,

    format_score
)


# =====================================
# SAFE MODULE EXECUTION
# =====================================

from app.core.logger import get_logger

logger = get_logger(__name__)


def safe_execute(
    func,
    default_value,
    *args,
    **kwargs
):

    try:
        return func(*args, **kwargs)

    except Exception as e:

        logger.error(
            f"Module '{func.__name__}' failed: {str(e)}",
            exc_info=True   # This automatically includes the full stack trace
        )

        return default_value


# =====================================
# MAIN AI PIPELINE
# =====================================

def run_pipeline(data):

    # =================================
    # PREPROCESS TRANSCRIPT
    # =================================

    transcript = safe_execute(

        preprocess_transcript,

        data,

        data
    )

    # =================================
    # SHARED AI CONTEXT
    # =================================

    context = build_ai_context(
        transcript
    )

    # =================================
    # TOPICS
    # =================================

    raw_topics = context["topics"]

    validated_topics = safe_execute(

        validate_topics,

        [],

        raw_topics
    )

    topics = safe_execute(

        format_topics,

        [],

        validated_topics
    )

    # =================================
    # SUMMARY
    # =================================

    raw_summary = safe_execute(

        summarize,

        "Summary generation failed.",

        transcript
    )

    refined_summary = safe_execute(

        refine_summary,

        raw_summary,

        raw_summary
    )

    final_summary = safe_execute(

        format_summary,

        refined_summary,

        refined_summary
    )

    # =================================
    # ACTION ITEMS
    # =================================

    raw_actions = safe_execute(

        extract_action_items,

        [],

        transcript
    )

    validated_actions = safe_execute(

        validate_action_items,

        [],

        raw_actions
    )

    action_items = safe_execute(

        format_action_items,

        [],

        validated_actions
    )

    # =================================
    # DECISIONS
    # =================================

    raw_decisions = safe_execute(

        extract_decisions,

        [],

        transcript
    )

    validated_decisions = safe_execute(

        validate_decisions,

        [],

        raw_decisions
    )

    decisions = safe_execute(

        format_decisions,

        [],

        validated_decisions
    )

        # =================================
    # USELESS TALK
    # =================================

    raw_useless_talk = safe_execute(

        detect_useless_talk,

        {
            "useless_segments": []
        },

        transcript,

        context
    )

    validated_useless_talk = safe_execute(

        validate_useless_talk,

        {
            "useless_segments": []
        },

        raw_useless_talk
    )

    useless_talk = safe_execute(

        format_useless_talk,

        {
            "useless_segments": []
        },

        validated_useless_talk
    )

    # =================================
    # SPEAKER ANALYSIS
    # =================================

    raw_speaker_analysis = safe_execute(

        analyze_speakers,

        {},

        transcript,

        context
    )

    speaker_analysis = safe_execute(

        format_speaker_analysis,

        {},

        raw_speaker_analysis
    )

    # =================================
    # SENTIMENT ANALYSIS
    # =================================

    raw_sentiment_analysis = safe_execute(

        analyze_sentiment,

        {},

        transcript,

        context
    )

    sentiment_analysis = safe_execute(

        format_sentiment_analysis,

        {},

        raw_sentiment_analysis
    )

    # =================================
    # MEETING SCORE
    # =================================

    raw_score = safe_execute(

        calculate_score,

        {
            "final_score": 0,
            "rating": "Unavailable",
            "breakdown": {}
        },

        transcript,

        final_summary,

        action_items,

        useless_talk,

        speaker_analysis,

        decisions
    )

    score = safe_execute(

        format_score,

        {
            "final_score": 0,
            "rating": "Unavailable",
            "breakdown": {}
        },

        raw_score
    )

    # =================================
    # FOLLOWUPS
    # =================================

    raw_followups = safe_execute(

        generate_followups,

        [],

        final_summary,

        action_items,

        decisions,

        sentiment_analysis,

        score["final_score"]
    )

    followups = safe_execute(

        format_followups,

        [],

        raw_followups
    )

    # =================================
    # AI INSIGHTS
    # =================================

    raw_insights = safe_execute(

        generate_meeting_insights,

        [],

        final_summary,

        score,

        speaker_analysis,

        sentiment_analysis,

        topics
    )

    insights = safe_execute(

        format_ai_insights,

        [],

        raw_insights
    )

    # =================================
    # FINAL RESPONSE
    # =================================

    return {

        "summary":
            final_summary,

        "topics":
            topics,

        "action_items":
            action_items,

        "decisions":
            decisions,

        "useless_talk":
            useless_talk,

        "speaker_analysis":
            speaker_analysis,

        "sentiment_analysis":
            sentiment_analysis,

        "score":
            score,

        "followups":
            followups,

        "ai_insights":
            insights
    }














# from app.modules.summarizer import (
#     summarize
# )

# from app.modules.action_items import (
#     extract_action_items
# )

# from app.modules.useless_talk import (
#     detect_useless_talk
# )

# from app.modules.speaker_analysis import (
#     analyze_speakers
# )

# from app.modules.scoring import (
#     calculate_score
# )

# from app.modules.decisions import (
#     extract_decisions
# )

# from app.modules.topic_detection import (
#     detect_meeting_topics
# )

# from app.modules.llm_enhancer import (

#     refine_summary,

#     validate_action_items,

#     validate_decisions,

#     generate_meeting_insights
# )

# from app.modules.sentiment_analysis import (
#     analyze_sentiment
# )

# from app.modules.followup_generator import (
#     generate_followups
# )


# # =====================================
# # MAIN AI PIPELINE
# # =====================================

# def run_pipeline(data):

#     transcript = data

#     # ---------------------------------
#     # 1. SHARED SEMANTIC CONTEXT
#     # ---------------------------------

#     semantic_context = detect_meeting_topics(
#         transcript
#     )

#     topics = semantic_context["topics"]

#     # ---------------------------------
#     # 2. Generate Summary
#     # ---------------------------------

#     raw_summary = summarize(
#         transcript
#     )

#     refined_summary = refine_summary(
#         raw_summary
#     )

#     # ---------------------------------
#     # 3. Action Items
#     # ---------------------------------

#     raw_actions = extract_action_items(
#         transcript
#     )

#     action_items = validate_action_items(
#         raw_actions
#     )

#     # ---------------------------------
#     # 4. Decisions
#     # ---------------------------------

#     raw_decisions = extract_decisions(
#         transcript
#     )

#     decisions = validate_decisions(
#         raw_decisions
#     )

#     # ---------------------------------
#     # 5. Useless Talk
#     # ---------------------------------

#     useless_talk = detect_useless_talk(

#         transcript,

#         semantic_context
#     )

#     # ---------------------------------
#     # 6. Speaker Intelligence
#     # ---------------------------------

#     speaker_analysis = analyze_speakers(

#         transcript,

#         semantic_context
#     )
#     # ---------------------------------
#     # 7. Sentiment Intelligence
#     # ---------------------------------

#     sentiment_analysis = (
#         analyze_sentiment(
#             transcript
#         )
#     )

#     # ---------------------------------
#     # 8. Meeting Score
#     # ---------------------------------

#     score = calculate_score(

#         transcript,

#         refined_summary,

#         action_items,

#         useless_talk,

#         speaker_analysis,

#         decisions
#     )
    
#         # ---------------------------------
#     # 9. AI Follow-up Intelligence
#     # ---------------------------------

#     followups = generate_followups(

#         refined_summary,

#         action_items,

#         decisions,

#         score["final_score"]
#     )

#     # ---------------------------------
#     # 10. AI Insights
#     # ---------------------------------

#     insights = generate_meeting_insights(

#         refined_summary,

#         score["final_score"]
#     )

#     # ---------------------------------
#     # FINAL RESPONSE
#     # ---------------------------------

#     return {

#         "summary":
#             refined_summary,

#         "topics":
#             topics,

#         "action_items":
#             action_items,

#         "decisions":
#             decisions,

#         "useless_talk":
#             useless_talk,

#         "speaker_analysis":
#             speaker_analysis,
            
#         "sentiment_analysis":
#             sentiment_analysis,

#         "score":
#             score,
            
#         "followups":
#         followups,

#         "ai_insights":
#             insights
#     }

































# from app.modules.summarizer import summarize
# from app.modules.action_items import extract_action_items
# from app.modules.useless_talk import detect_useless_talk
# from app.modules.speaker_analysis import analyze_speakers
# from app.modules.scoring import calculate_score
# from app.modules.decisions import extract_decisions


# def run_pipeline(data):

#     transcript = data

#     # -------------------------
#     # 1. Meeting Summary
#     # -------------------------

#     summary = summarize(transcript)

#     # -------------------------
#     # 2. Action Items
#     # -------------------------

#     action_items = extract_action_items(
#         transcript
#     )

#     # -------------------------
#     # 3. Useless Talk + Topics
#     # -------------------------

#     useless_data = detect_useless_talk(
#         transcript
#     )

#     detected_topics = useless_data[
#         "detected_topics"
#     ]

#     useless_segments = useless_data[
#         "useless_segments"
#     ]

#     # -------------------------
#     # 4. Speaker Analysis
#     # -------------------------

#     speaker_analysis = analyze_speakers(
#         transcript
#     )

#     # -------------------------
#     # 5. Decisions
#     # -------------------------

#     decisions = extract_decisions(
#         transcript
#     )

#     # -------------------------
#     # 6. Meeting Scoring
#     # -------------------------

#     score = calculate_score(
#         transcript,
#         summary,
#         action_items,
#         useless_segments,
#         speaker_analysis,
#         decisions
#     )

#     # -------------------------
#     # Final Response
#     # -------------------------

#     return {
#         "summary": summary,

#         "topics": detected_topics,

#         "action_items": action_items,

#         "decisions": decisions,

#         "useless_talk": useless_segments,

#         "speaker_analysis": speaker_analysis,

#         "score": score
#     }























































# # from app.modules.summarizer import summarize
# # from app.modules.action_items import extract_action_items
# # from app.modules.useless_talk import detect_useless_talk
# # from app.modules.speaker_analysis import analyze_speakers
# # from app.modules.scoring import calculate_score
# # from app.modules.decisions import extract_decisions


# # def run_pipeline(data):
# #     transcript = data

# #     # Summary
# #     summary = summarize(transcript)

# #     # Action items
# #     action_items = extract_action_items(transcript)

# #     # Useless talk
# #     useless = detect_useless_talk(transcript)

# #     # Speaker analysis
# #     speaker_analysis = analyze_speakers(transcript)

# #     # Decisions
# #     decisions = extract_decisions(transcript)

# #     # Score
# #     score = calculate_score(
# #     transcript,
# #     summary,
# #     action_items,
# #     useless,
# #     speaker_analysis,
# #     decisions
# # )

# #     return {
# #         "summary": summary,
# #         "action_items": action_items,
# #         "decisions": decisions,
# #         "useless_talk": useless,
# #         "speaker_analysis": speaker_analysis,
# #         "score": score
# #     }