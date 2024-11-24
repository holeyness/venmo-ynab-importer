#!/bin/zsh
cd /Users/ianluo/software/venmo-importer/ &&
rm -rf ./package;
rm deployment-package.zip;
pip install -r requirements.txt --target /Users/ianluo/software/venmo-importer/package &&
cd /Users/ianluo/software/venmo-importer/package &&
zip -r /Users/ianluo/software/venmo-importer/deployment-package.zip ./* &&
cd /Users/ianluo/software/venmo-importer  &&
zip -g /Users/ianluo/software/venmo-importer/deployment-package.zip handler.py &&
zip -g /Users/ianluo/software/venmo-importer/deployment-package.zip transaction.py &&
aws lambda update-function-code --function-name venmo-ynab-importer --zip-file fileb:///Users/ianluo/software/venmo-importer/deployment-package.zip &&
echo "Success"
