# tests/integration/test_job.py

from pipeline.job import run_job


def test_full_pipeline(spark, tmp_path):

    input_weights = str(tmp_path / "weights.csv")
    input_marks = str(tmp_path / "marks.json")
    output_path = str(tmp_path / "output")

    # create small test data
    spark.read.csv("tests/data/input/weights.csv", header=True).write.csv(input_weights, header=True)
    spark.read.option("multiline", "true").json("tests/data/input/marks.json").write.json(input_marks, mode="overwrite")

    run_job(spark, input_weights, input_marks, output_path)

    result = spark.read.option("header",True).option("inferSchema",True).csv(output_path).collect()

    assert result[0]["final_score"] == 516.2