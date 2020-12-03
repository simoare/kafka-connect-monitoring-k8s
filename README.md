# kafka-connect-monitoring-k8s
A Python Docker Image to monitoring your Kafka connectors using K8s cronjob

This is my first python journey, in fact this project is not intended to be perfect. The aim was to implement and automate something capable to monitoring (and alerting) the Kafka Connectors as well the Kafka Streams application in a Kubernetes way. 


1) The kubernetes cluster used for the project has not direct access to the internet. The Teams webhook calls are made via corporate proxy

2) To check the KStream application consumer group lag, we use https://github.com/linkedin/Burrow, in fact the code calls the REST API exposed by the Burrow docker container







