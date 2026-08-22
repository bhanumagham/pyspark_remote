from pyspark.sql import DataFrame, SparkSession

def load_weights(spark: SparkSession, weights_path: str) -> DataFrame:
    df_weights = spark.read\
                .format("csv")\
                .option("header",True)\
                .option("inferSchema",True)\
                .option("mode","PERMISSIVE")\
                .load(weights_path)
    return df_weights
    
def load_marks(spark: SparkSession, marks_path: str) -> DataFrame:
    df_marks = spark.read\
                .format("json")\
                .option("multiline",True)\
                .load(marks_path)
    return df_marks