import streamlit as st
import random

class Question:
    def __init__(self, prompt, answer):
        self.prompt = prompt
        self.answer = answer

question_prompts = [
    "What are the three great lights?",
    "As an Entered Apprentice, from whence you came?",
    "What came you here to do?",
    "Then I presume you are a Mason?",
    "What makes you a Mason?",
    "How do you know yourself to be a mason?",
    "How shall I know you to be a mason?",
    "What are signs?",
    "What is a token?",
    "What do you conceal?"
]

options = [
    ["The Holy Bible, Square, Compass", "The trestle board, burning tapers, indented trestle", "The square, plumb, level", "The sun, moon, Worshipful Master"],
    ["Egypt", "From the lodge of H.B. Turner", "Lodge of Due Guard", "From the Lodge of the Holy Saints John"],
    ["To seek light", "To improve my passions", "To subdue my passions and improve myself in Masonry", "To learn secrets"],
    ["I am so taken and acknowledged among brothers and fellows", "I am", "I am because I received the light", "I'm cautious"],
    ["The Bible", "My Obligation", "My Word", "Gods word"],
    ["The fact that I know my penalty and signs", "By having been often tried and never denied, and am willing to be tried again", "I known my obligation", "By having a grip, token , and sign"],
    ["By having been often tried and never denied", "By being recognized by other brothers", "By subduing my passions and improving myself in masonry", "By certain signs, a token, a word, and the principal points of my entrance"],
    ["The Holy Bible, Square, Compass", "A grip called the due guard", "Right angles, horizontals, and perpendiculars", "The three burning tapers"],
    ["The password from the Holy St John", "Either the square, level, plumb", "A certain fraternal and brotherly grip whereby one Mason may know one another in the dark as well as in the light", "Your apron"],
    ["My signs and tokens", "My obligation", "All the secrets of Masons in masonry except it be to him or them they rightfully belong.", "The Holy bible, square, Compass"]
]

answers = ['a', 'd', 'c', 'a', 'b', 'b', 'd', 'c', 'c', 'c']
questions = [Question(p, a) for p, a in zip(question_prompts, answers)]

# Session state to keep track of quiz progress
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'completed' not in st.session_state:
    st.session_state.completed = False
if 'master' not in st.session_state:
    st.session_state.master = None
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = []

st.title("Masonic Entered Apprentice Quiz")

if not st.session_state.name:
    st.session_state.name = st.text_input("What is your name?")
    st.session_state.master = st.radio("Are you a Master Mason?", ["Yes", "No"], index=None)

    if st.session_state.name and st.session_state.master and st.button("Start Quiz"):
        st.image("https://i.imgur.com/zY3qOZt.png", width=120)
        if st.session_state.master == "Yes":
            st.info(f"Great! Get ready to learn, {st.session_state.name}.")
        else:
            st.info("Time will get you where you need to be.")
        st.info("Let's start off with some Entered Apprentice questions.")

elif not st.session_state.completed:
    q_idx = st.session_state.current_q
    st.progress(q_idx / len(questions))
    st.subheader(f"Question {q_idx + 1} of {len(questions)}")
    st.write(question_prompts[q_idx])
    radio_key = f"user_answer_{q_idx}"

    # ✅ FIX: Use the value from st.radio without trying to manually assign to session_state
    user_answer = st.radio("Choose one:", options[q_idx], index=None, key=radio_key)

    if st.button("Submit Answer"):
        user_answer = st.session_state[radio_key]
        correct_letter = questions[q_idx].answer
        correct_text = options[q_idx][ord(correct_letter) - ord('a')]

        st.session_state.user_answers.append({
            'question': question_prompts[q_idx],
            'selected': user_answer,
            'correct': correct_text
        })

        if user_answer == correct_text:
            st.success("Correct!")
            st.session_state.score += 1
        else:
            st.error(f"Incorrect. The correct answer was: {correct_text}")

        st.session_state.current_q += 1
        if st.session_state.current_q >= len(questions):
            st.session_state.completed = True

if st.session_state.completed:
    st.markdown("---")
    st.subheader(f"You got {st.session_state.score} out of {len(questions)} correct.")
    if st.session_state.score == len(questions):
        st.success("Excellent! You have a strong understanding of the Entered Apprentice degree.")
    elif st.session_state.score >= len(questions) // 2:
        st.info("Good job! Keep studying to improve your knowledge.")
    else:
        st.warning("Keep learning and improving. Study your work and try again!")

    st.markdown("### Review Your Answers")
    for idx, item in enumerate(st.session_state.user_answers):
        st.write(f"**Q{idx+1}:** {item['question']}")
        st.write(f"- Your answer: {item['selected']}")
        st.write(f"- Correct answer: {item['correct']}")
        st.markdown("---")

    if st.button("Restart Quiz"):
        st.session_state.name = ""
        st.session_state.score = 0
        st.session_state.current_q = 0
        st.session_state.completed = False
        st.session_state.master = None
        st.session_state.user_answers = []
