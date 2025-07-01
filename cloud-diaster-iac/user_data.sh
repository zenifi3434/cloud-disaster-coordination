#!/bin/bash
yum update -y
amazon-linux-extras install docker -y
service docker start
usermod -a -G docker ec2-user

docker pull zenifi/disaster-api:latest

docker run -d -p 8000:8000 --restart unless-stopped zenifi/disaster-api:latest