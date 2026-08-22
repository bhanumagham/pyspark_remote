from pyspark.sql import DataFrame
from pyspark.sql import functions as F

def assert_non_empty(df: DataFrame, msg: str = "DataFrame is empty")-> None:
    if df.limit(1).count() == 0:
        raise ValueError(msg)



def check_no_nulls(df: DataFrame, col: str)-> None:
    if df.filter(F.col(col).isNull()).limit(1).count() > 0:
        raise ValueError(f"Null values found in {col}")


def check_range(df: DataFrame, col: str, min_val: float, max_val: float)-> None:
    if df.filter((F.col(col) < min_val) | (F.col(col) > max_val)).limit(1).count() > 0:
        raise ValueError(f"{col} out of range [{min_val}, {max_val}]")