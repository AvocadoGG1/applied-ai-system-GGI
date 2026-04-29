# Loom Walkthrough and Live Presentation Plan

This file separates the **required Loom video** from the shorter **live peer presentation**.

The Loom video is for graders and should prove every required feature. The live presentation can be shorter and focus on the most interesting parts.

Use these files for the live peer presentation:

- `presentation/glitch_museum_mode_peer_presentation.pptx`
- `presentation/glitch_museum_mode_peer_speaker_notes.md`

## Required Loom Checklist

Your Loom must clearly demonstrate:

- [ ] **End-to-end system run with 2-3 inputs**
- [ ] **AI feature behavior**, specifically RAG retrieval and evidence-grounded answers
- [ ] **Reliability, guardrail, or evaluation behavior**
- [ ] **Clear outputs for each case**

The video does **not** need to show code setup, file structure, or installation steps.

## Loom Recording Setup

Before recording:

1. Open the Streamlit app: `http://localhost:8502`
2. Open a terminal with the test result already visible:

```powershell
cd C:\Users\andre\PythonPrograms\applied-ai-system-final
py -m pytest -vv
```

3. Keep `README.md` open near the architecture diagram if you want to briefly show it.
4. Keep these three demo inputs ready:
   - `Shapeshifting Secret Number`
   - `Which test proves the hints were fixed?`
   - `Explain database migrations and cloud billing`

## Required Loom Script

### 0:00-0:30 - Quick Intro

Screen:

- Show the Streamlit app.
- Start near the top of the page.

Say:

"This project is **Game Glitch Investigator: Glitch Museum Mode**. It started as a broken AI-generated Streamlit guessing game. I fixed the game logic, added automated tests, and then added a RAG-powered museum guide that explains the old bugs using real evidence from the project files."

Requirement covered:

- Project context
- End-to-end app is running

### 0:30-1:15 - End-to-End App Run

Screen:

- Show the guessing game.
- Choose a difficulty if needed.
- Enter one normal guess.
- Click **Submit Guess**.
- Show the output/hint or game feedback.

Say:

"First, here is the base app running end-to-end. The user can choose a difficulty, enter a guess, and get game feedback. The original version had bugs like changing the secret number, backwards hints, invalid guesses, and broken reset behavior. Those have been fixed and tested."

Requirement covered:

- End-to-end system run
- Clear output from the base app

### 1:15-2:15 - Input 1: Preset RAG Artifact

Screen:

- Scroll to **Glitch Museum Mode**.
- Select `Shapeshifting Secret Number`.
- Click **Inspect Artifact**.
- Show the answer, confidence score, and retrieved evidence.

Say:

"This is the AI feature behavior. I selected the artifact **Shapeshifting Secret Number**. The app turns that artifact into a retrieval query, searches project files like `reflection.md` and `app.py`, and then generates an explanation using the retrieved evidence."

"The output is clear: it explains that Streamlit reruns the script, so the secret number needed to live in session state. It also shows a confidence score and the exact evidence snippets used."

Requirement covered:

- Input 1
- RAG behavior
- Evidence-grounded output
- Confidence score
- Clear output

### 2:15-3:15 - Input 2: Custom RAG Question

Screen:

- In the custom question box, type:

```text
Which test proves the hints were fixed?
```

- Click **Ask Custom Question**.
- Show the answer, confidence score, and evidence from `tests/test_game_logic.py`.

Say:

"This is a custom question, so the system is not just responding to preset buttons. It retrieves evidence from the test file and explains which tests prove that low guesses tell the player to go higher and high guesses tell the player to go lower."

"This demonstrates that the RAG guide can connect the explanation to actual testing evidence."

Requirement covered:

- Input 2
- Custom AI behavior
- RAG retrieval from tests
- Clear output

### 3:15-4:00 - Input 3: Guardrail / Fallback

Screen:

- In the custom question box, type:

```text
Explain database migrations and cloud billing
```

- Click **Ask Custom Question**.
- Show the fallback response and confidence score.

Say:

"This is the guardrail behavior. The question is unrelated to the project. Instead of pretending it knows the answer, the system returns a not-enough-evidence response and gives `0.00` confidence."

"This matters because responsible AI should be honest when it does not have enough context."

Requirement covered:

- Input 3
- Reliability/guardrail behavior
- Low-confidence fallback
- Clear output

### 4:00-4:45 - Reliability / Evaluation

Screen:

- Show the terminal with the pytest result.
- Make sure `26 passed` is visible.

Say:

"The system also has automated tests. The final result is **26 out of 26 tests passed**. The tests cover the game logic, retrieval behavior, fallback behavior, and confidence scoring."

"So the project is not only a working demo. It has checks that prove the main behaviors work."

Requirement covered:

- Reliability/evaluation behavior
- Automated tests

### 4:45-5:30 - Architecture and Closing

Screen:

- Show the README architecture diagram, or stay on the app output if time is short.

Say:

"The architecture is simple: the user asks a question in Streamlit, `rag_utils.py` retrieves matching project evidence, and the museum guide generates an answer with confidence. Human review and pytest are both part of checking the system."

"What I learned is that AI-generated code can run and still be wrong. Responsible AI needs evidence, tests, confidence scoring, and fallback behavior."

Requirement covered:

- System explanation
- Reflection

## Loom Must-Show Summary

If you are nervous, make sure these exact moments appear in the video:

1. **Normal app run:** one guess submitted with visible feedback.
2. **RAG preset input:** `Shapeshifting Secret Number` with answer, confidence, and evidence.
3. **RAG custom input:** `Which test proves the hints were fixed?` with answer and test evidence.
4. **Guardrail input:** `Explain database migrations and cloud billing` with fallback and `0.00` confidence.
5. **Evaluation:** terminal showing `26 passed`.

## Short Live Peer Presentation

Tomorrow's peer presentation can be about 3 minutes plus questions. It does not need every required grading feature.

### 0:00-0:30 - Intro

"My project is **Game Glitch Investigator: Glitch Museum Mode**. I turned a fixed AI-generated guessing game into a RAG museum that explains the old bugs using project evidence."

### 0:30-1:45 - Favorite Feature

Show `Shapeshifting Secret Number`.

Say:

"This is my favorite part because it turns a bug into an exhibit. The system retrieves evidence from the reflection and app code, then explains why the secret number used to change."

Point out:

- confidence score,
- retrieved evidence,
- project-specific explanation.

### 1:45-2:30 - Most Responsible Feature

Show the unrelated question:

```text
Explain database migrations and cloud billing
```

Say:

"This is the responsible AI part. The app does not fake an answer when it lacks evidence. It gives low confidence and says it cannot find enough project context."

### 2:30-3:00 - What I Learned

Say:

"The biggest thing I learned is that AI-generated code can look fine but still behave incorrectly. Testing, retrieval evidence, confidence scoring, and fallback behavior helped make the system more trustworthy."

## Final Reminder

For grading, prioritize the Loom. For peers, prioritize the interesting story.
