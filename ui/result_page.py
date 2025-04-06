import streamlit as st
import pandas as pd
from utils.session_manager import logout_user

def show_result_page():
    """
    채점 결과를 표시하는 결과 페이지 UI
    """
    # 로그인 상태 확인
    if not st.session_state.get("logged_in", False):
        st.warning("로그인이 필요합니다.")
        st.session_state.current_page = "login"
        st.rerun()
        return
    
    # 채점 결과가 없는 경우
    if not st.session_state.get("grading_results", {}):
        st.warning("제출된 답안이 없습니다.")
        if st.button("문제 풀기로 돌아가기"):
            st.session_state.current_page = "quiz"
            st.rerun()
        return
    
    # 사용자 정보 가져오기
    user_info = st.session_state.user_info
    
    st.title("📊 채점 결과")
    st.write(f"{user_info['이름']}님의 답안이 채점되었습니다.")
    
    # 로그아웃 버튼
    if st.sidebar.button("로그아웃"):
        logout_user()
        st.rerun()
        return
    
    # 전체 결과 집계
    total_score = 0
    total_problems = len(st.session_state.grading_results)
    
    for result in st.session_state.grading_results.values():
        total_score += result.get("점수", 0)
    
    average_score = total_score / total_problems if total_problems > 0 else 0
    
    # 점수 표시
    st.subheader("종합 점수")
    st.metric("평균 점수", f"{average_score:.1f}점")
    
    # 각 문제별 결과 표시
    st.subheader("문제별 채점 결과")
    
    for problem_id, result in st.session_state.grading_results.items():
        with st.expander(f"문제 {problem_id} - {result.get('점수')}점"):
            # 문제 ID와 제출 답안 표시
            st.write(f"**제출 답안:** {result.get('제출답안', '')}")
            
            # 점수에 따른 결과 색상 설정
            score = result.get("점수", 0)
            if score >= 80:
                st.success(f"**점수:** {score}점")
            elif score >= 50:
                st.warning(f"**점수:** {score}점")
            else:
                st.error(f"**점수:** {score}점")
            
            # 피드백 표시
            st.write(f"**피드백:** {result.get('피드백', '')}")
    
    # 버튼 영역
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("새 문제 풀기"):
            # 세션에서 문제 데이터 초기화
            st.session_state.pop("current_problems", None)
            st.session_state.submitted_answers = {}
            st.session_state.grading_results = {}
            st.session_state.current_page = "quiz"
            st.rerun()
    
    with col2:
        if st.button("같은 문제 다시 풀기"):
            # 답안 및 결과만 초기화
            st.session_state.submitted_answers = {}
            st.session_state.grading_results = {}
            st.session_state.current_page = "quiz"
            st.rerun() 