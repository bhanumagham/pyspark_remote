# src/pipeline/schemas.py

from pyspark.sql.types import (
    StructType, StructField,
    StringType, IntegerType, ArrayType
)

SUBJECT_SCHEMA = StructType([
    StructField("Telugu", IntegerType(), True),
    StructField("Hindi", IntegerType(), True),
    StructField("English", IntegerType(), True),
    StructField("Maths", IntegerType(), True),
    StructField("Science", IntegerType(), True),
    StructField("Social", IntegerType(), True),
])

EXAM_SCHEMA = StructType([
    StructField("exam", StringType(), True),
    StructField("subjects", SUBJECT_SCHEMA, True),
])

STUDENT_SCHEMA = StructType([
    StructField("name", StringType(), True),
    StructField("marks", ArrayType(EXAM_SCHEMA), True),
])

MARKS_SCHEMA = StructType([
    StructField("school", StringType(), True),
    StructField("academic_year", StringType(), True),
    StructField("students", ArrayType(STUDENT_SCHEMA), True),
])

WEIGHT_SCHEMA = StructType([
    StructField("exam_name", StringType(), True),
    StructField("weightage", IntegerType(), True),
])