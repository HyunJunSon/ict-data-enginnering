import duckdb
import pandas as pd
 
 
def load_raw() -> pd.DataFrame:
    # 추출 — 대용량이어도 여기서 필터·열 선택으로 줄일 수 있다
    return duckdb.sql("SELECT * FROM 'orders.csv'").df()
 
 
def clean(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out['category'] = out['category'].str.strip()          # 공백 오염 제거
    out['order_date'] = pd.to_datetime(out['order_date'])  # 타입 복원
    out = out.drop_duplicates(subset='order_id', keep='first')  # 중복 제거
    out['price'] = out['price'].fillna(out['price'].median())   # 결측 보정
    out['amount'] = out['price'] * out['quantity']         # 파생 컬럼
    return out

if __name__ == '__main__':
    raw = load_raw()
    cleaned = clean(raw)
    cleaned.to_parquet('orders_clean.parquet', index=False)
    print(len(raw), '행 ->', len(cleaned), '행 정제 완료')