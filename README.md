## Venmo Ynab Importer
This repo is a function that pulls in transactions from Venmo and uploads them to Ynab. It's smart enough to not repeat transactions, and will update existing transactions when they are cleared.

### Requirements
- Venmo access token
- Venmo username
- Ynab token
- Ynab budget id
- Ynab account id

### Venmo Authorization
Use `authorizer.py` to generate a Venmo access token

### Deploy to lambda
`./upload.sh`
