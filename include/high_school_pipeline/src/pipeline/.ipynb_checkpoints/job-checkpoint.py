from pyspark.sql import SparkSession

from src.pipeline.reader import load_marks, load_weights
from src.pipeline.transformations import (explode_students, explode_marks, 
                             clean_marks, calculate_totals, 
                             join_marks_weights, rank_calculation)
from src.pipeline.writer import write_output 

def run_job(spark: SparkSession, weights_path: str, marks_path: str, output_path: str) -> None:
    # Load the data
    df_marks = load_marks(spark, marks_path)
    df_weights = load_weights(spark, weights_path)

    # Transform the data
    df_exploded_students = explode_students(df_marks)
    df_exploded_marks = explode_marks(df_exploded_students)
    df_cleaned_marks = clean_marks(df_exploded_marks)
    df_totals = calculate_totals(df_cleaned_marks)
    df_joined = join_marks_weights(df_totals, df_weights)
    df_ranked = rank_calculation(df_joined)

    # Write the output
    write_output(df_ranked, output_path)
    