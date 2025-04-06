# 🧪 학원 자동 첨삭 시스템 테스트 가이드

## ⚙️ 테스트 준비

1. **Google Sheets API 사용 설정**
   - [Google Cloud Console](https://console.cloud.google.com/)에서 새 프로젝트 생성
   - Google Sheets API 활성화
   - 서비스 계정 생성 및 키(JSON) 다운로드
   - 다운로드한 키를 `credentials.json` 이름으로 `auto-check-app` 폴더에 저장

2. **구글 시트 공유 설정**
   - 구글 시트(`1ke4Sv6TjOBua-hm-PLayMFHubA1mcJCrg0VVTJzf2d0`)를 서비스 계정 이메일과 공유 (편집 권한)
   - 구글 시트에 'problems'와 'student_answers' 시트 탭이 존재하는지 확인

## 🧮 테스트 실행 방법

1. **앱 실행**
   ```bash
   cd auto-check-app
   streamlit run main.py
   ```

2. **로그인 테스트**
   - 기본 계정 사용: admin/admin123, student1/student123 등
   - 로그인 성공 시 문제 페이지로 이동하는지 확인

3. **문제 풀기 테스트**
   - 구글 시트에서 문제가 제대로 불러와지는지 확인
   - 객관식/주관식 UI가 제대로 렌더링되는지 확인
   - 문제 간 이동이 정상적으로 작동하는지 확인

4. **채점 테스트**
   - 답안 제출 후 자동 채점이 정확히 이루어지는지 확인
   - 채점 결과와 피드백이 올바르게 표시되는지 확인

5. **결과 저장 테스트**
   - 제출 후 구글 시트의 student_answers 탭에 데이터가 저장되었는지 확인
   - 저장된 데이터의 형식과 내용이 올바른지 확인

## 📋 테스트 체크리스트

- [ ] 로그인/로그아웃 기능
- [ ] 구글 시트에서 문제 불러오기
- [ ] 객관식 문제 UI 및 제출
- [ ] 주관식 문제 UI 및 제출
- [ ] 자동 채점 기능
- [ ] 결과 페이지 표시
- [ ] 구글 시트에 결과 저장

## 🛠️ 디버깅 팁

1. 구글 시트 연동 오류 발생 시:
   - `credentials.json` 파일 경로 확인
   - 서비스 계정에 구글 시트 공유 권한 확인
   - 구글 시트 ID가 `sheets_api.py`에 올바르게 설정되었는지 확인

2. 문제 불러오기 실패 시:
   - 구글 시트의 'problems' 탭 구조 확인
   - 필수 열(문제ID, 유형, 난이도, 문제내용, 정답) 확인

3. 결과 저장 실패 시:
   - 구글 시트의 'student_answers' 탭 존재 여부 확인
 