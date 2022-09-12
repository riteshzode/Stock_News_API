import requests
from twilio.rest import Client

STOCK = "META"  # Company symbol
COMPANY_NAME = "Meta Platforms Inc"  # Company Name

# Needed

######################################################################################################

# STEP 1: Use https://www.alphavantage.co
# Price Api

STOCK_ENDPOINT = 'https://www.alphavantage.co/query?'
STOCK_API_KEY = "STOCK_API_KEY"

# STEP 2: Use https://newsapi.org
# News Api
NEWS_ENDPOINT = "https://newsapi.org/v2/everything?"
NEWS_API = "NEWS_API"

# STEP 3: Use https://www.twilio.com

account_sid = "account_sid"
auth_token = "auth_token"

twilio_from_no = "twilio_from_no"
twilio_to_no = "twilio_to_no"

######################################################################################################

# STEP 1

stock_para = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}

r1 = requests.get(STOCK_ENDPOINT, params=stock_para)

list = [value for key, value in r1.json()["Time Series (Daily)"].items()]

yesterday = float(list[0]["4. close"])

day_before_yesterday = float(list[1]["4. close"])

diff = yesterday - day_before_yesterday

up_down = None

if diff > 0:
    up_down = "⬆️"
else:
    up_down = "⬇️"

diff_percent = round(abs(diff) * 100 / day_before_yesterday, 2)

if diff_percent > 0:

    # STEP 2

    news_para = {
        "q": COMPANY_NAME,
        "apiKey": NEWS_API
    }

    r2 = requests.get(NEWS_ENDPOINT, params=news_para)

    article = [
        f"{STOCK} :{abs(diff_percent)}% {up_down} \nHeadline : {i['title']}. \nBrief: {i['description']}\nURl : {i['url']}\n"
        for i in r2.json()["articles"][:3]]

    # STEP 3:

    for i in article:
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
            body=i,
            from_=twilio_from_no,
            to=twilio_to_no
        )

        print(message.status)
