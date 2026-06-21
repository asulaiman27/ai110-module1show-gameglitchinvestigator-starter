# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

  - Hints are backwards - the UI shows a "go higher" hint then the real number is actually below the guess and "go lower" when the real number is actually above the guess
  - The "New Game" button is buggy - it sometimes doesn't register and requires a websitre restart to actually fix the game
  - When I switch difficulties, only the guess count gets updated on the main UI, not the range of numbers. Easy is supposed to show 1-20, but it only shows 1-100 because it doesn't update from the normal

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|Guess of 1|Go HIGHER|go LOWER|none|
|"New Game" button pressed |UI reset with a new game and number|New game required ntoifcation doesn't dissapear, and button does not work|none|
|Changing difficult to "Easy" |Range changes from 1-20 with 6 guesses|Range stays the same but guesses changes to 6|none|

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I just used Claude
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
The AI suggested that other logic test cases could would fail when I asked it to add in test cases for the changes I made. It was able to fix these cases and when I ran pytest all cases passed.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
To "run" the game, the AI first tried to take a screenshot of the live app with headless Chrome and acted like that would show me the working UI. When I looked at the actual image it was just a blank gray loading skeleton, not the game, because Streamlit renders over a websocket after the screenshot is taken. I verified this by opening the screenshot myself and seeing nothing useful, and the AI switched to Streamlit's AppTest instead, which actually ran the app and let it click buttons and read the real values.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I didn't trust that the code "looked right" — I ran `pytest` after every change and also drove the real app to watch the behavior. For example, after fixing the hints I confirmed a guess that was too high actually told me to go LOWER, and after changing the scoring I checked the real numbers: score started at 100, dropped 10 per wrong guess, and went to 0 when I ran out of attempts. A fix only counted as done once both the tests passed and the app behaved correctly.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
The clearest one was the hint-direction test: `check_guess(60, 50)` is too high, so the message should contain "LOWER". On the broken code that test failed because the message said "Go HIGHER!", and after the fix it passed. That showed me the bug wasn't in the higher/lower comparison itself but in the message text that got attached to the outcome.

- Did AI help you design or understand any tests? How?
Yes. The AI wrote a regression test for each bug I fixed and explained the key idea that a good regression test should fail on the buggy code and pass after the fix, so it actually proves the bug is gone. It also caught that the starter test file was already failing because `check_guess` returned a tuple instead of a plain string, which I hadn't noticed.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Every time you touch anything on a Streamlit page — click a button, type in a box, change a dropdown — Streamlit re-runs your whole script from top to bottom. That means normal Python variables get wiped and recreated each time, so they can't remember anything. `session_state` is a dictionary that survives those reruns, so it's basically the game's memory for things like the secret number, score, and attempts. I really felt this with the input box: the typed number wouldn't clear on its own because its value lives in session state, so we had to change the widget's `key` to force Streamlit to build a fresh, empty box.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
Writing a regression test for every bug I fix, right when I fix it. Seeing tests go from failing to passing gave me real confidence the bug was actually gone instead of just hoping it was, and it left behind a safety net so a later change can't quietly bring the bug back.

- What is one thing you would do differently next time you work with AI on a coding task?
I'd be clearer about scope up front. Early on I asked the AI to refactor and it correctly moved the code but kept the bugs in place, because I hadn't said to fix them yet — so I had to go back and ask again. Next time I'll say exactly whether I want it to just reorganize or also fix behavior.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
The original game was AI-written and looked polished and "production-ready," but it was full of subtle bugs like flipped hints and broken state handling. It taught me that AI code has to be read, tested, and run before I trust it, not accepted just because it looks confident and clean.
