# Google Cloud Deploy

## Requirements

### Install gunicorn

`pip install gunicorn`

## Create requirements

`pip freeze > requirements.txt`

## Create Dockerfile

Create a Dockerfile in project root directory

## Create Artifact Repository (Google Cloud)

Create repository on gcp with project name
`https://console.cloud.google.com/artifacts`

## Configure Docker

```
gcloud auth configure-docker \
    us-east1-docker.pkg.dev
```

## Build image

`docker build -t <<image-name>> .`

### For M1 Apple Silicon Chip

Docker image has to be build using linux. Cloud Run specifically supports the Linux x86_64 ABI format.

`docker build --platform linux/amd64 -t <<image-name>> .`

## Tag image

`docker tag <<image-name>> <<region>>-docker.pkg.dev/<project-id>>/<<repo-name>>/<<image-name-you-want>>`

## Push image

`docker push <<region>>-docker.pkg.dev/<project-id>>/<<repo-name>>/<<image-name-you-want>>`

## Deploy Cloud Run service

`gcloud run deploy --image us-east1-docker.pkg.dev/front-street-ug/app/fs_api --platform managed`

### Edit and Redeploy Cloud

`gcloud run deploy fsapi --image us-east1-docker.pkg.dev/front-street-ug/app/fs_api:latest --platform managed`

### Set default region

`gcloud config set run/region us-east1`
