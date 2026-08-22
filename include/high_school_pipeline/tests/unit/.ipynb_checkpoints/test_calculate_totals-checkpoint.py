from src.pipeline.transformations import calculate_totals
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

def test_calculate_totals_basic(spark):

    data = [
        ("2025", "ABC School", "Bhanu", "Unit Test 1", 80, 70, 60, 90, 85, 75)
    ]

    

    schema = StructType([
        StructField("academic_year", StringType(), True),
        StructField("school", StringType(), True),
        StructField("student_name", StringType(), True),
        StructField("exam_name", StringType(), True),
        StructField("English", IntegerType(), True),
        StructField("Hindi", IntegerType(), True),
        StructField("Telugu", IntegerType(), True),
        StructField("Maths", IntegerType(), True),
        StructField("Science", IntegerType(), True),
        StructField("Social", IntegerType(), True),
    ])

    df = spark.createDataFrame(data, schema)

    

    result_df = calculate_totals(df)
    result = result_df.collect()[0]

    assert result["sub_total"] == 80 + 70 + 60 + 90 + 85 + 75

def test_calculate_totals_with_nulls(spark):

    data = [
        ("2025", "ABC School", "Siva", "Unit Test 1", None, 70, None, 90, None, 40)
    ]

    schema = StructType([
        StructField("academic_year", StringType(), True),
        StructField("school", StringType(), True),
        StructField("student_name", StringType(), True),
        StructField("exam_name", StringType(), True),
        StructField("English", IntegerType(), True),
        StructField("Hindi", IntegerType(), True),
        StructField("Telugu", IntegerType(), True),
        StructField("Maths", IntegerType(), True),
        StructField("Science", IntegerType(), True),
        StructField("Social", IntegerType(), True),
    ])

    df = spark.createDataFrame(data, schema)

    result_df = calculate_totals(df)
    result = result_df.collect()[0]

    # None should be treated as 0
    assert result["sub_total"] == 0 + 70 + 0 + 90 + 0 + 40


def test_calculate_totals_multiple_rows(spark):

    data = [
        ("2025", "ABC", "A", "UT1", 10, 10, 10, 10, 10, 10),
        ("2025", "ABC", "B", "UT1", 20, 20, 20, 20, 20, 20)
    ]

    schema = StructType([
        StructField("academic_year", StringType(), True),
        StructField("school", StringType(), True),
        StructField("student_name", StringType(), True),
        StructField("exam_name", StringType(), True),
        StructField("English", IntegerType(), True),
        StructField("Hindi", IntegerType(), True),
        StructField("Telugu", IntegerType(), True),
        StructField("Maths", IntegerType(), True),
        StructField("Science", IntegerType(), True),
        StructField("Social", IntegerType(), True),
    ])

    df = spark.createDataFrame(data, schema)

    result_df = calculate_totals(df)

    results = {r["student_name"]: r["sub_total"] for r in result_df.collect()}

    assert results["A"] == 60
    assert results["B"] == 120