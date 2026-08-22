from src.pipeline.dq.basic import assert_non_empty, check_no_nulls
from pyspark.sql import DataFrame
from src.pipeline.logging.logger import get_logger

logger = get_logger(__name__)

def validate_dataframe(df: DataFrame)-> None:
    assert_non_empty(df, "Exploded data is empty")
    check_no_nulls(df, "student_name")