import re

from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession.builder.master('local').appName("Anomaly").getOrCreate()
    rdd = spark.read.format('orc').load("E:\\Projects\\sigma\\FileAnomaly\\src\\main\\resources\\test2")

    def process_string(x):
        return re.sub("[^А-Яа-я\\w]", " ", x.__getitem__('value').lower())

    rdd = rdd.rdd.map(process_string)\
        .flatMap(lambda x: re.split("\\s+", x))\
        .map(lambda x: (x, 1))\
        .reduceByKey(lambda x, y: (x + y))\
        .sortBy(lambda x: x[1])

    rdd.toDF().coalesce(1).write.mode("overwrite").csv("result.csv")
