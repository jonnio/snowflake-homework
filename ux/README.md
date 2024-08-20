# Front End


```shell
# docker build -t your-image-name .

./ux/gradlew -p ./ux clean build

gcloud run deploy snowflake-homework-ux --source ./ux

./ux/gradlew -p ./ux clean build && gcloud run deploy snowflake-homework-ux --source ./ux

```