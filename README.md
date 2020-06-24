# ecs-fargate-sample-app
django sample app to demonstrate ecs fargate deployment


build docker base image
```
docker build -f config/app/Dockerfile_app_base -t kokospapa8/django-sample:base .
docker push kokospapa8/django-sample:base
```