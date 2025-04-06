import streamlit as st
import pandas as pd
import hashlib

# 기본 계정 정보 (실제 서비스에서는 DB에서 관리하는 것이 좋음)
DEFAULT_USERS = [
    {
        "아이디": "admin",
        "비밀번호": "admin123",  # 실제로는 해시화된 값 저장
        "이름": "관리자",
        "역할": "관리자",
        "학생ID": "",
        "학년": ""
    },
    {
        "아이디": "student1",
        "비밀번호": "student123",
        "이름": "홍길동",
        "역할": "학생",
        "학생ID": "S001",
        "학년": "중1"
    },
    {
        "아이디": "student2",
        "비밀번호": "student123",
        "이름": "김철수",
        "역할": "학생",
        "학생ID": "S002",
        "학년": "중2"
    },
    {
        "아이디": "student3",
        "비밀번호": "student123",
        "이름": "이영희",
        "역할": "학생",
        "학생ID": "S003",
        "학년": "중3"
    }
]

def init_session():
    """
    세션 초기화 함수
    """
    # 로그인 상태 초기화
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    # 사용자 정보 초기화
    if "user_info" not in st.session_state:
        st.session_state.user_info = None
    
    # 현재 문제 초기화
    if "current_problems" not in st.session_state:
        st.session_state.current_problems = []
    
    # 제출 답안 초기화
    if "submitted_answers" not in st.session_state:
        st.session_state.submitted_answers = {}
    
    # 채점 결과 초기화
    if "grading_results" not in st.session_state:
        st.session_state.grading_results = {}

def login_user(username, password):
    """
    사용자 로그인 처리 함수
    
    username: 사용자 아이디
    password: 비밀번호
    
    return: (로그인 성공 여부, 사용자 정보)
    """
    # 입력값 검증
    if not username or not password:
        return False, None
    
    # 사용자 정보 검색
    for user in DEFAULT_USERS:
        if user["아이디"] == username and user["비밀번호"] == password:
            return True, user
    
    return False, None

def logout_user():
    """
    로그아웃 처리 함수
    """
    st.session_state.logged_in = False
    st.session_state.user_info = None
    st.session_state.current_page = "login"
    st.session_state.current_problems = []
    st.session_state.submitted_answers = {}
    st.session_state.grading_results = {} 