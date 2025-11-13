# Q&A 데이터 준비 방법

이 폴더에는 Q&A.xlsx 파일이 필요합니다.

## 방법 1: CSV를 Excel로 변환 (권장)

제공된 `Q&A_sample.csv` 파일을 Excel로 변환:

1. Excel 또는 Google Sheets에서 `Q&A_sample.csv` 파일 열기
2. "다른 이름으로 저장" → Excel Workbook (.xlsx) 선택
3. 파일명을 `Q&A.xlsx`로 저장
4. 이 폴더에 배치

## 방법 2: 직접 생성

Excel에서 직접 생성:

### 컬럼 구조
| 순번 | 내  용 |
|------|--------|
| 1    | Q. ...<br>A. ... |
| 2    | Q. ...<br>A. ... |

### 데이터 형식
```
Q. Perso.ai는 어떤 서비스인가요?
A. Perso.ai는 이스트소프트가 개발한 다국어 AI 영상 더빙 플랫폼으로...
```

## 방법 3: Python 스크립트 사용

```python
import pandas as pd

# CSV 읽기
df = pd.read_csv('Q&A_sample.csv')

# Excel로 저장
df.to_excel('Q&A.xlsx', index=False)
```

## 주의사항

- 파일명은 반드시 `Q&A.xlsx`여야 합니다
- 컬럼명: "순번", "내  용" (띄어쓰기 2칸)
- 각 셀에는 "Q. ... A. ..." 형식으로 작성

## 테스트

데이터 파일이 준비되었다면:

```bash
# 백엔드 폴더에서
python scripts/preprocess_data.py
```

성공 메시지가 표시되면 데이터가 올바르게 준비된 것입니다.
