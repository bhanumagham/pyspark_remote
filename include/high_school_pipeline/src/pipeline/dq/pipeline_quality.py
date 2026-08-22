from pipeline.dq.basic import assert_non_empty, check_no_nulls
from pyspark.sql import DataFrame

def validate_dataframe(df: DataFrame)-> None:
    assert_non_empty(df, "Exploded data is empty")
    check_no_nulls(df, "student_name")