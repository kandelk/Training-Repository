import codecs
import re

from pyspark import SparkContext, SQLContext

if __name__ == "__main__":

    sc = SparkContext("local", "SQLApp")
    sqlContext = SQLContext(sc)
    dataFragment = sqlContext.read.format('orc').load("E:\\Projects\\sigma\\FileAnomaly\\src\\main\\resources\\test2")

    wordCount = dict()

    def process_string(string):
        processed_string = re.sub("[^А-Яа-я\\w]", " ", string)
        processed_string = re.sub("\\s+", " ", processed_string)
        return processed_string.split()

    def put_words_to_dict(words):
        for word in words:
            wordCount[word] = wordCount.pop(word, 0) + 1

    # dataFragment.foreach(lambda row: put_words_to_dict(process_string(row.__getitem__('value'))))

    for row in dataFragment.collect():
        put_words_to_dict(process_string(row.__getitem__('value')))

    wordCount = sorted(wordCount.items(), key=lambda kv: kv[1])

    file = open("result.txt", 'w')
    file.close()
    file = codecs.open("result.txt", "a", "utf-8")
    for word in wordCount:
        file.write(str(word[0]) + " - " + str(word[1]) + "\n")
    file.close()
