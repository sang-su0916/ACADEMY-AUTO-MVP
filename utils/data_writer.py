import pandas as pd
import datetime
from sheets.sheets_api import save_student_answer

def save_result(user_info, problem, answer, score, feedback):
    """
    학생 답안 결과를 저장하는 함수
    
    user_info: 학생 정보 딕셔너리
    problem: 문제 데이터 딕셔너리
    answer: 학생 답안 (문자열)
    score: 점수 (정수)
    feedback: 피드백 (문자열)
    
    return: 저장 성공 여부 (Boolean)
    """
    # 저장할 데이터 준비
    data = {
        "학생ID": user_info.get("학생ID", ""),
        "이름": user_info.get("이름", ""),
        "학년": user_info.get("학년", ""),
        "문제ID": problem.get("문제ID", ""),
        "제출답안": answer,
        "점수": score,
        "피드백": feedback,
        "제출시간": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 구글 시트에 데이터 저장
    return save_student_answer(data)

def save_bulk_results(results):
    """
    여러 문제의 결과를 한 번에 저장하는 함수
    
    results: 결과 딕셔너리 리스트
    
    return: 성공한 저장 개수
    """
    success_count = 0
    
    for result in results:
        success = save_student_answer(result)
        if success:
            success_count += 1
    
    return success_count 