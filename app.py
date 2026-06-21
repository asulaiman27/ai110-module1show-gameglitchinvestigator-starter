import random
import streamlit as st

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    get_hint_message,
    update_score,
    new_game_state,
)

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
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    # FIX: score now starts at 100 instead of 0. Claude, agent mode.
    st.session_state.score = 100

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# FIX: track an input-key nonce and a feedback queue so we can clear the guess
# box on each click while still showing messages. Added with Claude in agent mode.
if "input_nonce" not in st.session_state:
    st.session_state.input_nonce = 0

if "feedback" not in st.session_state:
    st.session_state.feedback = []

# FIX: regenerate the secret (and start a fresh game) whenever the difficulty
# changes, so the actual number always falls within the range shown on the UI
# instead of keeping the first difficulty's secret. Claude, agent mode.
if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

if st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.update(new_game_state(low, high))
    st.session_state.input_nonce += 1
    st.session_state.feedback = [
        ("info", f"Difficulty set to {difficulty}. New game started!")
    ]
    st.rerun()

st.subheader("Make a guess")

st.info(
    # FIX: show the real difficulty range (low..high) instead of a hardcoded
    # "1 and 100". Claude, agent mode.
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

# FIX: added a Scoring Rules tab so players can see how points work, matching
# the corrected update_score logic. Built with Claude in agent mode.
rules_tab, debug_tab = st.tabs(["📊 Scoring Rules", "🛠️ Developer Debug Info"])

with rules_tab:
    st.markdown(
        """
        **Your score starts at 100.** 💯

        - ❌ **Wrong guess (too high or too low):** **−10 points** each.
        - 🎉 **Correct guess (Win):** you keep whatever score you have left —
          win in fewer guesses to finish higher!
        - 💀 **Out of attempts:** your score drops to **0**.

        Win in as few attempts as possible to finish with the highest score. 🏆
        """
    )

with debug_tab:
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    # FIX: include the nonce in the key so bumping it on submit/new game forces
    # a fresh, empty input widget (clears the typed number). Claude, agent mode.
    key=f"guess_input_{difficulty}_{st.session_state.input_nonce}",
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# FIX: render feedback queued by the previous click, then clear it. Queuing
# (instead of showing inline) lets messages survive the rerun that resets the
# input box and Submit button. Built with Claude in agent mode.
for _kind, _text in st.session_state.feedback:
    getattr(st, _kind)(_text)
st.session_state.feedback = []
if st.session_state.pop("show_balloons", False):
    st.balloons()

if new_game:
    # FIX: New Game now fully resets state (attempts, score, status, history)
    # using the difficulty range, instead of leaving a finished game stuck.
    # Debugged and refactored with Claude in agent mode.
    st.session_state.update(new_game_state(low, high))
    # FIX: also clear the typed guess and reset the Submit button on every New
    # Game click by bumping the input key nonce. Claude, agent mode.
    st.session_state.input_nonce += 1
    st.session_state.feedback = [("success", "New game started.")]
    st.rerun()
#FIXME: Logic breaks here
if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.session_state.feedback.append(("error", err))
    else:
        st.session_state.history.append(guess_int)

        outcome = check_guess(guess_int, st.session_state.secret)
        message = get_hint_message(outcome)

        if show_hint:
            st.session_state.feedback.append(("warning", message))

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.session_state.show_balloons = True
            st.session_state.status = "won"
            st.session_state.feedback.append((
                "success",
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}",
            ))
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                # FIX: running out of attempts now resets the score to 0.
                # Claude, agent mode.
                st.session_state.score = 0
                st.session_state.feedback.append((
                    "error",
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}",
                ))

    # FIX: after each guess, clear the input field and reset the Submit button
    # by bumping the input key nonce, then rerun. Claude, agent mode.
    st.session_state.input_nonce += 1
    st.rerun()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
