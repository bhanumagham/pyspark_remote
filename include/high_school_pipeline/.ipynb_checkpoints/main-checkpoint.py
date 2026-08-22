from pyspark.sql import SparkSession
import yaml
from src.pipeline.job import run_job
from datetime import datetime



def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)

if __name__ == "__main__":
    config = load_config("config/pipeline_config.yaml")
    weights_path = config["paths"]["weights"]
    marks_path = config["paths"]["marks"]
    output_path = config["paths"]["output"]
    
    ts = datetime.now().strftime("%Y-%m-%d")
    output_filename = output_path + f"students_marks_ranked_{ts}.csv"

    builder = SparkSession.builder.appName(config["spark"]["app_name"])

    for key, value in config["spark"]["configs"].items():
        builder = builder.config(key, value)

    spark = builder.getOrCreate()

    
    run_job(spark, weights_path, marks_path, output_filename)

    spark.stop()
