from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.window import Window
import pandas as pd


spark = SparkSession.builder\
            .config("spark.driver.memory", "2g") \
            .appName("justice_chowdary_highschool").getOrCreate()


marks_path = "../data/jchs_marks_data.json"
weights_path = "../data/jchs_weightage.csv"

#=========== Loading Data ===============
df_weights = spark.read\
                .format("csv")\
                .option("header",True)\
                .option("inferSchema",True)\
                .option("mode","PERMISSIVE")\
                .load(weights_path)


df_marks = spark.read\
                .format("json")\
                .option("multiline",True)\
                .load(marks_path)
#===========Load in functions=============

def load_weights(weights_path):
    df_weights = spark.read\
                .format("csv")\
                .option("header",True)\
                .option("inferSchema",True)\
                .option("mode","PERMISSIVE")\
                .load(weights_path)
    return df_weights
    
def load_marks(marks_path):
    df_marks = spark.read\
                .format("json")\
                .option("multiline",True)\
                .load(marks_path)
    return df_marks

#============ transform Marks================
df2 = df_marks.withColumn("student_info", F.explode(F.col("students")))

df3 = df2.withColumn("student_name",F.col("student_info.name"))\
            .withColumn("marks",F.col("student_info.marks"))\
            .drop("students","student_info")

df4 = df3.withColumn("marks_exp",F.explode("marks"))\
            .withColumn("exam_name",F.col("marks_exp.exam"))\
            .withColumn("subjects",F.col("marks_exp.subjects"))\
            .drop("marks","marks_exp")


df5 = df4.select('academic_year', 'school', 'student_name', 
           'exam_name', 'subjects.English',
           'subjects.Hindi','subjects.Telugu',
           'subjects.Maths','subjects.Science',
          'subjects.Social')


df6 = df5.withColumn("sub_total",F.coalesce(df5.English,F.lit(0))
                     + F.coalesce(df5.Hindi,F.lit(0)) + 
                     F.coalesce(df5.Telugu,F.lit(0)) +
                     F.coalesce(df5.Maths,F.lit(0)) +
                     F.coalesce(df5.Science,F.lit(0)) +
                     F.coalesce(df5.Social,F.lit(0))).\
                    select('academic_year', 'school', 'student_name', 
           'exam_name','sub_total')

df_totals = df6.alias("df_totals")
#======== func
def transform_marks(df_marks):
    df2 = df_marks.withColumn("student_info", F.explode(F.col("students")))\
            .withColumn("student_name",F.col("student_info.name"))\
            .withColumn("marks",F.col("student_info.marks"))\
            .drop("students","student_info")

    df3 = df2.withColumn("marks_exp",F.explode("marks"))\
                .withColumn("exam_name",F.col("marks_exp.exam"))\
                .withColumn("subjects",F.col("marks_exp.subjects"))\
                .select('academic_year', 'school', 'student_name', 
                   'exam_name', 'subjects.English',
                   'subjects.Hindi','subjects.Telugu',
                   'subjects.Maths','subjects.Science',
                    'subjects.Social')
                


    df_totals = df5.withColumn("sub_total",F.coalesce(df5.English,F.lit(0))
                         + F.coalesce(df5.Hindi,F.lit(0)) + 
                         F.coalesce(df5.Telugu,F.lit(0)) +
                         F.coalesce(df5.Maths,F.lit(0)) +
                         F.coalesce(df5.Science,F.lit(0)) +
                         F.coalesce(df5.Social,F.lit(0))).\
                        select('academic_year', 'school', 'student_name', 
               'exam_name','sub_total')

     return df_totals
    

#====== Joining================

df_joined = df_totals.join(df_weights, "exam_name","left")
#=====func
def join_marks_weights(df_marks,df_weights):
    df_joined = df_totals.join(df_weights, "exam_name","left")
    return df_joined

#=============Final Calculation ================
df_weighted = df_joined.withColumn("weighted_score" , F.col("sub_total") * F.col("weightage") / 100 )


df_prefinal = df_weighted.groupBy("student_name").agg(F.round(F.sum("weighted_score"),2).alias("final_score"))

window1 = Window.orderBy(F.col("final_score").desc())

df_final = df_prefinal.withColumn("rank",F.row_number().over(window1))
#func
def rank_calculation(df_joined):
    df_weighted = df_joined.withColumn("weighted_score" , F.col("sub_total") * F.col("weightage") / 100 )\
                            .groupBy("student_name").agg(F.round(F.sum("weighted_score"),2).alias("final_score"))
    
    window1 = Window.orderBy(F.col("final_score").desc())
    
    df_final = df_weighted.withColumn("rank",F.row_number().over(window1))

    return df_final

#=============Saving the File =============


df_final.toPandas().to_csv("../data/final_ranks2.csv",index = False)
