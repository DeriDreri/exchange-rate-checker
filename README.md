# exchange-rate-checker
Python scripts meant to provide an automatic currencies check via FreeCurrencyAPI. The script support alarms for minimal exchange values to raise an alarm for.

## How to use
### Get your FreecurrencyAPI key
Go to FreecurrencyAPI and quickly register for free to get your key
```
https://freecurrencyapi.com/
```
At 4th March 2024 the API supports only 10 requests per minute but 5,000 requests per month. As the script was meant to be used as a daily chron job on a private Linux server, this should be more than needed. 

### Configure requests
Go to config.yaml and follow the instructions in first line to configure the requests and alarm you desire

### (Optionally) Configure alarm behaviour 
By default the script simply prints alarms to standard output which are then meant to be used by different scripts or alternatievly acknowledged by the user themselves. However, you can easily modify the default behaviour by modyfing `alarm` function in `check.py`

### Run the script by hand or in a different script
To call the script simply use:
```
python3 check.py
```
