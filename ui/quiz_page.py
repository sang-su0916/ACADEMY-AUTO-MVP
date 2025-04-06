import streamlit as st
import pandas as pd
from data.problems_loader import get_random_problems, get_problem_by_id
from data.answer_checker import check_answer

def show_quiz_page():
    """
    문제 풀기 페이지 UI를 표시하는 함수
    """
    # 로그인 상태 확인
    if not st.session_state.get("logged_in", False):
        st.warning("로그인이 필요합니다.")
        st.session_state.current_page = "login"
        st.rerun()
        return
    
    # 사용자 정보 가져오기
    user_info = st.session_state.user_info
    
    st.title("📝 영어 문제 풀기")
    st.write(f"안녕하세요, {user_info['이름']}님!")
    
    # 로그아웃 버튼
    if st.sidebar.button("로그아웃"):
        from utils.session_manager import logout_user
        logout_user()
        st.rerun()
        return
    
    # 새로운 문제 가져오기
    if "current_problems" not in st.session_state or not st.session_state.current_problems:
        st.session_state.current_problems = get_random_problems(count=5)
        st.session_state.submitted_answers = {}
        st.session_state.current_problem_index = 0
    
    # 문제가 없는 경우
    if not st.session_state.current_problems:
        st.error("문제를 불러올 수 없습니다. 구글 시트 연결을 확인해주세요.")
        if st.button("다시 시도"):
            st.session_state.pop("current_problems", None)
            st.rerun()
        return
    
    # 현재 문제 인덱스
    current_idx = st.session_state.get("current_problem_index", 0)
    
    # 현재 문제
    if 0 <= current_idx < len(st.session_state.current_problems):
        current_problem = st.session_state.current_problems[current_idx]
        show_problem(current_problem, current_idx + 1, len(st.session_state.current_problems))
    else:
        st.error("문제 인덱스가 범위를 벗어났습니다.")
        if st.button("처음으로"):
            st.session_state.current_problem_index = 0
            st.rerun()

def show_problem(problem, problem_number, total_problems):
    """
    개별 문제를 표시하는 함수
    
    problem: 문제 데이터 딕셔너리
    problem_number: 현재 문제 번호
    total_problems: 전체 문제 수
    """
    st.subheader(f"문제 {problem_number}/{total_problems}")
    
    # 문제 정보 표시
    problem_id = problem.get("문제ID", "")
    problem_type = problem.get("유형", "")
    problem_level = problem.get("난이도", "")
    
    # 문제 내용 표시
    st.markdown(f"**{problem.get('문제내용', '')}**")
    
    # 객관식 문제
    if problem_type == "객관식":
        # 보기 추출 (보기1, 보기2, 보기3, 보기4, 보기5 열이 있다고 가정)
        options = []
        for i in range(1, 6):
            option_key = f"보기{i}"
            if option_key in problem and problem[option_key]:
                options.append(problem[option_key])
        
        # 라디오 버튼으로 보기 표시
        answer_key = f"answer_{problem_id}"
        student_answer = st.radio("답을 선택하세요:", options, key=answer_key)
        
        # 제출 버튼
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("제출하기", key=f"submit_{problem_id}"):
                # 학생 정보 준비
                student_info = {
                    "학생ID": st.session_state.user_info.get("학생ID", ""),
                    "이름": st.session_state.user_info.get("이름", ""),
                    "학년": st.session_state.user_info.get("학년", "")
                }
                
                # 채점 처리
                result = check_answer(problem, student_answer, student_info)
                
                # 결과 저장
                st.session_state.submitted_answers[problem_id] = student_answer
                st.session_state.grading_results[problem_id] = result
                
                # 결과 페이지로 이동
                st.session_state.current_page = "result"
                st.rerun()
    
    # 주관식 문제
    elif problem_type == "주관식":
        # 텍스트 입력으로 답안 입력
        answer_key = f"answer_{problem_id}"
        student_answer = st.text_input("답을 입력하세요:", key=answer_key)
        
        # 제출 버튼
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("제출하기", key=f"submit_{problem_id}"):
                if not student_answer.strip():
                    st.warning("답을 입력해주세요.")
                    return
                
                # 학생 정보 준비
                student_info = {
                    "학생ID": st.session_state.user_info.get("학생ID", ""),
                    "이름": st.session_state.user_info.get("이름", ""),
                    "학년": st.session_state.user_info.get("학년", "")
                }
                
                # 채점 처리
                result = check_answer(problem, student_answer, student_info)
                
                # 결과 저장
                st.session_state.submitted_answers[problem_id] = student_answer
                st.session_state.grading_results[problem_id] = result
                
                # 결과 페이지로 이동
                st.session_state.current_page = "result"
                st.rerun()
    
    # 다음/이전 문제 버튼
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.current_problem_index > 0:
            if st.button("이전 문제"):
                st.session_state.current_problem_index -= 1
                st.rerun()
    
    with col2:
        if st.session_state.current_problem_index < total_problems - 1:
            if st.button("다음 문제"):
                st.session_state.current_problem_index += 1
                st.rerun() 