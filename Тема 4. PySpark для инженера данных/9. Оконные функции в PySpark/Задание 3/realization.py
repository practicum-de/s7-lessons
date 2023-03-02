    import pyspark
    from pyspark.sql import SparkSession
    from pyspark.sql.window  ...
    import pyspark.sql.functions ....
    
    spark = SparkSession.builder \
                        .master("yarn") \
                        .appName("Learning DataFrames") \
                        .getOrCreate()
    
    events = spark.read.json("/user/master/data/events/date=2022-05-01")
    
    window = Window().partitionBy('event. ...').orderBy('...')
    
    dfWithLag = events.withColumn("lag_7",F.lag("event. ... ").over(window))
    
    dfWithLag.select(...) \
    .filter(dfWithLag.lag_7. ...) \
    .orderBy(...) \
    .show(10, False) 
