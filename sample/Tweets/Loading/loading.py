from configparser import ConfigParser

from pyspark.sql import functions as func, SparkSession


def process_data(dataframe):
    return dataframe.filter(dataframe.tweet.isNotNull()) \
        .filter(dataframe.created_at.like("2020-%-%")) \
        .withColumn("created_at", func.substring(dataframe.created_at, 0, 10)) \
        .distinct()


def clean_data(dataframe):
    return dataframe.filter(
        lambda df:
            spark.read.jdbc(
                url=db_url,
                table=f"(SELECT * FROM tweets WHERE tweet_id LIKE cast({df['tweet_id'].__getitem__('value')} as varchar(255))) as my_table",
                properties=db_properties
            ).count() == 0
    )


def main():
    staged_data = spark.read.jdbc(
        url=db_url,
        table='staging',
        properties=db_properties
    )

    processed_data = process_data(staged_data)

    processed_data.write.jdbc(
        url=db_url,
        table='tweets',
        properties=db_properties,
        mode='append'
    )


if __name__ == "__main__":
    config = ConfigParser()
    config.read("/home/pi/test/settings.ini")
    resource_folder_path = config['resources']['tweets']

    db_conf = config['postgresql']
    db_url = db_conf['url']
    db_properties = {'user': db_conf['username'], 'password': db_conf['password'], 'driver': db_conf['driver']}

    spark = SparkSession.builder \
        .getOrCreate()

    main()
