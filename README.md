### Pyspark Repository 
Building a remote repository for all my pyspark hobby project notebooks.

- Spark version 3.5.1
- Jdk 17
- python 3.1.0
- jupyterlab - compatible for spark 3.5.0 and python 3.1.1 - Installed Pyspark 3.5.1 in the container
- Delta lake - 3.0.0 which is compatible with Spark version above

Tip: make sure you build the image with the compatible versions, else you will waste a lot of time debugging what went wrong.

  ========================================
#### Important Commands ####
- docker-compose build --no-cache   (for rebuilding the image after you do some changes to configs etc)
- docker compose up (to start the container)
- docker compose down (to stop the containers)
  
  ========================================
  
Tip : Make sure you keep Build in the place of Image in Config.YAML, as image skips the DockerFile   


