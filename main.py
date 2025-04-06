import streamlit as st
import os
import sys

# 상위 디렉토리 import를 위한 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 로컬 모듈 import
from ui.login import show_login_page
from ui.quiz_page import show_quiz_page
from ui.result_page import show_result_page
from utils.session_manager import init_session

def main():
    # 세션 초기화
    init_session()
    
    # 현재 페이지 상태 확인
    if "current_page" not in st.session_state:
        st.session_state.current_page = "login"
    
    # 페이지 라우팅
    if st.session_state.current_page == "login":
        show_login_page()
    elif st.session_state.current_page == "quiz":
        show_quiz_page()
    elif st.session_state.current_page == "result":
        show_result_page()

if __name__ == "__main__":
    st.set_page_config(
        page_title="학원 자동 첨삭 시스템",
        page_icon="✏️",
        layout="wide"
    )
    main() 