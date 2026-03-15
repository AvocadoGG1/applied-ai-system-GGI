# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

1. The game was asking me to go lower numbers than the range, so less than 0, which I expect it to be in range. It never went higher, it was always lower. You could also type any number outside the difficulty range and it would still be accepted as a valid guess.
2. The new game button wouldnt reset the amount of attempts I had, I thought I would continue. 
3. When you clicked the new game the secret could be out of range of a difficulty, because the new game button used a hardcoded range of 1–100 instead of the selected difficulty's range.
4. The hints were backwards — when I guessed too low it told me to go lower, and when I guessed too high it told me to go higher, so the messages were completely misleading.
5. The attempts remaining in the sidebar always showed the total allowed and never counted down as I made guesses, so I had no live tracking of how many attempts I had left.
6. Changing the difficulty mid-game did not reset the secret number, so the secret could be completely outside the new difficulty's range and the game would be unwinnable.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Claude Code as my main AI tool throughout the project. I described bugs in plain English and Claude helped me locate the exact lines responsible and write the fixes.

One example of a correct suggestion was when I asked why invalid guesses were still consuming attempts. Claude pointed out that `st.session_state.attempts += 1` was running before `parse_guess` was even called, so every button press counted regardless of whether the input was valid. It moved the increment inside the `else` block so only valid guesses cost an attempt — I verified this by running the game and confirming bad inputs no longer counted down my attempts.

One example where I had to guide the AI was the out-of-range validation. The first version of `parse_guess` only rejected negative numbers, and Claude did not automatically add difficulty range checking until I specifically asked for it. This showed me that AI gives you exactly what you ask for, so I need to be precise and complete when describing what I want.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was really fixed when a pytest I wrote specifically for that bug went from failing to passing, and I also manually ran the game to confirm the behavior felt correct in the browser.

One test I wrote was `test_hint_too_low_tells_player_to_go_higher`, which called `check_guess(30, 50)` and asserted the message contained "HIGHER". Before the fix this test failed because the message said "Go LOWER!" — the wrong direction. After swapping the messages in `check_guess`, the test passed and I confirmed in the game that guessing too low now correctly told me to go higher.

Yes, Claude helped design most of the tests. For each bug I described, it wrote a pytest that directly targeted the broken behavior — for example, it structured `test_new_game_button_resets_status` to simulate the session state dictionary and assert that `status` returned to `"playing"` after a new game, which made the missing reset line in `app.py` immediately visible as a failure.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

The secret number kept changing because every time the player clicked a button, Streamlit re-ran the entire Python script from the top. The line `st.session_state.secret = random.randint(low, high)` was outside any condition, so it generated a brand new secret on every single rerun — the game never remembered what number it had picked.

I would explain Streamlit to a friend like this: imagine your entire program is a function that gets called again from scratch every time the user does anything — clicks a button, types in a box, anything. Session state is like a sticky note that survives between those calls, so you can write something on it once and it stays there even when the program reruns. Without session state, every variable resets to whatever the code says at the top.

The fix was wrapping the secret generation in a `if "secret" not in st.session_state:` guard. That way the secret is only generated once on the very first load, and every rerun after that just reads the existing value from session state instead of rolling a new number.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to carry forward is writing a pytest specifically targeting the broken behavior before fixing it, so I can confirm the test fails first and then passes after the fix. That red-to-green pattern gave me real confidence that the bug was actually fixed and not just hidden.

Next time I work with AI on a coding task I would describe the full acceptance criteria upfront — for example, stating "the New Game button must reset score, history, status, and attempts" rather than just "fix the New Game button." Being vague got me partial fixes that I had to loop back on multiple times.

This project changed the way I think about AI-generated code because I used to assume that if the code ran without errors it was probably correct. Now I understand that the code can run perfectly and still have logic bugs, misleading behavior, and nonsense scoring rules — AI-generated code needs the same skeptical review as any other code.

- For Commit
