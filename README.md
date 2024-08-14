# Osborn Snowflake Homework

## Deploy to GCP
```shell
# set the project default name. the project should have been created
# in cloud run ahead of time
gcloud config set project snowflakehomework
# run in us-east1 for lack of a better idea
gcloud config set run/region us-east1
# enable docker
gcloud auth configure-docker
#export requirements from poetry into requirements.txt that the Dockerfile can use
poetry export -f requirements.txt --output requirements.txt
# deploy the image to GCP
gcloud run deploy snowflake-homework --port 8080 --source .
```

## Run Locally
We used Poetry for the build framework so let's use it!
```shell
poetry run uvicorn app.main:app --reload
```
