from rag_utils import (
    ARTIFACT_QUERIES,
    answer_museum_question,
    calculate_confidence,
    get_artifact_query,
    retrieve_evidence,
)


def test_artifact_query_maps_to_specific_search_terms():
    query = get_artifact_query("Backwards Hint Machine")

    assert query != "Backwards Hint Machine"
    assert "hint" in query
    assert "higher" in query
    assert "lower" in query


def test_unknown_artifact_uses_name_as_query():
    assert get_artifact_query("Mystery Exhibit") == "Mystery Exhibit"


def test_retrieve_evidence_finds_relevant_chunk():
    chunks = [
        {
            "source": "reflection.md",
            "text": "The secret number kept changing because Streamlit reran the script.",
        },
        {
            "source": "logic_utils.py",
            "text": "The scoring function deducts points for wrong guesses.",
        },
    ]

    evidence = retrieve_evidence("secret number changing Streamlit", chunks)

    assert evidence
    assert evidence[0]["source"] == "reflection.md"


def test_empty_question_returns_not_enough_evidence():
    answer, evidence, confidence, confidence_label = answer_museum_question("", chunks=[])

    assert evidence == []
    assert confidence == 0.0
    assert confidence_label == "Not enough evidence"
    assert "could not find enough project evidence" in answer


def test_unrelated_question_returns_not_enough_evidence():
    chunks = [
        {
            "source": "README.md",
            "text": "The hint bug made low guesses point in the wrong direction.",
        }
    ]

    answer, evidence, confidence, confidence_label = answer_museum_question(
        "explain database migrations and cloud billing",
        chunks=chunks,
    )

    assert evidence == []
    assert confidence == 0.0
    assert confidence_label == "Not enough evidence"
    assert "could not find enough project evidence" in answer


def test_museum_answer_uses_retrieved_project_evidence():
    chunks = [
        {
            "source": "tests/test_game_logic.py",
            "text": "test_hint_too_low_tells_player_to_go_higher checks that LOW guesses say HIGHER.",
        }
    ]

    answer, evidence, confidence, confidence_label = answer_museum_question(
        ARTIFACT_QUERIES["Backwards Hint Machine"],
        chunks=chunks,
    )

    assert evidence
    assert confidence > 0.0
    assert confidence_label in ("Low", "Medium", "High")
    assert "Retrieved evidence from: tests/test_game_logic.py" in answer
    assert "hint bug" in answer


def test_stronger_evidence_has_higher_confidence():
    weak_evidence = [
        {
            "source": "README.md",
            "text": "hint",
            "score": 3,
            "matched_terms": ["hint"],
        }
    ]
    strong_evidence = [
        {
            "source": "README.md",
            "text": "hint too low higher too high lower check_guess",
            "score": 12,
            "matched_terms": ["hint", "higher", "lower"],
        },
        {
            "source": "tests/test_game_logic.py",
            "text": "test_hint_too_low_tells_player_to_go_higher",
            "score": 9,
            "matched_terms": ["hint", "higher"],
        },
    ]

    weak_confidence, _ = calculate_confidence(weak_evidence)
    strong_confidence, _ = calculate_confidence(strong_evidence)

    assert strong_confidence > weak_confidence


def test_confidence_never_exceeds_one():
    evidence = [
        {
            "source": "README.md",
            "text": "lots of strong evidence",
            "score": 100,
            "matched_terms": ["strong"],
        },
        {
            "source": "reflection.md",
            "text": "more strong evidence",
            "score": 100,
            "matched_terms": ["strong"],
        },
        {
            "source": "tests/test_game_logic.py",
            "text": "even more strong evidence",
            "score": 100,
            "matched_terms": ["strong"],
        },
    ]

    confidence, label = calculate_confidence(evidence)

    assert confidence == 1.0
    assert label == "High"
