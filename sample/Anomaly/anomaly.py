import re
import configparser

from pyspark.sql import SparkSession


def process_file_with_anomaly():
    config = configparser.ConfigParser()
    config.read('settings.ini')

    spark = SparkSession.builder.master(config["Spark"]["remote"]).getOrCreate()
    rdd = spark.read.format('orc').load("E:\\Projects\\sigma\\PyhonAnomaly\\sample\\test2")

    def process_string(x):
        return re.sub("[^А-Яа-я\\w]", " ", x.__getitem__('value').lower())

    rdd = rdd.rdd.map(process_string) \
        .flatMap(lambda x: re.split("\\s+", x)) \
        .map(lambda x: (x, 1)) \
        .reduceByKey(lambda x, y: (x + y)) \
        .sortBy(lambda x: x[1])

    rdd.toDF().coalesce(1).write.mode("overwrite").csv("result.csv")
