import io
from configparser import ConfigParser

import psycopg2
from pyspark.sql import SparkSession


def main():
    conn = psycopg2.connect(dbname=db_name, user=db_username,
                            password=db_password, host=db_host)
    cursor = conn.cursor()

    tweet_view = "CREATE OR REPLACE VIEW managers_view AS " \
                 "SELECT created_at, tweet, user_name, city, country, state, continent " \
                 "FROM tweets"
    cursor.execute(tweet_view)

    youtube_view = "CREATE OR REPLACE VIEW youtube_view AS " \
                   "SELECT \"publishedAt\", \"channelTitle\", description, title " \
                   "FROM youtube"
    cursor.execute(youtube_view)

    conn.commit()
    cursor.close()


if __name__ == "__main__":
    spark = SparkSession.builder \
        .getOrCreate()
    sc = spark.sparkContext

    config_list = sc.textFile("s3://project.tweet.functions/resources/settings.ini").collect()
    buf = io.StringIO("\n".join(config_list))

    config = ConfigParser()
    config.read_file(buf)

    db_conf = config['postgresql']

    db_username = db_conf['username']
    db_password = db_conf['password']
    db_name = db_conf['database_rds']
    db_host = db_conf['host_rds']

    main()
