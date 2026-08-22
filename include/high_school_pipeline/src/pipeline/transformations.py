from functools import reduce
from operator import add
import pyspark.sql.functions as F
from pyspark.sql.window import Window
import pandas as pd

from pyspark.sql import DataFrame

def explode_students(df_marks: DataFrame) -> DataFrame:
    """Explode the top-level 'students' array into one row per student.

    Args:
        df_marks: DataFrame with schema matching MARKS_SCHEMA containing
            columns 'academic_year', 'school', and 'students' (array of structs).

    Returns:
        DataFrame with one row per student containing the original
        'academic_year' and 'school' columns plus:
            - student_name: the student's name
            - marks: the student's marks array (one element per exam)

    Notes:
        This transformation preserves other top-level fields and drops the
        original 'students' column.
    """
    return (df_marks.withColumn("student_info", F.explode(F.col("students")))\
            .withColumn("student_name",F.col("student_info.name"))\
            .withColumn("marks",F.col("student_info.marks"))\
            .drop("students","student_info"))


def explode_marks(df2: DataFrame) -> DataFrame:
    """Explode the per-student 'marks' array into one row per (student, exam).

    Args:
        df2: DataFrame produced by explode_students that contains the
            'marks' column (array of exam structs) and 'student_name'.

    Returns:
        DataFrame with one row per student-exam containing:
            - academic_year, school, student_name
            - exam_name
            - individual subject columns (English, Hindi, Telugu, Maths, Science, Social)

    Notes:
        The nested 'marks' -> 'exam' and 'subjects' fields are flattened to
        top-level columns to make aggregation and joins straightforward.
    """
    return (df2.withColumn("marks_exp",F.explode("marks"))\
                .withColumn("exam_name",F.col("marks_exp.exam"))\
                .withColumn("subjects",F.col("marks_exp.subjects"))\
                .select('academic_year', 'school', 'student_name', 
                   'exam_name', 'subjects.English',
                   'subjects.Hindi','subjects.Telugu',
                   'subjects.Maths','subjects.Science',
                    'subjects.Social')
    )
                
def clean_marks(df3: DataFrame) -> DataFrame:
    """Remove duplicate student-exam records.

    Args:
        df3: DataFrame with columns including 'academic_year', 'school',
            'student_name', and 'exam_name'.

    Returns:
        DataFrame with duplicate rows (based on academic_year, school,
        student_name, exam_name) dropped.

    Notes:
        This is a simple de-duplication step to guard against repeated
        entries in the input JSON.
    """
    return df3.dropDuplicates(['academic_year', 'school', 'student_name', 'exam_name'])


def calculate_totals(df5: DataFrame) -> DataFrame:
    """Compute subtotal of all subject marks for each student-exam row.

    Args:
        df5: DataFrame with subject columns: English, Hindi, Telugu, Maths,
            Science, Social. These columns may contain nulls.

    Returns:
        DataFrame with an added column 'sub_total' that is the sum of the
        subject marks for the row. Nulls are treated as zero.

    Example:
        If a row has English=80, Hindi=None, Telugu=70, ..., then
        sub_total = 80 + 0 + 70 + ...
    """
    subjects = ['English', 'Hindi', 'Telugu', 'Maths', 'Science', 'Social']
    total_expr = reduce(add, (F.coalesce(F.col(c), F.lit(0)) for c in subjects))
    return (df5.withColumn("sub_total", total_expr) )

def join_marks_weights(df_totals: DataFrame, df_weights: DataFrame) -> DataFrame:
    """Join the per-exam totals with exam weightages.

    Args:
        df_totals: DataFrame produced by calculate_totals and containing
            an 'exam_name' column and 'sub_total'.
        df_weights: DataFrame with 'exam_name' and 'weightage' columns.

    Returns:
        Left join of df_totals with df_weights on 'exam_name'. This
        preserves all student-exam rows and attaches the corresponding
        weightage when available.
    """
    return df_totals.join(df_weights, "exam_name","left")

def rank_calculation(df_joined: DataFrame) -> DataFrame:
    """Calculate weighted scores per exam, aggregate to final score, and rank students.

    Args:
        df_joined: DataFrame resulting from join_marks_weights with columns
            including 'student_name', 'sub_total', and 'weightage'.

    Returns:
        DataFrame with one row per student containing:
            - final_score: sum of (sub_total * weightage / 100) across exams,
              rounded to 2 decimal places
            - rank: integer rank ordered by final_score descending (1 is highest)

    Notes:
        Ties are broken by row_number() ordering; if stable tie-handling is
        required, replace row_number() with dense_rank() or rank().
    """
    df_weighted = df_joined.withColumn("weighted_score" , F.col("sub_total") * F.col("weightage") / 100 )\
                            .groupBy("school","student_name").agg(F.round(F.sum("weighted_score"),2).alias("final_score"))
    
    window1 = Window.partitionBy(F.col("school")).orderBy(F.col("final_score").desc())
    
    return ( df_weighted.withColumn("rank",F.dense_rank().over(window1)).drop("school") )