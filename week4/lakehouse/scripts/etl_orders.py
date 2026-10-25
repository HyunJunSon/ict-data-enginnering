# scripts/etl_orders.py — 랜딩 존 → 정제 → MERGE 적재
from pyspark.sql import SparkSession, Window
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("orders-etl").getOrCreate()

# 1) 랜딩 존(raw 버킷)에서 원천 읽기 (s3a)
raw = spark.read.option("header", "true").csv("s3a://raw/orders/")
print("원천 행:", raw.count())

# 2) 형 변환
typed = raw.select(
    F.col("order_id").cast("bigint").alias("order_id"),
    F.col("customer"),
    F.col("amount").cast("double").alias("amount"),
    F.to_date("order_date").alias("order_date"),
    F.col("channel"),
)

# 3) 정제: 불량 걸러내기 + 키별로 최신 한 행만 (결정적)
w = Window.partitionBy("order_id").orderBy(F.col("order_date").desc())
clean = (
    typed
    .filter("order_id IS NOT NULL AND amount >= 0")
    .withColumn("rn", F.row_number().over(w))
    .filter("rn = 1")
    .drop("rn")
)
print("정제 후 행:", clean.count())
clean.createOrReplaceTempView("updates")

# 4) 적재: 키가 있으면 갱신, 없으면 삽입 (멱등)
spark.sql("""
    MERGE INTO demo.lakehouse.orders AS t
    USING updates AS s
    ON t.order_id = s.order_id
    WHEN MATCHED THEN UPDATE SET *
    WHEN NOT MATCHED THEN INSERT *
""")

print("total rows:", spark.table("demo.lakehouse.orders").count())
spark.stop()
