from pyspark.sql import SparkSession

from src.pipeline.reader import load_marks, load_weights
from src.pipeline.transformations import (explode_students, explode_marks, 
                             clean_marks, calculate_totals, 
                             join_marks_weights, rank_calculation)
from src.pipeline.writer import write_output 
from src.pipeline.dq.pipeline_quality import validate_dataframe

from src.pipeline.logging.logger import get_logger

def run_job(spark: SparkSession, weights_path: str, marks_path: str, output_path: str) -> None:
    # Load the data
    df_marks = load_marks(spark, marks_path)
    df_weights = load_weights(spark, weights_path)

    logger = get_logger(__name__)
    logger.info("Data loaded successfully")

    # Transform the data
    """
    df_exploded_students = explode_students(df_marks)
    df_exploded_marks = explode_marks(df_exploded_students)
    df_cleaned_marks = clean_marks(df_exploded_marks)
    df_totals = calculate_totals(df_cleaned_marks)
    """
    df_totals = df_marks.transform(explode_students)\
                        .transform(explode_marks)\
                        .transform(clean_marks)\
                        .transform(calculate_totals)

    logger.info("Data transformation completed successfully")
    logger.info(f"Total records after transformation: {df_totals.count()}")
    validate_dataframe(df_totals)
    
    df_joined = join_marks_weights(df_totals, df_weights)

    logger.info("Data joined successfully")
    df_ranked = rank_calculation(df_joined)

    # Write the output
    write_output(df_ranked, output_path)
    