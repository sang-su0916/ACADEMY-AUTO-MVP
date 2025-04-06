import streamlit as st
import sys
import os

# 애플리케이션 경로 추가
app_dir = "auto-check-app"
if os.path.exists(app_dir):
    sys.path.append(os.path.abspath(app_dir))
    # main.py 직접 실행
    try:
        # auto-check-app 폴더의 main.py 모듈 import
        sys.path.insert(0, os.path.abspath(app_dir))
        from main import main
        
        st.set_page_config(
            page_title="학원 자동 첨삭 시스템",
            page_icon="✏️",
            layout="wide"
        )
        
        main()
        
    except ImportError as e:
        st.error(f"모듈을 불러오는 중 오류가 발생했습니다: {e}")
else:
    st.error(f"애플리케이션 폴더를 찾을 수 없습니다: {app_dir}")
    
    st.warning("""
    ## 설정 오류 발생
    
    애플리케이션 폴더를 찾을 수 없습니다. 다음 내용을 확인해주세요:
    
    1. GitHub 리포지토리 구조가 올바른지 확인
    2. requirements.txt의 종속성이 모두 설치되었는지 확인
    3. Google Sheets API 인증 정보가 올바르게 설정되었는지 확인
    
    자세한 설정 방법은 README.md 파일을 참고하세요.
    """) 