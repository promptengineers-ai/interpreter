#!/bin/bash

SHORT_SHA=$(git rev-parse --short HEAD)
APP_NAME="interpreter"

docker build -t promptengineers/$APP_NAME:$SHORT_SHA .

echo ""
## Prompt to push the image to Docker Hub
echo "Do you want to push the image to Docker Hub with tag $SHORT_SHA? (y/n)"
read -r response
if [[ $response =~ ^([yY][eE][sS]|[yY])$ ]]
then
  docker push promptengineers/$APP_NAME:$SHORT_SHA
fi

echo ""
## Prompt to tag the image as latest and push to Docker Hub
echo "Do you also want to tag the image as latest and push to Docker Hub? (y/n)"
read -r response
if [[ $response =~ ^([yY][eE][sS]|[yY])$ ]]
then
  docker tag promptengineers/$APP_NAME:$SHORT_SHA promptengineers/$APP_NAME:latest
  docker push promptengineers/$APP_NAME:latest
fi
