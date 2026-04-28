# 5-7 Minute Presentation Plan

## Goal

Show **Game Glitch Investigator: Glitch Museum Mode** running end-to-end, demonstrate the RAG feature, show reliability behavior, and explain what I learned.

## Recording Flow

Use this screen order:

1. Streamlit app title/top of page
2. Original number guessing game demo
3. Glitch Museum Mode preset artifact
4. Glitch Museum Mode custom test question
5. Glitch Museum Mode unrelated question fallback
6. README architecture diagram
7. Terminal pytest result
8. Reflection closing screen

## Exact Presentation Script

### 0:00-0:45 - Project Intro

Screen:

- Show the top of the running Streamlit app.
- Make sure the project title and main game area are visible.
- Do not show code yet.

Speaker Notes:

"My project is called **Game Glitch Investigator: Glitch Museum Mode**. It started as a Streamlit number guessing game called **Game Glitch Investigator: The Impossible Guesser**. The original version had AI-generated bugs in the game logic, so my first job was to debug the game and make it actually reliable.

After fixing the core game, I added an AI feature: a RAG-powered museum guide. The guide explains the old bugs using evidence from the project files instead of just making up a general answer. The final project combines a playable app, automated tests, retrieved evidence, and confidence scoring."

Transition:

"I will start by showing the fixed game, then I will show the RAG museum guide and the reliability guardrails."

### 0:45-1:30 - Original Game Demo

Screen:

- Stay in the Streamlit app.
- Show the difficulty selector.
- Show the guess input box.
- Pick a difficulty.
- Enter one valid guess.
- Click the guess/submit button.
- Show the feedback message.
- If visible, briefly show the debug panel.

Speaker Notes:

"This is the original number guessing game after the logic fixes. The player chooses a difficulty, enters a guess, and the app gives higher or lower feedback.

The important part is that the game now behaves consistently. The original version had bugs like changing the secret number during the game, giving backwards hints, accepting invalid guesses, and not resetting correctly. I fixed those issues and added tests so the game logic can be checked automatically."

Transition:

"Now I am going to scroll down to the AI part of the project, which is Glitch Museum Mode."

### 1:30-2:15 - RAG Demo Input 1: Preset Artifact

Screen:

- Scroll to **Glitch Museum Mode**.
- In the artifact dropdown, select `Shapeshifting Secret Number`.
- Click **Inspect Artifact**.
- Show the generated explanation.
- Show the confidence score.
- Show the retrieved case-file evidence.

Speaker Notes:

"This section demonstrates the RAG feature. I selected the artifact called **Shapeshifting Secret Number**, which represents one of the original bugs.

When I click inspect, the app turns that artifact into a retrieval query. It searches project files like `README.md`, `reflection.md`, `app.py`, and the test files. Then it generates an explanation using the retrieved evidence.

The key thing to notice is that the answer is project-specific. It is not just a generic explanation of a programming bug. It is grounded in the files from this project, and the app shows the evidence it used."

Transition:

"Next I will ask a custom question instead of using a preset artifact."

### 2:15-3:00 - RAG Demo Input 2: Custom Project Question

Screen:

- In the custom question box, type: `Which test proves the hints were fixed?`
- Click **Ask Custom Question**.
- Show the generated answer.
- Point to evidence from `tests/test_game_logic.py`.
- Show the confidence score.

Speaker Notes:

"This shows that the guide can answer custom questions, not only preset museum artifacts.

Here I asked, **Which test proves the hints were fixed?** The system should retrieve evidence from the test file and explain which tests prove the higher and lower hint behavior works correctly.

This is useful because the AI feature is connected to the actual engineering work. It can explain not just what changed, but how the project verifies that the change is correct."

Transition:

"Now I will show what happens when the user asks something unrelated to the project."

### 3:00-3:30 - RAG Demo Input 3: Unrelated Question Fallback

Screen:

