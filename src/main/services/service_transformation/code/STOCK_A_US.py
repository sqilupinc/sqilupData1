import json
import sys
#import pyspark.sql import SparkSession
#import boto3
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark import SparkConf 

def main():
#conf=SparkConf().setAll(['spark.master','spark://34.205.139.127'),('spark.app.name','Dharma_Spark'),('spark.executor.memory','8g'),('spark.executor.cores','3'),('spark.cores.max','3'),('spark.driver.memory','8g')])    
	conf=SparkConf().set('spark.app.name','STOCK_A_US')
	sc=SparkContext(conf=conf)
	sqlContext=SQLContext(sc)  
	schema=StructType(		
		   [StructField("Date",StringType(), True),
		   StructField("Open",FloatType(), True),
		   StructField("High",FloatType(), True),
		   StructField("Low",FloatType(), True),
		   StructField("Close",FloatType(), True),
		   StructField("Volume",FloatType(), True),
		   StructField("OpenInt",FloatType(), True)])    
	df=sqlContext.read.format('csv').schema(schema).option('delimiter',',').option('header','true').load('C:\\Spark_projects\\a_us.txt')
	df.show()
	df.groupBy("Date").avg("Open").show()
main()