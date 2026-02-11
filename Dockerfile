FROM jupyter/base-notebook:python-3.10
USER root


# Set permissions
RUN chown -R jovyan:users /home/jovyan

RUN apt-get update && \
    apt-get install -y openjdk-17-jdk && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64
ENV PATH=$JAVA_HOME/bin:$PATH

# Install Delta Lake dependencies


USER jovyan
# Install Python packages
RUN pip install \
    pyspark==3.5.1 \
    delta-spark==3.0.0 \
    pandas \
    matplotlib \
    seaborn

#RUN pip install pyspark==3.5.1


########

