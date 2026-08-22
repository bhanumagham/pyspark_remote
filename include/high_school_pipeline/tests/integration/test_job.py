# tests/integration/test_job.py

from pipeline.job import run_job


def test_full_pipeline(spark, tmp_path):

    input_students = str(tmp_path / "students.json")
    input_marks = str(tmp_path / "marks.parquet")
    output_path = str(tmp_path / "output")

    # create small test data
    spark.createDataFrame(
        [("S1", "Bhanu")],
        ["student_id", "name"]
    ).write.json(input_students)

    spark.createDataFrame(
        [("S1", "Maths", 90)],
        ["student_id", "subject", "marks"]
    ).write.parquet(input_marks)

    run_job(spark, input_students, input_marks, output_path)

    result = spark.read.parquet(output_path).collect()

    assert result[0]["total_marks"] == 90