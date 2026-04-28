import re
from pathlib import Path


ARTIFACT_QUERIES = {
    "Shapeshifting Secret Number": (
        "secret number kept changing Streamlit rerun session_state random randint"
    ),
    "Backwards Hint Machine": (
        "hints backwards too low go higher too high go lower check_guess"
    ),
    "Haunted New Game Button": (
        "new game button reset attempts status score history"
    ),
    "Out-of-Range Guess Portal": (
        "out of range guess difficulty range validation parse_guess"
    ),
    "Suspicious Scorekeeper": (
        "score logic wrong guess parity bonus update_score"
    ),
    "Pytest Evidence Wall": (
        "pytest tests prove bug fixed test_game_logic"
    ),
}

KNOWLEDGE_FILES = (
    "README.md",
    "reflection.md",
    "logic_utils.py",
    "app.py",
    "tests/test_game_logic.py",
)

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "how",
    "i",
    "in",
    "is",
    "it",
    "of",
    "or",
    "the",
    "to",
    "was",
    "what",
    "when",
    "which",
    "why",
    "with",
}


def get_artifact_query(artifact_name: str) -> str:
    """Return the retrieval query for a museum artifact."""
    return ARTIFACT_QUERIES.get(artifact_name, artifact_name)


def tokenize(text: str) -> list[str]:
    """Lowercase text into searchable words."""
    return [
        word
        for word in re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", text.lower())
        if word not in STOPWORDS and len(word) > 1
    ]


def chunk_text(text: str, source: str, max_words: int = 90) -> list[dict[str, str]]:
    """Split a file into small evidence chunks."""
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
    chunks = []

    for paragraph in paragraphs:
        words = paragraph.split()
        for start in range(0, len(words), max_words):
            chunk_words = words[start : start + max_words]
            if chunk_words:
                chunks.append(
                    {
                        "source": source,
                        "text": " ".join(chunk_words),
                    }
                )

    return chunks


def load_knowledge_base(base_path: str | Path = ".") -> list[dict[str, str]]:
    """Load project files used by Glitch Museum Mode."""
    root = Path(base_path)
    chunks = []

    for relative_path in KNOWLEDGE_FILES:
        path = root / relative_path
        if path.exists():
            text = path.read_text(encoding="utf-8", errors="ignore")
            chunks.extend(chunk_text(text, relative_path))

    return chunks


def retrieve_evidence(
    query: str,
    chunks: list[dict[str, str]],
    top_k: int = 3,
    min_score: int = 2,
) -> list[dict[str, object]]:
    """Return the most relevant evidence chunks for a query."""
    query_terms = tokenize(query)
    if not query_terms:
        return []

    query_set = set(query_terms)
    scored = []

    for chunk in chunks:
        text_terms = tokenize(chunk["text"])
        text_set = set(text_terms)
        overlap = query_set & text_set
        score = len(overlap)

        for term in query_terms:
            if term in chunk["text"].lower():
                score += 1

        if score >= min_score:
            scored.append(
                {
                    "source": chunk["source"],
                    "text": chunk["text"],
                    "score": score,
                    "matched_terms": sorted(overlap),
                }
            )

    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored[:top_k]


def calculate_confidence(evidence: list[dict[str, object]]) -> tuple[float, str]:
    """Estimate confidence from evidence strength and source diversity."""
    if not evidence:
        return 0.0, "Not enough evidence"

    total_score = sum(int(item.get("score", 0)) for item in evidence)
    source_count = len({str(item.get("source", "")) for item in evidence})

    score_confidence = min(total_score / 30, 0.85)
    source_bonus = min(source_count * 0.05, 0.15)
    confidence = min(score_confidence + source_bonus, 1.0)
    confidence = round(confidence, 2)

    if confidence >= 0.75:
        label = "High"
    elif confidence >= 0.4:
        label = "Medium"
    else:
        label = "Low"

    return confidence, label


def generate_museum_answer(question: str, evidence: list[dict[str, object]]) -> str:
    """Create a project-specific museum guide answer from retrieved evidence."""
    if not evidence:
        return (
            "I could not find enough project evidence for that exhibit. "
            "Try asking about the secret number, hints, new game reset, "
            "range validation, scoring, or pytest evidence."
        )

    sources = ", ".join(dict.fromkeys(str(item["source"]) for item in evidence))
    evidence_points = []
    for item in evidence:
        text = str(item["text"]).strip()
        if len(text) > 260:
            text = text[:257].rstrip() + "..."
        evidence_points.append(f"- {item['source']}: {text}")

    lower_question = question.lower()
    if "secret" in lower_question or "session" in lower_question:
        focus = (
            "This artifact shows the old state bug: Streamlit reruns the script, "
            "so the secret number had to live in session state instead of being "
            "generated fresh every interaction."
        )
    elif "hint" in lower_question or "higher" in lower_question or "lower" in lower_question:
        focus = (
            "This artifact shows the hint bug: the comparison result and the player "
            "message had to agree, so low guesses point higher and high guesses point lower."
        )
    elif "new game" in lower_question or "reset" in lower_question:
        focus = (
            "This artifact shows the reset bug: starting over must clear the whole game "
            "state, not just pick a new secret."
        )
    elif "range" in lower_question or "difficulty" in lower_question:
        focus = (
            "This artifact shows the validation bug: each difficulty has its own allowed "
            "range, and guesses plus generated secrets must stay inside that range."
        )
    elif "score" in lower_question:
        focus = (
            "This artifact shows the scoring bug: wrong guesses should be punished "
            "consistently, while wins should earn points based on attempts used."
        )
    elif "test" in lower_question or "pytest" in lower_question:
        focus = (
            "This artifact shows the evidence wall: tests turn each bug fix into a "
            "repeatable check instead of a one-time manual guess."
        )
    else:
        focus = (
            "This exhibit connects your question to the project's debugging notes, "
            "fixed code, and tests."
        )

    return (
        f"{focus}\n\n"
        f"Retrieved evidence from: {sources}\n\n"
        "Evidence used by the museum guide:\n"
        + "\n".join(evidence_points)
    )


def answer_museum_question(
    question: str,
    base_path: str | Path = ".",
    chunks: list[dict[str, str]] | None = None,
) -> tuple[str, list[dict[str, object]], float, str]:
    """Retrieve evidence and generate an answer for Glitch Museum Mode."""
    if not question or not question.strip():
        return generate_museum_answer("", []), [], 0.0, "Not enough evidence"

    knowledge_chunks = chunks if chunks is not None else load_knowledge_base(base_path)
    evidence = retrieve_evidence(question, knowledge_chunks)
    confidence, confidence_label = calculate_confidence(evidence)
    return generate_museum_answer(question, evidence), evidence, confidence, confidence_label
