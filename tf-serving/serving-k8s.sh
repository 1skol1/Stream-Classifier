#!/bin/bash

gcloud auth list &&
gcloud config list project &&

gcloud config set compute/zone asia-south2-a &&

export PROJECT_ID=$(gcloud config get-value project) &&
export CLUSTER_NAME=cluster-1 &&

gcloud beta container clusters create $CLUSTER_NAME \
  --cluster-version=latest \
  --machine-type=n1-standard-4 \
  --enable-autoscaling \
  --min-nodes=1 \
  --max-nodes=3 \
  --num-nodes=1 &&

gcloud container clusters list &&

gcloud container clusters get-credentials $CLUSTER_NAME &&

kubectl get nodes &&

kubectl apply -f ./serving/configmap.yaml &&

kubectl apply -f ./serving/deployment.yaml &&

kubectl get deployments &&

kubectl apply -f ./serving/service.yaml &&

kubectl get svc image-classifier &&

kubectl autoscale deployment image-classifier \
--cpu-percent=60 \
--min=1 \
--max=4 &&

kubectl get hpa


