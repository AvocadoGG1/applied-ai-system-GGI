# Model Card: Glitch Museum Mode RAG Guide

## System Overview

**Project:** Game Glitch Investigator: Glitch Museum Mode

This system adds a lightweight Retrieval-Augmented Generation (RAG) feature to a fixed Streamlit number guessing game. The RAG guide acts like a museum docent for old bugs: users select a bug artifact or ask a question, and the system searches project files before generating an evidence-based explanation.

The base project was **Game Glitch Investigator: The Impossible Guesser**, a debugging project where I fixed an AI-generated guessing game. The original game had logic and state bugs, including a changing secret number, backwards hints, broken reset behavior, invalid guess handling, and inconsistent scoring.

## Intended Use

The system is intended for educational debugging reflection. It helps users understand:

- what bugs existed in the original AI-generated game,
- why those bugs happened,
- how they were fixed,
- which tests prove the fixes work.

It is not intended to be a general programming assistant or a replacement for reading the actual code and tests.

## AI Feature

The AI feature is a local RAG-style guide implemented in `rag_utils.py`.

The guide retrieves evidence from:

- `README.md`
- `reflection.md`
- `app.py`
- `logic_utils.py`
- `tests/test_game_logic.py`

It then generates a project-specific explanation and displays:

- the answer,
- retrieved evidence snippets,
- a confidence score from `0.00` to `1.00`,
- a confidence label such as `High`, `Medium`, `Low`, or `Not enough evidence`.

## Testing and Reliability Results

The project uses automated tests to prove that the system works.

Current result: **26 out of 26 tests passed**.

The tests cover:

- core game logic,
- input validation,
- difficulty ranges,
- scoring behavior,
- artifact-to-query mapping,
- evidence retrieval,
- fallback behavior for missing context,
- confidence scoring.

The most important reliability behavior is that unrelated questions receive `0.00` confidence and a fallback response instead of a fake answer. For example, if the user asks about database migrations or cloud billing, the guide says it cannot find enough project evidence.

## Limitations and Biases

The system is limited by its small knowledge base. It can only explain information that appears in the included project files, so it may miss an answer if the evidence was never documented.

The retriever uses keyword matching instead of embeddings, so it may struggle when a user asks a valid question using very different wording. This creates a bias toward exact project vocabulary like "secret number," "hints," "score," "pytest," and "session_state."

The confidence score is also limited. It measures retrieval strength and source diversity, not absolute truth. A high confidence score means the system found strong matching evidence, not that the answer is guaranteed to be correct.

## Misuse Risks and Mitigations

The system could be misused if someone treats it like a general-purpose coding expert. It is only designed to explain this specific project.

Mitigations:

- The guide shows retrieved evidence snippets so users can inspect the source.
- It gives `0.00` confidence when no useful evidence is found.
- It returns a "not enough evidence" fallback instead of inventing unsupported answers.
- The knowledge base is limited to approved local project files.

## Human Evaluation

Human review is still part of the system. I manually check whether the guide's explanation is supported by the retrieved snippets and whether the confidence score feels reasonable.

During testing, the most useful discovery was that failure cases matter. The unrelated-question test showed that a responsible AI system should sometimes refuse to answer instead of stretching weak evidence into a confident response.

## AI Collaboration Reflection

AI was useful as a debugging and design teammate. One helpful suggestion was to move reusable game logic into `logic_utils.py`, which made it much easier to test functions like `check_guess`, `parse_guess`, and `update_score` without launching Streamlit.

One flawed suggestion was an early validation fix that only rejected negative numbers. It did not reject guesses outside the selected difficulty range. Testing and manual review exposed that gap, so I added full range validation based on the difficulty's low and high values.

This project taught me that AI-generated code can look convincing while still being wrong. My job as an AI engineer is to verify behavior, add guardrails, and make the system honest about what it knows.
