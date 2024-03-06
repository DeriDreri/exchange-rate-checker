import check 

def test_default_config():

    #Test for right detection of bad config file
    alarms = check.check("config.yaml")
    assert alarms == "You haven't included your Freecurrency API key in config.yaml file\n", "Perhaps you have changed your config file, then ignore" 

def test_get_api_string():
    #Simple case: USD -> EUR
    testMap = {"baseCurrency": "USD", "currencies": [{"name":"EUR"}] }
    assert check.createApiString("X", testMap) == "https://api.freecurrencyapi.com/v1/latest?apikey=X&currencies=EUR", "Simple test failed"

    #Multiple currencies with default base currency and alarms
    testMap = {"baseCurrency": "USD", "currencies": [{"name":"EUR"},{"name":"PLN", "alarm":"4.0"},{"name":"GBR"}] }
    assert check.createApiString("X", testMap) == "https://api.freecurrencyapi.com/v1/latest?apikey=X&currencies=EUR%2CPLN%2CGBR", "Multiple currencies failed"

    #No default base currency
    testMap = {"baseCurrency": "PLN", "currencies": [{"name":"EUR"}] }
    assert check.createApiString("X", testMap) == "https://api.freecurrencyapi.com/v1/latest?apikey=X&currencies=EUR&base_currency=PLN", "Different currency failed"
