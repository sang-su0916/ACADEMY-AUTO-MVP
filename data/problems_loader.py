import pandas as pd
import streamlit as st
from sheets.sheets_api import get_problems

def load_problems():
    """
    구글 시트에서 문제 데이터를 가져와 처리하는 함수
    """
    # 문제 데이터 로드
    problems_df = get_problems()
    
    if problems_df.empty:
        st.error("문제를 불러올 수 없습니다. 구글 시트 연결을 확인해주세요.")
        return None
    
    # 필요한 열이 있는지 검증
    required_columns = ["문제ID", "유형", "난이도", "문제내용"]
    missing_columns = [col for col in required_columns if col not in problems_df.columns]
    
    if missing_columns:
        st.error(f"구글 시트에 필요한 열이 없습니다: {', '.join(missing_columns)}")
        return None
    
    return problems_df

def get_problem_by_id(problem_id):
    """
    문제 ID로 특정 문제를 가져오는 함수
    """
    problems_df = load_problems()
    
    if problems_df is None:
        return None
    
    # 문제 ID로 필터링
    problem = problems_df[problems_df["문제ID"] == problem_id]
    
    if problem.empty:
        st.error(f"ID가 {problem_id}인 문제를 찾을 수 없습니다.")
        return None
    
    return problem.iloc[0].to_dict()

def get_random_problems(count=5, level=None, problem_type=None):
    """
    필터 조건에 맞는 랜덤 문제를 가져오는 함수
    
    count: 가져올 문제 수
    level: 난이도 필터 (상/중/하)
    problem_type: 문제 유형 필터 (객관식/주관식)
    """
    problems_df = load_problems()
    
    if problems_df is None:
        return []
    
    # 난이도 필터 적용
    if level:
        problems_df = problems_df[problems_df["난이도"] == level]
    
    # 유형 필터 적용
    if problem_type:
        problems_df = problems_df[problems_df["유형"] == problem_type]
    
    # 결과가 없으면 빈 리스트 반환
    if problems_df.empty:
        return []
    
    # count 개수만큼 랜덤 선택 (count가 전체 개수보다 크면 모두 반환)
    sample_count = min(count, len(problems_df))
    random_problems = problems_df.sample(n=sample_count)
    
    return random_problems.to_dict('records') 