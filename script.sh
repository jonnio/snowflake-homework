

gcloud auth login
gcloud config set project snowflakehomework

gcloud config set run/region us-east1

gcloud auth configure-docker

poetry export -f requirements.txt --output requirements.txt

gcloud run deploy snowflake-homework --port 8080 --source .

poetry run uvicorn app.main:app --reload


#### UX / UI DEPLOY

./ux/gradlew -p ux clean build && gcloud run deploy snowflake-homework-ux --port 8081 --source ./ux


# MY SNOWFLAKE URL
# https://zn23616.us-east-2.aws.snowflakecomputing.com


# snowsql -a zn23616.us-east-2.aws -u jonnio -r ROLE_HOMEWORK -w HOMEWORK_WH -d SNOWFLAKE_SAMPLE_DATA -s TPCH_SF10 --authenticator oauth --token
