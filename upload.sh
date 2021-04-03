#!/bin/zsh
cd /Users/ian/venmo-importer/ &&
rm -rf ./package;
rm deployment-package.zip;
pip install -r requirements.txt --target /Users/ian/venmo-importer/package &&
cd /Users/ian/venmo-importer/package &&
zip -r /Users/ian/venmo-importer/deployment-package.zip ./* &&
cd /Users/ian/venmo-importer  &&
zip -g /Users/ian/venmo-importer/deployment-package.zip handler.py &&
zip -g /Users/ian/venmo-importer/deployment-package.zip transaction.py &&
aws lambda update-function-code --function-name venmo-ynab-importer --zip-file fileb:///Users/ian/venmo-importer/deployment-package.zip &&
echo "Success"
