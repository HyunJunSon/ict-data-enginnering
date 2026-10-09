# 2주차 산출물 — 쇼핑몰 ERD 설계 + 크롤링 파이프라인

## 1. ERD 설계서
- 파일: ERD_설계서.md (엔터티 정의 · 관계 · 정규화 근거 · 반정규화 결정)
- 표 4개: customers · products · orders · order_items
- N:M(주문↔상품)을 order_items 교차 표로 해소

## 2. 크롤러
- 대상: https://quotes.toscrape.com (수집 허용 확인 완료)
- 구조: fetch(수집) → parse(정제) → load(적재) 3함수 분리
- 예절: User-Agent 표기 · 요청 간격 1초 · robots.txt 사전 확인
- 중복 방지: quotes 표의 UNIQUE(author, quote_text) 제약 + INSERT IGNORE

## 3. 실행 방법
```
docker start de-mysql
python3 -m venv .venv && source .venv/bin/activate   # Windows(WSL2)·macOS·리눅스 모두 같습니다
pip install requests beautifulsoup4 pymysql
python3 check_robots.py       # 수집 가능 여부 확인
python3 crawler_pipeline.py   # 3페이지 수집·적재
```

## 4. 검증한 것
- 첫 실행: parsed 10 / saved 10 × 3페이지 = 30건
- 재실행: parsed 10 / saved 0 (DB 제약이 중복을 막음)
- SELECT COUNT(*) FROM quotes → 30

## 5. 남은 개선점
- tags를 쉼표 문자열로 저장 중 (1NF 위반) → quote_tags 교차 표로 분리 예정
- 페이지 수(3개)가 코드에 하드코딩되어 있어, "다음 페이지" 링크가 없을 때까지 자동 순회하도록 개선 필요
- 네트워크 오류 시 재시도·타임아웃 처리가 없어, requests에 timeout·retry(지수 백오프)를 추가하면 안정성이 올라감