from configparser import ConfigParser

import psycopg2
from psycopg2 import sql
from pyspark.sql import functions as func, SparkSession, DataFrame


def process_tweet_data(dataframe):
    return dataframe.filter(dataframe.tweet.isNotNull()) \
        .filter(dataframe.created_at.like("2020-%-%")) \
        .withColumn("created_at", func.substring(dataframe.created_at, 0, 10)) \
        .distinct()


def process_youtube_data(dataframe):
    return dataframe.withColumn("publishedAt", func.to_date("publishedAt"))


def clean_data(dataframe):
    return dataframe.filter(
        lambda df:
            spark.read.jdbc(
                url=db_url,
                table=f"(SELECT * FROM tweets WHERE tweet_id LIKE cast({df['tweet_id'].__getitem__('value')} as varchar(255))) as my_table",
                properties=db_properties
            ).count() == 0
    )


def read_dataframe_from_table(table):
    return spark.read.jdbc(
        url=db_url,
        table=table,
        properties=db_properties
    )


def write_dataframe_to_table(df: DataFrame, table):
    df.write.jdbc(
        url=db_url,
        table=table,
        properties=db_properties,
        mode='append'
    )


def clear_table(table):
    conn = psycopg2.connect(dbname=db_name, user=db_username,
                            password=db_password, host=db_host)
    cursor = conn.cursor()

    clear_query = sql.SQL("DELETE FROM {table}").format(
        table=sql.Identifier(table)
    )
    cursor.execute(clear_query)

    conn.commit()
    cursor.close()


def load_tweet_data():
    table_name = "tweet_staging"
    staged_tweet_data = read_dataframe_from_table(table_name)
    processed_tweet_data = process_tweet_data(staged_tweet_data)
    write_dataframe_to_table(processed_tweet_data, 'tweets')
    clear_table(table_name)


def load_youtube_data():
    table_name = "youtube_staging"
    staged_youtube_data = read_dataframe_from_table(table_name)
    processed_youtube_data = process_youtube_data(staged_youtube_data)
    write_dataframe_to_table(processed_youtube_data, 'youtube')
    clear_table(table_name)

def main():
    load_tweet_data()
    load_youtube_data()


if __name__ == "__main__":
    config = ConfigParser()
    config.read("/home/pi/test/settings.ini")
    # config.read("E:\\Projects\\sigma\\PyhonAnomaly\\sample\\settings.ini")
    resource_folder_path = config['resources']['tweets']

    db_conf = config['postgresql']
    db_url = db_conf['url']
    db_properties = {'user': db_conf['username'], 'password': db_conf['password'], 'driver': db_conf['driver']}
    db_name = db_conf['database']
    db_username = db_conf['username']
    db_password = db_conf['password']
    db_host = db_conf['host']

    spark = SparkSession.builder \
        .getOrCreate()

    main()
