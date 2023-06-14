# -*- coding: utf-8 -*-

"""MakeDatasetApp"""
from pyspark.sql import SparkSession

inputFile = "README.md"  # Should be some file on your system
spark = SparkSession.builder.appName("MakeDatasetApp").getOrCreate()
cacheData = spark.read.text(inputFile).cache()

numAs = cacheData.filter(cacheData.value.contains('a')).count()
numBs = cacheData.filter(cacheData.value.contains('b')).count()

print("Lines with a: %i, lines with b: %i" % (numAs, numBs))

spark.stop()


