#!/bin/bash
cd lambda_layer

# Create layer based on requirements.txt in python/ directory
pip3 install -r requirements.txt --platform manylinux2014_x86_64 --target ./python --only-binary=:all:

# Create a zip of the layer
zip -r layer.zip python

aws lambda publish-layer-version --layer-name incident_lambda_port_execution_package_layer --description "Python pacakges layer for lambda Port execution example" --compatible-runtimes python3.6 python3.7 python3.8 python3.9 --zip-file fileb://layer.zip --region eu-west-1
