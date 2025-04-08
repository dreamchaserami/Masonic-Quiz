import streamlit as st
import time
import pandas as pd
from datetime import datetime

# ---- QUESTIONS ---- #
question_bank = {
    "Entered Apprentice": [
        ("What are the three great lights?",
         ["The Holy Bible, Square, Compass", "The trestle board, burning tapers", "The square, plumb, level", "The sun, moon, Worshipful Master"], "a"),
        ("As an Entered Apprentice, from whence you came?",
         ["Egypt", "Lodge of H.B. Turner", "Lodge of Due Guard", "Lodge of the Holy Saints John"], "d"),
        ("What came you here to do?",
         ["To seek light", "To improve my passions", "To subdue my passions and improve myself in Masonry", "To learn secrets"], "c"),
        ("Then I presume you are a Mason?",
         ["I am so taken and acknowledged", "I am", "I received the light", "I'm cautious"], "a"),
        ("What makes you a Mason?",
         ["The Bible", "My Obligation", "My Word", "God's Word"], "b"),
        ("How do you know yourself to be a mason?",
         ["I know my penalty and signs", "Tried and never denied", "I know my obligation", "I have grip, token, and sign"], "b"),
        ("How shall I know you to be a mason?",
         ["Tried and never denied", "Recognized by brothers", "Subduing passions", "Signs, token, word, and entrance"], "d"),
        ("What are signs?",
         ["Bible, Square, Compass", "Grip called due guard", "Right angles and perpendiculars", "Three burning tapers"], "c"),
        ("What is a token?",
         ["Password from St. John", "Square, level, plumb", "Grip to identify in dark/light", "Your apron"], "c"),
        ("What do you conceal?",
         ["My signs and tokens", "My obligation", "All secrets except rightful", "Bible, square, compass"], "c"),
    ],
    "Fellow Craft": [
        ("What is the wage of a Fellow Craft?",
         ["Corn, wine, oil", "Knowledge and wisdom", "Five orders of architecture", "Brotherly love, relief, truth"], "a"),
        ("Where is the winding staircase?",
         ["Second degree lodge", "East side of the temple", "Between pillars", "Behind the altar"], "a"),
        ("How many steps lead to the Middle Chamber?",
         ["3", "7", "15", "33"], "c"),
    ],
    "Master Mason": [
        ("Who was Hiram Abiff?",
         ["Architect of King Solomon’s Temple", "First Grand Master", "Builder of the Ark", "Keeper of the Temple Scrolls"], "a"),
        ("What are the three Ruffians’ names?",
         ["Jubela, Jubelo, Jubelum", "Abiram, Aholiab, Jehoash", "Tyrus, Sidon, Judah", "Jubela, Jubelum, Jubelo"], "d"),
        ("What does the sprig of acacia symbolize?",
         ["Immortality", "Brotherhood", "New beginnings", "Secrecy"], "c"),
    ]
}

# ---- INITIAL STATE ---- #
if 'name' not in st.session_state: st.session_state.name = ""
if 'degree' not in st.session_state: st.session_state.degree = "Entered Apprentice"
if 'quiz_started' not in st.session_state: st.session_state.quiz_started = False
if 'current_q' not in st.session_state: st.session_state.current_q = 0
if 'score' not in st.session_state: st.session_state.score = 0
if 'completed' not in st.session_state: st.session_state.completed = False
if 'user_answers' not in st.session_state: st.session_state.user_answers = []
if 'start_time' not in st.session_state: st.session_state.start_time = None

# ---- CONFIG ---- #
st.set_page_config(page_title="Masonic Quiz", layout="centered")
st.title("🧱 Masonic Degree Quiz")

# ---- QUIZ SETUP ---- #
if not st.session_state.quiz_started:
    st.session_state.name = st.text_input("Enter your name:")
    st.session_state.degree = st.selectbox("Select Degree Level:", list(question_bank.keys()))

    if st.button("Start Quiz") and st.session_state.name:
        st.session_state.quiz_started = True
        st.session_state.start_time = time.time()
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Freemasonry_Emblem.svg/320px-Freemasonry_Emblem.svg.png", width=100)
        st.success(f"Welcome Brother {st.session_state.name}, let's begin the {st.session_state.degree} quiz.")

# ---- QUIZ LOOP ---- #
elif not st.session_state.completed:
    q_list = question_bank[st.session_state.degree]
    q_idx = st.session_state.current_q
    q_text, opts, correct_letter = q_list[q_idx]

    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Freemasonry_Emblem.svg/320px-Freemasonry_Emblem.svg.png", width=80)
    st.progress(q_idx / len(q_list))
    st.subheader(f"Question {q_idx + 1} of {len(q_list)}")
    st.write(q_text)

    selected = st.radio("Choose one:", opts, index=None, key=f"q_{q_idx}")

    time_limit = 30  # seconds per question
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, time_limit - elapsed)
    st.info(f"⏱️ Time remaining: {remaining} seconds")

    if remaining == 0:
        st.warning("Time's up! Moving to the next question...")
        selected = None

    if st.button("Submit Answer"):
        correct_text = opts[ord(correct_letter) - ord('a')]
        is_correct = selected == correct_text

        st.session_state.user_answers.append({
            "question": q_text,
            "selected": selected or "(No answer)",
            "correct": correct_text,
            "result": "✅ Correct" if is_correct else "❌ Incorrect"
        })

        if is_correct:
            st.session_state.score += 1

        st.session_state.current_q += 1
        st.session_state.start_time = time.time()  # Reset timer

        if st.session_state.current_q >= len(q_list):
            st.session_state.completed = True

        st.rerun()

# ---- QUIZ COMPLETE ---- #
if st.session_state.completed:
    total = len(question_bank[st.session_state.degree])
    st.success(f"{st.session_state.name}, you scored {st.session_state.score} out of {total}.")

    if st.session_state.score == total:
        st.balloons()
        st.info("Perfect knowledge!")
    elif st.session_state.score >= total // 2:
        st.info("Well done, keep studying!")
    else:
        st.warning("Keep learning, Brother. You’ll get there!")

    # Save score to CSV
    score_data = {
        "Name": st.session_state.name,
        "Degree": st.session_state.degree,
        "Score": st.session_state.score,
        "Total": total,
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    df = pd.DataFrame([score_data])
    df.to_csv("masonic_scores.csv", mode='a', index=False, header=not pd.io.common.file_exists("masonic_scores.csv"))
    st.success("Your score has been saved.")

    # Review answers
    st.markdown("### 🔍 Review Your Answers")
    for idx, ans in enumerate(st.session_state.user_answers):
        st.write(f"**Q{idx+1}:** {ans['question']}")
        st.write(f"- Your answer: {ans['selected']}")
        st.write(f"- Correct answer: {ans['correct']}")
        st.write(f"- Result: {ans['result']}")
        st.markdown("---")

    if st.button("Restart Quiz"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
