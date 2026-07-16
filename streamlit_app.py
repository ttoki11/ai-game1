import random

import streamlit as st

st.set_page_config(page_title="세븐틴 퀴즈", page_icon="🎤", layout="centered")

st.title("🎤 세븐틴 퀴즈")
st.write("난이도를 선택하고, 세븐틴 지식으로 퀴즈를 풀어보세요!")

QUIZ_DATA = {
    "쉬움": [
        {"question": "세븐틴의 공식 팬클럽 이름은 무엇인가요?", "choices": ["Carat", "Weverse", "Mingus", "Stay"], "answer": "Carat"},
        {"question": "세븐틴의 리더는 누구인가요?", "choices": ["에스쿱스", "호시", "디노", "버논"], "answer": "에스쿱스"},
        {"question": "세븐틴은 총 몇 명으로 이루어져 있나요?", "choices": ["11명", "13명", "10명", "14명"], "answer": "13명"},
        {"question": "세븐틴의 데뷔 앨범 제목은 무엇인가요?", "choices": ["17 Carat", "FML", "Face the Sun", "Attacca"], "answer": "17 Carat"},
    ],
    "보통": [
        {"question": "세븐틴의 첫 정규 앨범 제목은 무엇인가요?", "choices": ["Love & Letter", "Face the Sun", "Heng:garæ", "Seventeenth Heaven"], "answer": "Love & Letter"},
        {"question": "세븐틴의 메인댄서로 알려진 멤버는 누구인가요?", "choices": ["호시", "민규", "우지", "준"], "answer": "호시"},
        {"question": "세븐틴의 2023년 앨범 제목은 무엇인가요?", "choices": ["FML", "Seventeenth Heaven", "Heng:garæ", "17 Is Right Here"], "answer": "FML"},
        {"question": "세븐틴의 멤버 'The8'로 알려진 사람은 누구인가요?", "choices": ["디노", "민규", "명호", "호시"], "answer": "명호"},
    ],
    "어려움": [
        {"question": "세븐틴의 유닛 BSS를 이루는 멤버는 누구인가요?", "choices": ["호시, DK, 승관", "에스쿱스, 우지, 버논", "도겸, 승관, 명호", "호시, 디노, 민규"], "answer": "호시, DK, 승관"},
        {"question": "세븐틴의 2020년 정규 앨범 제목은 무엇인가요?", "choices": ["Heng:garæ", "Face the Sun", "Attacca", "FML"], "answer": "Heng:garæ"},
        {"question": "세븐틴의 2021년 미니 앨범 제목은 무엇인가요?", "choices": ["Attacca", "No Easy", "Seventeenth Heaven", "17 Is Right Here"], "answer": "Attacca"},
        {"question": "세븐틴이 2024년에 발매한 정규 앨범의 제목은 무엇인가요?", "choices": ["17 Is Right Here", "Seventeenth Heaven", "FML", "Happy Ending"], "answer": "17 Is Right Here"},
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
    st.sidebar.write("기초 세븐틴 지식 위주로 익히기 좋은 난이도입니다.")
elif st.session_state.difficulty == "보통":
    st.sidebar.write("멤버와 앨범 정보까지 포함된 중간 난이도입니다.")
else:
    st.sidebar.write("유닛과 활동 정보까지 묻는 도전형 문제입니다.")

st.progress((st.session_state.current_index + 1) / len(questions))
st.caption(f"{st.session_state.difficulty} 난이도 · {st.session_state.current_index + 1}/{len(questions)}")

if st.session_state.finished:
    st.success(f"퀴즈가 끝났습니다! 최종 점수는 {st.session_state.score}/{len(questions)}점입니다.")
    if st.button("다시 도전하기"):
        reset_game()
        st.rerun()
else:
    st.subheader(current_question["question"])

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
        selected_answer = st.radio("정답을 선택하세요", current_choices)

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
