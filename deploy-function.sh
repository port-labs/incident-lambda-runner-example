zip -r function.zip src/

aws lambda update-function-code --function-name incident-management-example --zip-file fileb://function.zip 
