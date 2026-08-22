# writer.py
from pyspark.sql import DataFrame


def write_output(df: DataFrame, path: str) -> None:
    (
        df
        .write
        .mode("overwrite")
        .option("header",True)
        .csv(path)
    )