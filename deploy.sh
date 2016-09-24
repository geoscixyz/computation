#!/bin/bash

cd ../../..
if [ ! -d "$GAE_PYTHONPATH" ]; then wget https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.38.zip;
    unzip -q google_appengine_1.9.38.zip; fi
if [ ! -d "$GCSDK_PATH" ]; then curl https://sdk.cloud.google.com | bash; fi

# if [ "$TRAVIS_BRANCH" = "master" -a "$TRAVIS_PULL_REQUEST" = "false" ]; then
if [ "$TRAVIS_BRANCH" = "gae-deploy" -a "$TRAVIS_PULL_REQUEST" = "false" ]; then
  export GAE_PROJECT=simpegtutorials
  export APP_VERSION="$(echo $TRAVIS_COMMIT | cut -c -7)"
  export PROMOTE=Yes
fi

if [ -z "$GAE_PROJECT" ]; then
  exit 0;
fi

echo Unpack credentials
openssl aes-256-cbc -K $encrypted_c85711639858_key -iv $encrypted_c85711639858_iv -in docs/credentials.tar.gz.enc -out credentials.tar.gz -d
  -in credentials.tar.gz.enc -d | tar -xzf -

echo Starting Deploy
# gcloud -q components update gae-python
gcloud auth activate-service-account --key-file client-secret.json
gcloud config set project $GAE_PROJECT
gcloud preview datastore create-indexes ./docs/index.yaml --project $GAE_PROJECT
if [ "$PROMOTE" == "Yes" ]; then
  gcloud preview app deploy ./docs/app.yaml --project $GAE_PROJECT --version $APP_VERSION --promote;
else
  gcloud preview app deploy ./docs/app.yaml --project $GAE_PROJECT --version $APP_VERSION --no-promote;
fi
exit 0
