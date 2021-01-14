import psycopg2
from datetime import datetime
from configparser import ConfigParser
import io

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import *
import boto3


def get_files_to_load(type_to_load, last_load_timestamp):
    files_to_load = []
    last_loaded_hour = str(last_load_timestamp.time().hour)
    last_loaded_date = str(last_load_timestamp.date())

    db = boto3.client('dynamodb')

    partitions_items_from_db = db.query(
        TableName='Project-tweet-date',
        KeyConditionExpression='metadata = :mt AND load_date > :load_date',
        ExpressionAttributeValues={
            ':load_date': {'S': f"{last_loaded_date} {last_loaded_hour}"},
            ':mt': {'S': type_to_load}
        }
    )

    partitions_to_load = list(map(lambda item: item['path']['S'], partitions_items_from_db['Items']))

    for partition in partitions_to_load:

        files_items_from_db = db.query(
            TableName='Project-tweet-path',
            KeyConditionExpression='#pk = :bucket',
            ExpressionAttributeValues={
                ':bucket': {'S': partition}
            },
            ExpressionAttributeNames={
                "#pk": "bucket"
            }
        )
        files_from_db = list(map(lambda item: f"{item['bucket']['S']}{item['file']['S']}", files_items_from_db['Items']))
        files_to_load.extend(files_from_db)

    return files_to_load


def load_csv_df_from_s3(file):
    read_file_df = spark.read.format('csv') \
        .option("delimiter", csv_conf['delimiter']) \
        .option("header", csv_conf['header']) \
        .option("inferSchema", csv_conf['inferSchema']) \
        .load(f"s3://{file}")

    return read_file_df


def load_json_df_from_s3(file):
    read_df = spark.read.json(path=f"s3://{file}", multiLine=True)
    return read_df


def extract_data_from_json(df: DataFrame):
    return df \
        .select(explode("items").alias("items")) \
        .select("items.id.*", "items.snippet.*") \
        .select("videoId", "channelId", "channelTitle", "description", "publishedAt", "title")


def write_df_to_table(dataframe, table):
    dataframe.write.jdbc(
        url=db_url,
        table=table,
        properties=db_properties,
        mode='append'
    )


def extract_tweet_data(last_load_timestamp):
    files_to_load = get_files_to_load('tweet', last_load_timestamp)

    for file in files_to_load:
        loaded_dataframe = load_csv_df_from_s3(file)
        write_df_to_table(loaded_dataframe, "tweet_staging")

def extract_youtube_data(last_load_timestamp):
    files_to_load = get_files_to_load('youtube', last_load_timestamp)

    for file in files_to_load:
        loaded_youtube_dataframe = load_json_df_from_s3(file)
        extracted_dataframe = extract_data_from_json(loaded_youtube_dataframe)
        write_df_to_table(extracted_dataframe, "youtube_staging")


def main():
    conn = psycopg2.connect(dbname=db_name, user=db_properties['user'],
                            password=db_properties['password'], host=db_host)
    cursor = conn.cursor()

    sync_table_exists_query = "SELECT EXISTS (" \
                              "SELECT FROM information_schema.tables " \
                              "WHERE  table_schema = 'public' AND table_name = 'sync');"
    cursor.execute(sync_table_exists_query)
    is_sync_exists = cursor.fetchone()[0]

    if is_sync_exists:
        cursor.execute("SELECT MAX(last_load) FROM sync")
        last_load_timestamp = cursor.fetchone()[0]
    else:
        cursor.execute("CREATE TABLE IF NOT EXISTS sync (last_load timestamp)")
        last_load_timestamp = datetime(2021, 1, 1)

    extract_tweet_data(last_load_timestamp)
    extract_youtube_data(last_load_timestamp)

    cursor.execute("INSERT INTO sync VALUES (current_timestamp)")
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

    db_url = db_conf['url_rds']
    db_properties = {'user': db_conf['username'], 'password': db_conf['password'], 'driver': db_conf['driver']}

    db_name = db_conf['database_rds']
    db_host = db_conf['host_rds']

    csv_conf = config['csv']

    main()
