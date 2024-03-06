import requests
from yaml import load, dump
from os.path import exists

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

def alarm(baseCurrency, currency, value) -> str:
    return "Alarm! You can buy {amount} of {currency} for {baseCurrency}\n".format(amount=value, baseCurrency=baseCurrency, currency=currency)

def analyzeApiResponse(request: dict, response: dict) -> str:
    toReturn = ""

    for currency in request["currencies"]:
        if "alarm" not in currency: 
            continue

        alarmTreshold = float(currency["alarm"])
        currencyValue = float(response[currency["name"]])

        if alarmTreshold < currencyValue:
            toReturn += alarm(request["baseCurrency"], currency["name"], currencyValue)

    return toReturn

def check(configPath) -> str:
    toReturn = ""

    data = load(open(configPath, 'r'), Loader=Loader)
    key = data["key"]
    if key == "ENTER YOUR KEY":
        return "You haven't included your Freecurrency API key in config.yaml file\n"

    for request in data["requests"]:
        response = requests.get(createApiString(key, request))
        if not response.ok:
            toReturn += "HTTP request error for {baseCurrency} request\n".format(baseCurrency = request["baseCurrency"])
            continue
        responseData = response.json()["data"]
        toReturn += analyzeApiResponse(request, responseData)
        # print(createApiString(key, request))
    
    return toReturn

if __name__ == "__main__":
    alarms = check("my-config.yaml") if exists("my-config.yaml") else check("config.yaml")
    if alarms != "":
        print(alarms, end='')
