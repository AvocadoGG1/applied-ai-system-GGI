# 5-7 Minute Presentation Plan

## Goal

Show **Game Glitch Investigator: Glitch Museum Mode** running end-to-end, demonstrate the RAG feature, show reliability behavior, and explain what I learned.

## Suggested Timing

### 0:00-0:45 - Project Intro

"My project is called **Game Glitch Investigator: Glitch Museum Mode**. It started as a Streamlit number guessing game with AI-generated bugs. I fixed the game logic, added tests, and then added a RAG-powered museum guide that explains the old bugs using evidence from the project files."

Mention:

- Original project: **Game Glitch Investigator: The Impossible Guesser**
- AI feature: RAG-powered museum guide
- Reliability feature: automated tests plus confidence scoring

### 0:45-1:30 - Original Game Demo

Show the running Streamlit app.

Say:

"The game now works as a playable number guessing game. The player picks a difficulty, guesses a number, and gets higher/lower feedback. The original version had bugs like changing the secret number, backwards hints, invalid guesses, and broken reset behavior."

Demo briefly:

- Pick a difficulty.
- Enter one valid guess.
- Show that the game gives feedback.
- Mention that the debug panel shows state for development/testing.

### 1:30-3:30 - RAG Feature Demo: 2-3 Inputs

Scroll to **Glitch Museum Mode**.

#### Input 1

Select: `Shapeshifting Secret Number`

Click: **Inspect Artifact**

Say:

"This demonstrates the RAG feature. The app turns the artifact into a retrieval query, searches project files like `README.md`, `reflection.md`, `app.py`, and tests, then generates an explanation using the retrieved evidence."

Point out:

- The explanation
- The confidence score
- The retrieved case-file evidence

#### Input 2

Ask: `Which test proves the hints were fixed?`

Click: **Ask Custom Question**

Say:

"This shows that the guide can answer a custom question, not just a preset artifact. It retrieves evidence from the test file and explains which tests prove the higher/lower hint logic works."

Point out:

- Evidence from `tests/test_game_logic.py`
- Confidence score
- Project-specific answer

#### Input 3

Ask: `Explain database migrations and cloud billing`

Click: **Ask Custom Question**

Say:

"This is the reliability guardrail. The question is unrelated to the project, so the system should not pretend it knows the answer. It returns a low confidence score and a 'not enough evidence' fallback."

Point out:

- Confidence: `Not enough evidence (0.00)`
- Fallback response

### 3:30-4:30 - Architecture

Show the Mermaid diagram in the README.

Say:

"The architecture is simple and local. The user asks a question in Streamlit. The app sends it to `rag_utils.py`, which searches a small project knowledge base. The guide response is generated from retrieved evidence, and the output appears in the app with a confidence score."

Mention:

- `app.py` = Streamlit interface
- `rag_utils.py` = retriever, answer generator, confidence scoring
- Project files = knowledge base
- `pytest` = reliability checks

### 4:30-5:45 - Reliability and Testing

Show terminal test result if available, or README testing summary.

Say:

"The system proves reliability in two ways. First, automated tests check both the original game logic and the RAG helper functions. Second, the RAG guide displays confidence scores based on retrieval strength, and it refuses unrelated questions instead of making up an answer."

Mention:

- `26 out of 26 automated tests passed`
- Empty/unrelated questions return fallback
- Confidence scoring is based on retrieved evidence strength and source diversity

### 5:45-6:45 - Reflection

Say:

"This project taught me that AI-generated code can run and still be wrong. The biggest lesson was that responsible AI needs evidence, tests, and guardrails. I also learned how to work with AI as a teammate: it was helpful for refactoring and test ideas, but I still had to verify its suggestions because one early validation fix only rejected negative numbers and missed out-of-range guesses."

End with:

"What this project says about me as an AI engineer is that I care about building AI systems that are useful, testable, and honest about their limits."

## Loom Recording Checklist

The video should clearly show:

- End-to-end system run with 2-3 inputs.
- RAG behavior using preset artifact and custom question.
- Reliability behavior using confidence scoring and unrelated-question fallback.
- Clear outputs for each case.

The video does not need to show:

- Code installation.
- File setup.
- Full code walkthrough.


