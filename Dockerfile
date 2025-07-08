FROM jupyter/pyspark-notebook:latest

USER root

# Install any additional Python packages here
RUN pip install pandas matplotlib seaborn

# Set permissions
RUN chown -R jovyan:users /home/jovyan


# Install Delta Lake dependencies
ENV DELTA_CORE_VERSION=3.0.0 \
    SPARK_VERSION=3.5.1

# Add Delta Lake JARs to Spark
RUN wget https://repo1.maven.org/maven2/io/delta/delta-spark_2.12/3.0.0/delta-spark_2.12-3.0.0.jar -P /usr/local/spark/jars/ \
 && wget https://repo1.maven.org/maven2/io/delta/delta-storage/3.0.0/delta-storage-3.0.0.jar -P /usr/local/spark/jars/
#https://repo1.maven.org/maven2/io/delta/delta-spark_2.12/3.0.0/delta-spark_2.12-3.0.0.jar
# Optionally install Python delta library
RUN pip install delta-spark==3.0.0

USER jovyan
