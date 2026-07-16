import random

import streamlit as st

st.set_page_config(page_title="중학생 영단어 게임", page_icon="📚", layout="centered")

st.title("📚 중학생 영단어 게임")
st.write("난이도를 선택하고, 뜻에 맞는 영어 단어를 맞혀 보세요!")

QUIZ_DATA = {
    "쉬움": [
        {"word": "friend", "choices": ["친구", "학교", "집", "책"], "answer": "친구"},
        {"word": "school", "choices": ["집", "학교", "친구", "바다"], "answer": "학교"},
        {"word": "happy", "choices": ["슬픈", "행복한", "배고픈", "빠른"], "answer": "행복한"},
        {"word": "weather", "choices": ["날씨", "시간", "음식", "음악"], "answer": "날씨"},
        {"word": "book", "choices": ["책", "연필", "의자", "문"], "answer": "책"},
    ],
    "보통": [
        {"word": "improve", "choices": ["향상시키다", "버리다", "잃다", "기다리다"], "answer": "향상시키다"},
        {"word": "discover", "choices": ["발견하다", "사다", "읽다", "질문하다"], "answer": "발견하다"},
        {"word": "protect", "choices": ["보호하다", "기억하다", "이동하다", "포기하다"], "answer": "보호하다"},
        {"word": "suddenly", "choices": ["갑자기", "매일", "혼자서", "천천히"], "answer": "갑자기"},
        {"word": "introduce", "choices": ["소개하다", "공부하다", "생각하다", "지우다"], "answer": "소개하다"},
    ],
    "어려움": [
        {"word": "responsible", "choices": ["책임감 있는", "무심한", "불안한", "아쉬운"], "answer": "책임감 있는"},
        {"word": "opportunity", "choices": ["기회", "실수", "자원", "피로"], "answer": "기회"},
        {"word": "convenient", "choices": ["편리한", "어려운", "귀한", "복잡한"], "answer": "편리한"},
        {"word": "maintain", "choices": ["유지하다", "포기하다", "감사하다", "배우다"], "answer": "유지하다"},
        {"word": "evidence", "choices": ["증거", "기억", "감정", "행동"], "answer": "증거"},
    ],
}


def get_shuffled_choices(question):
    choices = list(question["choices"])
    if question["answer"] not in choices:
        choices.append(question["answer"])
    random.shuffle(choices)
    return choices


def reset_game():
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.show_answer = False
    st.session_state.correct = False
    st.session_state.finished = False
    st.session_state.question_choices = {}


if "difficulty" not in st.session_state:
    st.session_state.difficulty = None

if "current_index" not in st.session_state:
    reset_game()


difficulty_options = list(QUIZ_DATA.keys())
current_difficulty = st.session_state.difficulty
selected_difficulty = st.sidebar.selectbox(
    "난이도를 선택하세요",
    difficulty_options,
    index=difficulty_options.index(current_difficulty) if current_difficulty in difficulty_options else 0,
)

if st.sidebar.button("새 게임 시작"):
    st.session_state.difficulty = selected_difficulty
    reset_game()

if st.session_state.difficulty != selected_difficulty:
    st.session_state.difficulty = selected_difficulty
    reset_game()

if st.session_state.difficulty is None:
    st.info("난이도를 선택하면 게임이 시작됩니다.")
    st.stop()

questions = QUIZ_DATA[st.session_state.difficulty]
current_question = questions[st.session_state.current_index]

if "question_choices" not in st.session_state:
    st.session_state.question_choices = {}

if st.session_state.current_index not in st.session_state.question_choices:
    st.session_state.question_choices[st.session_state.current_index] = get_shuffled_choices(current_question)

current_choices = st.session_state.question_choices[st.session_state.current_index]

st.sidebar.markdown("### 난이도 안내")
if st.session_state.difficulty == "쉬움":
    st.sidebar.write("기초 단어 위주로 익히기 좋은 난이도입니다.")
elif st.session_state.difficulty == "보통":
    st.sidebar.write("중학생 수준의 일반적인 단어를 다룹니다.")
else:
    st.sidebar.write("좀 더 어려운 단어와 뜻을 묻는 도전형 문제입니다.")

st.progress((st.session_state.current_index + 1) / len(questions))
st.caption(f"{st.session_state.difficulty} 난이도 · {st.session_state.current_index + 1}/{len(questions)}")

if st.session_state.finished:
    st.success(f"게임이 끝났습니다! 최종 점수는 {st.session_state.score}/{len(questions)}점입니다.")
    if st.button("다시 도전하기"):
        reset_game()
        st.rerun()
else:
    st.subheader(f"{current_question['word']}의 뜻은?")

    if st.session_state.show_answer:
        if st.session_state.correct:
            st.success("정답입니다!")
        else:
            st.error(f"오답입니다. 정답은 {current_question['answer']}입니다.")

        if st.session_state.current_index < len(questions) - 1:
            if st.button("다음 문제"):
                st.session_state.current_index += 1
                st.session_state.show_answer = False
                st.session_state.correct = False
                st.rerun()
        else:
            if st.button("결과 보기"):
                st.session_state.finished = True
                st.session_state.show_answer = False
                st.rerun()
    else:
        selected_answer = st.radio("뜻을 선택하세요", current_choices)

        if st.button("정답 확인"):
            st.session_state.show_answer = True
            if selected_answer == current_question["answer"]:
                st.session_state.score += 1
                st.session_state.correct = True
            else:
                st.session_state.correct = False
            st.rerun()

st.write("")
st.write(f"현재 점수: {st.session_state.score}/{len(questions)}")
