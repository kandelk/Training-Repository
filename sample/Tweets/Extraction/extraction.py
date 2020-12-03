from configparser import ConfigParser
from functools import reduce
from os import walk

from pyspark.sql import DataFrame, SparkSession

def get_files_in_folder():
    files = []
    for (dirpath, dirnames, filenames) in walk(resource_folder_path):
        files = filenames
        break

    return files


def load_csv_dataframe_from_resource_folder(filename):
    read_file_df = spark.read.format('csv') \
        .option("delimiter", csv_conf['delimiter']) \
        .option("header", csv_conf['header']) \
        .option("inferSchema", csv_conf['inferSchema']) \
        .load(f"{config['resources']['tweets']}/{filename}")

    return read_file_df


def main():
    files_to_load = get_files_in_folder()

    if len(files_to_load) == 0:
        print('Empty folder: ' + resource_folder_path)
        return

    loaded_dataframes = []
    for filename in files_to_load:
        loaded_dataframes.append(load_csv_dataframe_from_resource_folder(filename))

    united_dataframe = reduce(DataFrame.unionAll, loaded_dataframes)

    united_dataframe.write.jdbc(
        url=db_url,
        table=db_table,
        properties=db_properties,
        mode='overwrite'
    )


if __name__ == "__main__":
    config = ConfigParser()
    config.read("/home/pi/test/settings.ini")
    resource_folder_path = config['resources']['tweets']

    db_conf = config['postgresql']
    db_url = db_conf['url']
    db_properties = {'user': db_conf['username'], 'password': db_conf['password'], 'driver': db_conf['driver']}
    db_table = "staging"

    csv_conf = config['csv']

    spark = SparkSession.builder \
        .getOrCreate()

    main()
