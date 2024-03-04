import requests
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def createApiString(key: str, requestMap: dict) -> str:
    toReturn = "https://api.freecurrencyapi.com/v1/latest?apikey=" + key + "&currencies="
    
    for currency in requestMap["currencies"]:
        toReturn += currency["name"] + "%2C"
    toReturn = toReturn[:-3]
    
    toReturn = toReturn if requestMap["baseCurrency"] == "USD" else toReturn + "&base_currency=" + requestMap["baseCurrency"] 
    
    return toReturn

def alarm(baseCurrency, currency, value):
    print("Alarm! You can buy {amount} of {currency} for {baseCurrency}".format(amount=value, baseCurrency=baseCurrency, currency=currency))

def analyzeApiResponse(request: dict, response: dict):
    for currency in request["currencies"]:
        if "alarm" not in currency: 
            continue

        alarmTreshold = float(currency["alarm"])
        currencyValue = float(response[currency["name"]])

        if alarmTreshold < currencyValue:
            alarm(request["baseCurrency"], currency["name"], currencyValue)

def main():
    data = load(open("config.yaml", 'r'), Loader=Loader)
    key = data["key"]

    for request in data["requests"]:
        response = requests.get(createApiString(key, request)).json()["data"]
        analyzeApiResponse(request, response)
        # print(createApiString(key, request))

if __name__ == "__main__":
    main()
