import random
import streamlit as st
from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
# Fix: sidebar now shows remaining attempts using session state instead of the static limit
st.sidebar.caption(f"Attempts remaining: {attempt_limit - st.session_state.get('attempts', 0)}")

if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

# Fix: reset secret, attempts, score, history, and status when difficulty changes
if st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.last_hint = None
    st.session_state.balloons_shown = False

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# Fix: track last hint in session state so it persists across reruns
if "last_hint" not in st.session_state:
    st.session_state.last_hint = None

# Fix: track whether win balloons have already been shown so reruns don't re-trigger them
if "balloons_shown" not in st.session_state:
    st.session_state.balloons_shown = False

st.subheader("Make a guess")

# Fix: info bar now shows the actual difficulty range instead of hardcoded 1-100
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    # Fix: disable submit button once the game is won or lost
    submit = st.button("Submit Guess 🚀", disabled=st.session_state.get("status") != "playing")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# Fix: new game now resets attempts, secret, status, history, and score
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.score = 0
    st.session_state.last_hint = None
    st.session_state.balloons_shown = False
    st.success("New game started.")
    st.rerun()
# Fix: display hint from session state after rerun so it shows alongside updated history/score
if st.session_state.last_hint and show_hint:
    kind, msg = st.session_state.last_hint
    if kind == "warning":
        st.warning(msg)
    else:
        st.error(msg)

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        if not st.session_state.balloons_shown:
            st.balloons()
            st.session_state.balloons_shown = True
        st.success(
            f"🎉 You won! The secret was {st.session_state.secret}. "
            f"Final score: {st.session_state.score}"
        )
    else:
        st.error(
            f"Out of attempts! The secret was {st.session_state.secret}. "
            f"Score: {st.session_state.score}"
        )
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        st.session_state.last_hint = ("error", err)
        st.rerun()
    else:
        # Fix: only count attempt when guess is valid so invalid inputs don't waste attempts
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # Fix: always compare secret as int — converting to str caused string comparison
        # bugs where e.g. "4" > "22" evaluated True (alphabetical order), flipping the hint
        outcome, message = check_guess(guess_int, st.session_state.secret)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.session_state.status = "won"
            st.session_state.last_hint = None
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.session_state.last_hint = None
        else:
            # Fix: store hint in session state and rerun so debug panel shows updated history/score
            st.session_state.last_hint = ("warning", message)

        st.rerun()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
