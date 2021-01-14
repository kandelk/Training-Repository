import io
from configparser import ConfigParser

from pyspark.sql import functions as func, SparkSession
from pyspark.sql.functions import col

from sample.Tweets.Utils.plot_utils import *


def get_dataframe_from_view(view):
    return spark.read.jdbc(
        url=db_url,
        table=view,
        properties=db_properties
    )


def analyze_tweets():
    tweets_view = get_dataframe_from_view('managers_view')

    count_by_date_list = tweets_view \
        .groupBy(func.col("created_at")) \
        .count() \
        .sort(col("created_at").asc()) \
        .collect()

    counts_list = [int(row['count']) for row in count_by_date_list]
    dates_list = [row['created_at'] for row in count_by_date_list]

    create_and_save_hbar(counts_list, dates_list, save_plot_folder, 'tweet')


def analyze_youtube_by_date():
    youtube_view = get_dataframe_from_view("youtube_view")

    count_by_date_list = youtube_view \
        .groupBy(func.col("publishedAt")) \
        .count() \
        .sort(col("publishedAt").asc()) \
        .collect()

    counts_list = [int(row['count']) for row in count_by_date_list]
    dates_list = [row['publishedAt'] for row in count_by_date_list]

    create_and_save_hbar(counts_list, dates_list, save_plot_folder, 'youtube-date')


def analyze_youtube_by_channel():
    youtube_view = get_dataframe_from_view("youtube_view")

    count_by_date_list = youtube_view \
        .groupBy(func.col("channelTitle")) \
        .count() \
        .sort(col("channelTitle").asc()) \
        .collect()

    counts_list = [int(row['count']) for row in count_by_date_list]
    dates_list = [row['channelTitle'] for row in count_by_date_list]

    create_and_save_hbar(counts_list, dates_list, save_plot_folder, 'youtube-channel')


def main():
    analyze_tweets()
    analyze_youtube_by_date()
    analyze_youtube_by_channel()

if __name__ == "__main__":
    spark = SparkSession.builder \
        .getOrCreate()
    sc = spark.sparkContext

    config_list = sc.textFile("s3://project.tweet.functions/resources/settings.ini").collect()
    buf = io.StringIO("\n".join(config_list))

    config = ConfigParser()
    config.read_file(buf)

    db_conf = config['postgresql']
    db_url = db_conf['url_rds']
    db_properties = {'user': db_conf['username'], 'password': db_conf['password'], 'driver': db_conf['driver']}

    save_plot_folder = config['s3']['plot_save_bucket']

    main()
