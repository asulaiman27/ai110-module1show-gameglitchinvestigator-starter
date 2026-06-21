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
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
