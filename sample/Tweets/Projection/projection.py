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
    config = ConfigParser()
    config.read("/home/pi/test/settings.ini")
    # config.read("E:\\Projects\\sigma\\PyhonAnomaly\\sample\\settings.ini")
    resource_folder_path = config['resources']['tweets']

    db_conf = config['postgresql']
    db_name = db_conf['database']
    db_username = db_conf['username']
    db_password = db_conf['password']
    db_host = db_conf['host']

    spark = SparkSession.builder \
        .getOrCreate()

    main()
