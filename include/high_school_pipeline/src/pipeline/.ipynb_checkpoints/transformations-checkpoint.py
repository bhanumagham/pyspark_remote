import pyspark.sql.functions as F
from pyspark.sql.window import Window
import pandas as pd

from pyspark.sql import DataFrame

def explode_students(df_marks: DataFrame) -> DataFrame:
    return (df_marks.withColumn("student_info", F.explode(F.col("students")))\
            .withColumn("student_name",F.col("student_info.name"))\
            .withColumn("marks",F.col("student_info.marks"))\
            .drop("students","student_info"))


def explode_marks(df2: DataFrame) -> DataFrame:
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
    return df3.dropDuplicates(['academic_year', 'school', 'student_name', 'exam_name'])


def calculate_totals(df5: DataFrame) -> DataFrame:
    subjects = ['English', 'Hindi', 'Telugu', 'Maths', 'Science', 'Social']
    return (df5.withColumn("sub_total", sum(F.coalesce(F.col(c), F.lit(0)) for c in subjects)) )

def join_marks_weights(df_totals: DataFrame, df_weights: DataFrame) -> DataFrame:
    return df_totals.join(df_weights, "exam_name","left")

def rank_calculation(df_joined: DataFrame) -> DataFrame:
    df_weighted = df_joined.withColumn("weighted_score" , F.col("sub_total") * F.col("weightage") / 100 )\
                            .groupBy("student_name").agg(F.round(F.sum("weighted_score"),2).alias("final_score"))
    
    window1 = Window.orderBy(F.col("final_score").desc())
    
    return ( df_weighted.withColumn("rank",F.row_number().over(window1)) )



    