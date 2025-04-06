import streamlit as st
import pandas as pd
from utils.session_manager import login_user

def show_login_page():
    """
    로그인 페이지 UI를 표시하는 함수
    """
    st.title("📚 학원 자동 첨삭 시스템")
    st.subheader("로그인")
    
    # 로그인 폼
    with st.form("login_form"):
        username = st.text_input("아이디")
        password = st.text_input("비밀번호", type="password")
        show_demo = st.checkbox("기본 계정 정보 보기")
        submit_button = st.form_submit_button("로그인")
    
    # 기본 계정 정보 표시
    if show_demo:
        st.info("""
        ## 기본 계정 정보
        - 관리자: admin / admin123
        - 학생 1: student1 / student123
        - 학생 2: student2 / student123
        - 학생 3: student3 / student123
        """)
    
    # 로그인 버튼 처리
    if submit_button:
        if not username or not password:
            st.error("아이디와 비밀번호를 모두 입력해주세요.")
            return
        
        # 로그인 처리
        login_success, user_info = login_user(username, password)
        
        if login_success:
            st.success(f"{user_info['이름']}님 환영합니다!")
            
            # 세션에 사용자 정보 저장
            st.session_state.user_info = user_info
            st.session_state.logged_in = True
            
            # 학생인 경우 문제 풀기 페이지로 이동
            if user_info["역할"] == "학생":
                st.session_state.current_page = "quiz"
                st.rerun()
            # 관리자인 경우 관리자 페이지로 이동 (향후 구현)
            else:
                st.session_state.current_page = "quiz"  # 임시로 문제 페이지로 이동
                st.rerun()
        else:
            st.error("아이디 또는 비밀번호가 올바르지 않습니다.") 