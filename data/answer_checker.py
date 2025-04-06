import pandas as pd
import re
import datetime
from sheets.sheets_api import save_student_answer

def check_answer(problem, student_answer, student_info):
    """
    제출된 답안을 채점하고 피드백을 생성하는 함수
    
    problem: 문제 데이터 딕셔너리
    student_answer: 학생이 제출한 답안 (문자열)
    student_info: 학생 정보 딕셔너리 {학생ID, 이름, 학년}
    
    return: 채점 결과 딕셔너리
    """
    # 채점 결과 기본 구조
    result = {
        "학생ID": student_info.get("학생ID", ""),
        "이름": student_info.get("이름", ""),
        "학년": student_info.get("학년", ""),
        "문제ID": problem.get("문제ID", ""),
        "제출답안": student_answer,
        "점수": 0,
        "피드백": "",
        "제출시간": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 문제 유형에 따른 채점 로직
    problem_type = problem.get("유형", "")
    correct_answer = problem.get("정답", "")
    
    if not correct_answer:
        result["피드백"] = "문제에 정답이 설정되어 있지 않습니다."
        return result
    
    # 객관식 문제 채점
    if problem_type == "객관식":
        if student_answer.strip().upper() == correct_answer.strip().upper():
            result["점수"] = 100
            result["피드백"] = "정답입니다!"
        else:
            result["점수"] = 0
            result["피드백"] = f"오답입니다. 정답은 {correct_answer}입니다."
    
    # 주관식 문제 채점 (정확한 일치 검사)
    elif problem_type == "주관식":
        # 공백, 대소문자 무시하고 비교
        cleaned_student = re.sub(r'\s+', '', student_answer.lower())
        cleaned_correct = re.sub(r'\s+', '', correct_answer.lower())
        
        if cleaned_student == cleaned_correct:
            result["점수"] = 100
            result["피드백"] = "정답입니다!"
        else:
            # 부분 점수 계산 (간단한 구현으로, 정확도에 따라 향후 개선 가능)
            # 현재는 절반 이상 일치하면 50점 부여
            similarity = calculate_similarity(cleaned_student, cleaned_correct)
            
            if similarity >= 0.8:
                result["점수"] = 80
                result["피드백"] = f"거의 정답입니다! 정확한 답변은 '{correct_answer}'입니다."
            elif similarity >= 0.5:
                result["점수"] = 50
                result["피드백"] = f"부분 정답입니다. 정확한 답변은 '{correct_answer}'입니다."
            else:
                result["점수"] = 0
                result["피드백"] = f"오답입니다. 정답은 '{correct_answer}'입니다."
    
    # 해당 유형이 없는 경우
    else:
        result["피드백"] = f"지원하지 않는 문제 유형입니다: {problem_type}"
    
    # 해설 추가 (구글 시트에 해설 열이 있는 경우)
    if "해설" in problem and problem["해설"]:
        result["피드백"] += f"\n\n[해설] {problem['해설']}"
    
    # 결과 저장
    save_student_answer(result)
    
    return result

def calculate_similarity(str1, str2):
    """
    두 문자열의 유사도를 계산하는 함수 (간단한 구현)
    0.0 ~ 1.0 사이의 값 반환 (1.0이 완전 일치)
    """
    if not str1 or not str2:
        return 0.0
    
    # 공통 문자 수 계산 (순서 무시)
    str1_set = set(str1)
    str2_set = set(str2)
    common_chars = str1_set.intersection(str2_set)
    
    # 유사도 계산 (Jaccard 유사도와 유사)
    similarity = len(common_chars) / max(len(str1_set), len(str2_set))
    
    return similarity 