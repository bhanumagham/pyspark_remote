# tests/conftest.py
import pytest
from pyspark.sql import SparkSession
import sys
import os
sys.path.append(os.path.abspath("src"))

@pytest.fixture(scope="session")
def spark():
    spark = (
        SparkSession.builder
        .master("local[2]")
        .appName("pytest-pyspark")
        .getOrCreate()
    )
    yield spark
    spark.stop()