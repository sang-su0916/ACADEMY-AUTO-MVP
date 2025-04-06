# 학원 자동 첨삭 시스템 MVP 개발 To-Do List

## 1. 초기 설정
- [x] 프로젝트 폴더 구조 생성
- [x] requirements.txt 작성 (streamlit, gspread, pandas 등)
- [x] GitHub 리포지토리 설정
- [x] Google Sheets API 연동 설정

## 2. 데이터 연동
- [x] 구글 시트 연결 기능 구현 (sheets_api.py)
- [x] 문제 불러오기 기능 구현 (problems_loader.py)
- [x] 학생 답안 저장 기능 구현 (data_writer.py)

## 3. 핵심 기능 개발
- [x] 로그인 기능 구현 (login.py)
- [x] 문제 풀기 UI 개발 (quiz_page.py)
  - [x] 객관식 문제 UI
  - [x] 주관식 문제 UI
- [x] 자동 채점 로직 구현 (answer_checker.py)
- [x] 첨삭 및 결과 화면 개발 (result_page.py)
- [x] 세션 관리 기능 구현 (session_manager.py)

## 4. UI/UX
- [x] 로그인 페이지 디자인
- [x] 문제 풀기 페이지 디자인
- [x] 결과 확인 페이지 디자인
- [x] 전체 앱 스타일링 및 UX 개선

## 5. 테스트
- [x] 로그인 기능 테스트
- [x] 문제 불러오기 테스트
- [x] 채점 및 첨삭 기능 테스트
- [x] 결과 저장 기능 테스트
- [x] 전체 플로우 통합 테스트

## 6. 배포
- [x] Streamlit Cloud 또는 로컬호스트 배포 설정
- [x] README.md 작성 (설치 및 사용 방법)

## 7. 우선순위 (PRD 강조사항)
- [x] **문제 불러오기** 기능
- [x] **문제풀기** UI/UX
- [x] **자동 채점** 기능
- [x] 결과 **Google Sheet 저장** 기능 