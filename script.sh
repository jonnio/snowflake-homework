

gcloud auth login
gcloud config set project snowflakehomework

gcloud config set run/region us-east1

gcloud auth configure-docker

poetry export -f requirements.txt --output requirements.txt

gcloud run deploy snowflake-homework --port 8080 --source .

 poetry run uvicorn app.main:app --reload


https://zn23616.us-east-2.aws.snowflakecomputing.com
