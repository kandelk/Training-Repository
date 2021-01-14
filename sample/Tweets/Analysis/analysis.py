from configparser import ConfigParser

from pyspark.sql import functions as func, SparkSession
from pyspark.sql.functions import col

from sample.Tweets.Utils.plot_utils import *


def main():
    tweets_view = spark.read.jdbc(
        url=db_url,
        table='managers_view',
        properties=db_properties
    )

    count_by_date_list = tweets_view\
        .groupBy(func.col("created_at"))\
        .count()\
        .sort(col("created_at").asc())\
        .collect()

    counts_list = [int(row['count']) for row in count_by_date_list]
    dates_list = [row['created_at'] for row in count_by_date_list]

    create_and_save_hbar(counts_list, dates_list, config['resources']['folder'])


if __name__ == "__main__":
    config = ConfigParser()
    config.read('/home/pi/test/settings.ini')

    db_conf = config['postgresql']
    db_url = db_conf['url']
    db_properties = {'user': db_conf['username'], 'password': db_conf['password'], 'driver': db_conf['driver']}

    spark = SparkSession.builder \
        .getOrCreate()

    main()
