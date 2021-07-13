######################################################
# Dockerfile per la Dashboard
######################################################

FROM openjdk:8-jdk 

RUN apt-get update && apt-get install -y curl

ADD build/libs/dashboard-1.0.0.jar dashboard-1.0.0.jar

EXPOSE 8080

ENTRYPOINT ["java", "-Xmx128m", "-Xms128m", "-jar", "dashboard.jar"]
