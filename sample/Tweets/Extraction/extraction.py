from configparser import ConfigParser
from datetime import date
from os import walk

import psycopg2
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import *


def get_files_in_folder(folder, timestamp):
    date_folders_to_load = []
    hour_folders_to_load = []
    last_loaded_hour = str(timestamp.time().hour)
    last_loaded_date = str(timestamp.date())

    # Find date folders to load
    for (dirpath, date_folders, filenames) in walk(f"{folder}"):
        for date_folder in date_folders:
            if date_folder >= str(timestamp.date()):
                date_folders_to_load.append(date_folder)
        break

    # Check date folders to find hour folders to load
    for date_folder in date_folders_to_load:

        for (dirpath, hour_folders, filenames) in walk(f"{folder}/{date_folder}"):

            if date_folder == last_loaded_date:
                for hour_folder in hour_folders:

                    if hour_folder > last_loaded_hour:
                        hour_folders_to_load.append(f"{date_folder}/{hour_folder}")

                break

            hour_folders_to_load.extend(list(map(lambda hour_dir: f"{date_folder}/{hour_dir}", hour_folders)))
            break

    return hour_folders_to_load


def load_csv_df_from_folder(folder):
    read_file_df = spark.read.format('csv') \
        .option("delimiter", csv_conf['delimiter']) \
        .option("header", csv_conf['header']) \
        .option("inferSchema", csv_conf['inferSchema']) \
        .load(f"{config['resources']['tweet']}/{folder}/*.csv")

    return read_file_df


def load_json_df_from_folder(folder):
    read_df = spark.read.json(path=f"{config['resources']['youtube']}/{folder}/*.json", multiLine=True)

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
    tweet_folders_to_load = get_files_in_folder(resource_config['tweet'], last_load_timestamp)

    for folder in tweet_folders_to_load:
        loaded_dataframe = load_csv_df_from_folder(folder)
        write_df_to_table(loaded_dataframe, "tweet_staging")


def extract_youtube_data(last_load_timestamp):
    youtube_folders_to_load = get_files_in_folder(resource_config['youtube'], last_load_timestamp)

    for folder in youtube_folders_to_load:
        loaded_youtube_dataframe = load_json_df_from_folder(folder)

        extracted_dataframe = extract_data_from_json(loaded_youtube_dataframe)
        write_df_to_table(extracted_dataframe, "youtube_staging")


def main():
    conn = psycopg2.connect(dbname=db_name, user=db_properties['user'],
                            password=db_properties['password'], host=db_host)
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(last_load) FROM sync")
    last_load_timestamp = cursor.fetchone()[0]

    extract_tweet_data(last_load_timestamp)
    extract_youtube_data(last_load_timestamp)

    cursor.execute("INSERT INTO sync VALUES (current_timestamp)")
    conn.commit()
    cursor.close()


if __name__ == "__main__":
    config = ConfigParser()
    # config.read("/home/pi/test/settings.ini")
    config.read("E:\\Projects\\sigma\\PyhonAnomaly\\sample\\settings.ini")

    resource_config = config['resources']

    db_conf = config['postgresql']
    db_url = db_conf['url_local']
    db_properties = {'user': db_conf['username'], 'password': db_conf['password'], 'driver': db_conf['driver']}

    db_name = db_conf['database']
    db_host = db_conf['host_local']

    csv_conf = config['csv']

    spark = SparkSession.builder \
        .master(config['spark']['local']) \
        .config("spark.driver.extraClassPath", db_conf['driver_classpath']) \
        .appName("test") \
        .getOrCreate()

    main()
