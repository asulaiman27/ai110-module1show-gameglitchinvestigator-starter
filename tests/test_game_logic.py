from logic_utils import check_guess, get_hint_message, new_game_state, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


def test_hint_direction_is_not_reversed():
    # Regression test for the "lying hints" bug.
    # A guess that is too HIGH must tell the player to go LOWER, and a guess
    # that is too LOW must tell them to go HIGHER. Previously these were swapped.
    too_high_message = get_hint_message(check_guess(60, 50))
    assert "LOWER" in too_high_message
    assert "HIGHER" not in too_high_message

    too_low_message = get_hint_message(check_guess(40, 50))
    assert "HIGHER" in too_low_message
    assert "LOWER" not in too_low_message


def test_new_game_fully_resets_state():
    # Regression test for the "New Game" bug: a finished game used to stay
    # "won"/"lost" with stale score/history, so you couldn't actually replay.
    state = new_game_state(1, 100)
    assert state["status"] == "playing"
    assert state["attempts"] == 1
    assert state["score"] == 100
    assert state["history"] == []


def test_new_game_secret_respects_difficulty_range():
    # Regression test: New Game used to hardcode randint(1, 100), ignoring the
    # difficulty range. The secret must fall within the requested bounds.
    for _ in range(100):
        secret = new_game_state(1, 20)["secret"]
        assert 1 <= secret <= 20


def test_wrong_guess_subtracts_ten():
    # Each incorrect guess (too high or too low) costs 10 points, regardless
    # of attempt number.
    assert update_score(100, "Too High", 2) == 90
    assert update_score(100, "Too High", 3) == 90
    assert update_score(100, "Too Low", 2) == 90


def test_win_does_not_change_score():
    # The win bonus was dropped: winning leaves the current score untouched,
    # so the player simply keeps whatever they have left.
    assert update_score(50, "Win", 2) == 50
    assert update_score(100, "Win", 5) == 100
