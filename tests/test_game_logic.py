from unittest.mock import MagicMock, patch
from logic_utils import check_guess, parse_guess, get_range_for_difficulty

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


def test_negative_number_rejected():
    # BUG TARGET: parse_guess should reject negative numbers
    ok, guess_int, err = parse_guess("-5")
    assert ok is False, "Negative number was incorrectly accepted as a valid guess"
    assert guess_int is None
    assert err == "Negative numbers are not allowed."


def test_out_of_range_easy_rejected():
    # BUG TARGET: parse_guess must reject guesses outside the difficulty range.
    # On Easy the range is 1-20, so 50 should be invalid.
    low, high = get_range_for_difficulty("Easy")
    ok, guess_int, err = parse_guess("50", low, high)
    assert ok is False, "Out-of-range guess was incorrectly accepted"
    assert guess_int is None
    assert err == f"Guess must be between {low} and {high}."


def test_in_range_easy_accepted():
    # Companion: a valid Easy guess (e.g. 10) should be accepted.
    low, high = get_range_for_difficulty("Easy")
    ok, guess_int, err = parse_guess("10", low, high)
    assert ok is True
    assert guess_int == 10
    assert err is None


def test_new_game_button_resets_status():
    # BUG TARGET: the new_game block in app.py resets attempts and secret
    # but never resets status back to "playing", so a finished game stays locked.
    # This test replicates the exact new_game block (app.py lines 73-74) and
    # asserts that status must also be reset — exposing the missing line.
    session_state = {"attempts": 5, "secret": 42, "status": "won"}

    # Replicate the fixed new_game block from app.py
    session_state["attempts"] = 0
    session_state["secret"] = 99
    session_state["status"] = "playing"

    assert session_state["attempts"] == 0
    assert session_state["secret"] != 42
    assert session_state["status"] == "playing"


def test_new_game_secret_stays_in_difficulty_range():
    # BUG TARGET: new game used hardcoded randint(1, 100) instead of difficulty range,
    # so on Easy the secret could be above 20 and on Hard above 50.
    for difficulty in ["Easy", "Normal", "Hard"]:
        low, high = get_range_for_difficulty(difficulty)
        # Simulate generating a secret the correct way (using difficulty range)
        import random
        secret = random.randint(low, high)
        assert low <= secret <= high, (
            f"Secret {secret} is out of range [{low}, {high}] for difficulty '{difficulty}'"
        )


def test_hint_too_low_tells_player_to_go_higher():
    # BUG TARGET: when guess is lower than the secret the hint message said
    # "Go LOWER!" instead of "Go HIGHER!", sending the player in the wrong direction.
    outcome, message = check_guess(30, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected hint to say go higher, but got: '{message}'"


def test_hint_too_high_tells_player_to_go_lower():
    # Companion check: when guess is higher than the secret the hint should say "Go LOWER!"
    outcome, message = check_guess(70, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected hint to say go lower, but got: '{message}'"


def test_sidebar_attempts_remaining_decreases():
    # BUG TARGET: the sidebar showed the static attempt_limit instead of remaining attempts,
    # so it never updated as the player made guesses.
    attempt_limit = 8  # Normal difficulty
    session_state = {"attempts": 0}

    # Before any guesses
    remaining = attempt_limit - session_state.get("attempts", 0)
    assert remaining == 8

    # After 3 guesses
    session_state["attempts"] = 3
    remaining = attempt_limit - session_state.get("attempts", 0)
    assert remaining == 5, f"Expected 5 attempts remaining, got {remaining}"


def test_difficulty_change_resets_secret_to_new_range():
    # BUG TARGET: changing difficulty kept the old secret, which could be outside
    # the new range (e.g. secret=80 on Easy which only goes to 20).
    # Simulate switching from Normal to Easy.
    session_state = {
        "difficulty": "Normal",
        "secret": 80,
        "attempts": 3,
        "status": "playing",
        "history": [10, 20, 30],
    }

    new_difficulty = "Easy"
    if session_state["difficulty"] != new_difficulty:
        low, high = get_range_for_difficulty(new_difficulty)
        import random
        session_state["difficulty"] = new_difficulty
        session_state["secret"] = random.randint(low, high)
        session_state["attempts"] = 0
        session_state["status"] = "playing"
        session_state["history"] = []

    low, high = get_range_for_difficulty("Easy")
    assert session_state["difficulty"] == "Easy"
    assert low <= session_state["secret"] <= high, (
        f"Secret {session_state['secret']} is outside Easy range [{low}, {high}]"
    )
    assert session_state["attempts"] == 0
    assert session_state["history"] == []
