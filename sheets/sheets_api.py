import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import streamlit as st

# Google Sheets API 범위 및 인증 정보
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# 구글 시트 ID (PRD에서 언급된 시트 ID)
SHEET_ID = "1ke4Sv6TjOBua-hm-PLayMFHubA1mcJCrg0VVTJzf2d0"

def connect_to_google_sheets():
    """
    Google Sheets API에 연결하는 함수
    첫 사용 시에는 credentials.json 파일이 필요합니다.
    """
    try:
        # Streamlit Cloud에서는 secrets 사용
        if hasattr(st, 'secrets') and 'google_sheets' in st.secrets:
            credentials = Credentials.from_service_account_info(
                st.secrets["google_sheets"],
                scopes=SCOPE
            )
        # 로컬에서는 credentials 파일 사용
        else:
            credentials = Credentials.from_service_account_file(
                "credentials.json",
                scopes=SCOPE
            )
            
        client = gspread.authorize(credentials)
        sheet = client.open_by_key(SHEET_ID)
        return sheet
    
    except Exception as e:
        st.error(f"구글 시트 연결 중 오류가 발생했습니다: {e}")
        return None

def get_problems():
    """
    구글 시트에서 문제 데이터를 가져오는 함수
    """
    sheet = connect_to_google_sheets()
    if not sheet:
        return pd.DataFrame()
    
    try:
        # 'problems' 탭에서 데이터 가져오기
        problems_sheet = sheet.worksheet("problems")
        data = problems_sheet.get_all_records()
        return pd.DataFrame(data)
    
    except Exception as e:
        st.error(f"문제 데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return pd.DataFrame()

def save_student_answer(answer_data):
    """
    학생 답안을 구글 시트에 저장하는 함수
    
    answer_data: 딕셔너리 형태의 답안 데이터
    {
        "학생ID": str,
        "이름": str,
        "학년": str,
        "문제ID": str,
        "제출답안": str,
        "점수": int,
        "피드백": str,
        "제출시간": str
    }
    """
    sheet = connect_to_google_sheets()
    if not sheet:
        return False
    
    try:
        # 'student_answers' 탭에 데이터 추가
        answers_sheet = sheet.worksheet("student_answers")
        answers_sheet.append_row([
            answer_data.get("학생ID", ""),
            answer_data.get("이름", ""),
            answer_data.get("학년", ""),
            answer_data.get("문제ID", ""),
            answer_data.get("제출답안", ""),
            answer_data.get("점수", 0),
            answer_data.get("피드백", ""),
            answer_data.get("제출시간", "")
        ])
        return True
    
    except Exception as e:
        st.error(f"답안을 저장하는 중 오류가 발생했습니다: {e}")
        return False 