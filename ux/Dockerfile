FROM openjdk:21-jdk

WORKDIR /app
# Note that the version is hard-coded for now
COPY build/libs/snowflake-homework-ux-0.0.1-SNAPSHOT.jar app.jar
EXPOSE 8081
CMD ["java", "-jar", "app.jar"]