- In the custom question box, type: `Explain database migrations and cloud billing`
- Click **Ask Custom Question**.
- Show the fallback response.
- Show the low confidence result, especially `Not enough evidence (0.00)` if visible.

Speaker Notes:

"This is the reliability guardrail. The question is about database migrations and cloud billing, which are not part of this project.

A weaker AI system might still try to answer confidently. This system should not do that. Because it cannot retrieve relevant project evidence, it returns a low confidence score and a not-enough-evidence fallback.

That behavior matters because responsible AI systems should be honest about their limits."

Transition:

"Next I will show the architecture behind what just happened."

### 3:30-4:30 - Architecture

Screen:

- Switch to `README.md`.
- Show the **Architecture Overview** section.
- Show the Mermaid diagram rendered if possible.
- If the diagram does not render, show the Mermaid code block.

Speaker Notes:

"This diagram shows the system architecture.

The flow is simple and local. The human player or student uses the Streamlit app. The app sends the selected artifact or custom question into `rag_utils.py`. That file handles retrieval, answer generation, and confidence scoring.

The knowledge base is made from project files such as `README.md`, `reflection.md`, `app.py`, `logic_utils.py`, and the test files. The retriever pulls the most relevant evidence snippets, and the museum guide uses those snippets to create a project-specific explanation in Streamlit.

Testing is also part of the architecture. `pytest` checks both the original game logic and the RAG helper functions."

Transition:

"Now I will show the reliability side more directly with the automated tests."

### 4:30-5:45 - Reliability and Testing

Screen:

- Show a terminal with the pytest result if available.
- Best screen: a terminal result showing `26 passed`.
- If the terminal result is not available, show the README testing summary or the `tests` folder.

Speaker Notes:

"The system proves reliability in two main ways.

First, automated tests check the original game logic and the RAG helper functions. The final result is **26 out of 26 automated tests passed**. These tests cover things like valid guesses, invalid guesses, reset behavior, hint direction, retrieval behavior, and fallback behavior.

Second, the RAG feature includes confidence scoring. The confidence score is based on the strength and diversity of retrieved evidence. If the question is empty or unrelated to the project, the system does not pretend it has an answer. It uses a fallback response instead.

So reliability here is not just whether the app runs. It is whether the app behaves correctly, whether the AI answer is grounded in evidence, and whether the system refuses questions it cannot support."

Transition:

"I will finish with what I learned from building and debugging this project."

### 5:45-6:45 - Reflection

Screen:

- Show `reflection.md`, or keep the app visible on the unrelated-question fallback response.
- If using `reflection.md`, show a section that discusses debugging, testing, or responsible AI.

Speaker Notes:

"This project taught me that AI-generated code can run and still be wrong. The original game looked like a working app, but the behavior was unreliable. That made testing and careful debugging necessary.

The biggest lesson was that responsible AI needs evidence, tests, and guardrails. The RAG guide is useful because it explains the project using retrieved evidence. The confidence score is important because it helps show when the system has enough support for an answer and when it does not.

I also learned how to work with AI as a teammate. It was helpful for refactoring and test ideas, but I still had to verify its suggestions. One early validation fix only rejected negative numbers and missed out-of-range guesses, so human review still mattered.

What this project says about me as an AI engineer is that I care about building AI systems that are useful, testable, and honest about their limits."

Final line:

"That is my demo of **Game Glitch Investigator: Glitch Museum Mode**."

## Loom Recording Checklist

Before recording:

- Run the Streamlit app.
- Have the browser open to the app.
- Have `README.md` ready at the architecture diagram.
- Have a terminal ready with the latest pytest result, or be ready to run `pytest`.
- Have `reflection.md` ready for the closing section.

During recording, clearly show:

- End-to-end app behavior.
- One normal game guess.
- Preset artifact RAG response.
- Custom project question RAG response.
- Unrelated question fallback.
- Confidence scores.
- Retrieved evidence snippets.
- Architecture diagram.
- Passing tests.

You do not need to show:

- Code installation.
- File setup.
- A full code walkthrough.
