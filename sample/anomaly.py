import re

from pyspark.sql import SparkSession


def main():
    spark = SparkSession.builder.master('spark://localhost:7077').getOrCreate()
    rdd = spark.read.format('orc').load("test2")

    def process_string(x):
        return re.sub("[^А-Яа-я\\w]", " ", x.__getitem__('value').lower())

    rdd = rdd.rdd.map(process_string) \
        .flatMap(lambda x: re.split("\\s+", x)) \
        .map(lambda x: (x, 1)) \
        .reduceByKey(lambda x, y: (x + y)) \
        .sortBy(lambda x: x[1])

    rdd.toDF().coalesce(1).write.mode("overwrite").csv("result.csv")
