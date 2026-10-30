# first_job.py
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("first-cluster-job").getOrCreate()
df = spark.range(1, 1_000_001)
result = df.withColumn("double", df["id"] * 2).filter("double > 1000000").count()
print("count =", result)   # 500000
# 어느 익스큐터에서 돌았는지 확인
print("master:", spark.sparkContext.master)
print("executors:", spark.sparkContext._jsc.sc().getExecutorMemoryStatus().size())
spark.stop()
