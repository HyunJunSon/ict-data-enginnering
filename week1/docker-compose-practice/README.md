# 1주차 산출물 — Docker Compose 기반 통합 엔지니어링 환경

## 구성
- db: PostgreSQL 16 (포트 5432, 볼륨 pgdata로 데이터 보존)
- admin: pgAdmin 4 (http://localhost:8081)
- app: 자체 빌드 파이썬 앱 (./app의 Dockerfile)

## 실행 방법
1. docker compose up -d --build
2. docker compose ps로 상태 확인
3. 종료는 docker compose down

## 접속 정보
- pgAdmin: admin@example.com / admin123
- DB: 호스트 db(내부) 또는 localhost:5432(외부), engineer / engineer123, DB명 pipeline

## 확인한 것
- pgAdmin에서 호스트 이름을 db로 지정해 연결 성공
- docker compose down 후 up 해도 week1 표가 유지됨 (볼륨 동작 확인)

## 겪은 문제와 해결
- 딱히 없음
