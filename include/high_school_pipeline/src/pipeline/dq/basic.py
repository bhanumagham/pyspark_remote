from pyspark.sql import DataFrame
from src.pipeline.logging.logger import get_logger
from pyspark.sql import functions as F

logger = get_logger(__name__)


def assert_non_empty(df: DataFrame, name: str = "dataset"):
    logger.info(f"Checking non-empty for {name}")

    if df.limit(1).count() == 0:
        logger.error(f"{name} is empty")
        raise ValueError(f"{name} is empty")

    logger.info(f"{name} passed non-empty check")


def check_no_nulls(df: DataFrame, col: str)-> None:
    logger.info(f"Checking for null values in {col}")
    if df.filter(F.col(col).isNull()).limit(1).count() > 0:
        logger.error(f"Null values found in {col}")
        raise ValueError(f"Null values found in {col}")
    logger.info(f"{col} passed null check")


def check_range(df: DataFrame, col: str, min_val: float, max_val: float)-> None:
    logger.info(f"Checking range for {col}")
    if df.filter((F.col(col) < min_val) | (F.col(col) > max_val)).limit(1).count() > 0:
        logger.error(f"{col} out of range [{min_val}, {max_val}]")
        raise ValueError(f"{col} out of range [{min_val}, {max_val}]")
    logger.info(f"{col} passed range check")