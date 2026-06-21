import random


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome.

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def get_hint_message(outcome: str):
    """Return the player-facing hint message for a given outcome."""
    # FIX: Higher/Lower hints were flipped (I spotted it playing the UI;
    # corrected the directions with Claude in agent mode).
    if outcome == "Win":
        return "🎉 Correct!"
    if outcome == "Too High":
        return "📉 Go LOWER!"
    if outcome == "Too Low":
        return "📈 Go HIGHER!"
    return ""


def new_game_state(low: int, high: int):
    """Return a fresh game-state dict for a new game within [low, high]."""
    # FIX: "New Game" only reset some fields, so a finished game stayed
    # "won"/"lost" and the secret ignored the difficulty range. Built this
    # single reset helper with Claude in agent mode so every field resets.
    return {
        "secret": random.randint(low, high),
        "attempts": 1,
        # FIX: score now starts at 100 instead of 0. Claude, agent mode.
        "score": 100,
        "status": "playing",
        "history": [],
    }


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # FIX: dropped the win bonus — winning no longer adds points, the player
    # simply keeps their remaining score. Claude, agent mode.
    if outcome == "Win":
        return current_score

    # FIX: every incorrect guess (too high or too low) now costs 10 points.
    # Claude, agent mode.
    if outcome in ("Too High", "Too Low"):
        return current_score - 10

    return current_score
