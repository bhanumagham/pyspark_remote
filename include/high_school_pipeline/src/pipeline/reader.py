from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import ArrayType, StructType, StructField, StringType, IntegerType, DateType

def load_weights(spark: SparkSession, weights_path: str) -> DataFrame:
    weight_schema = StructType(
    [
    StructField("exam_name", StringType(), True),
    StructField("weightage", IntegerType(), True)
    ]
    )
    df_weights = spark.read\
                .format("csv")\
                .option("header",True)\
                .schema(weight_schema)\
                .option("mode","PERMISSIVE")\
                .load(weights_path)
    return df_weights
    
def load_marks(spark: SparkSession, marks_path: str) -> DataFrame:

    subject_schema = StructType(
        [StructField("Telugu", IntegerType(), True),
        StructField("Hindi", IntegerType(), True),
        StructField("English", IntegerType(), True),
        StructField("Maths", IntegerType(), True),
        StructField("Science", IntegerType(), True),
        StructField("Social", IntegerType(), True)]
    )
    exam_subject_schema = StructType(
        [StructField("exam", StringType(), True),
        StructField("subjects", subject_schema, True)]
    )
    student_schema = StructType(
        [StructField("name", StringType(), True),
        StructField("marks", ArrayType(exam_subject_schema), True)]
    )
    
    marks_schema = StructType(
        [StructField("school", StringType(), True),
        StructField("academic_year", StringType(), True),
        StructField("students", ArrayType(student_schema), True)]
    )

    
    df_marks = spark.read\
                .format("json")\
                .option("multiline",True)\
                .schema(marks_schema)\
                .load(marks_path)
    return df_marks