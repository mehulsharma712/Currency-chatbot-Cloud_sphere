from flask import Flask,request
import requests

app = Flask(__name__)

@app.route('/',methods=['POST'])
def index():
    data = request.get_json()
    source_currency=data['queryResult']['parameters']['unit-currency']['currency']
    amount=data['queryResult']['parameters']['unit-currency']['amount']
    target_currency=data['queryResult']['parameters']['currency-name']

    if isinstance(target_currency, list):
        target_currency = target_currency[0]

    print(source_currency)
    print(amount)
    print(target_currency)

    cf=fetch_conversion_factor(source_currency,target_currency)
    final_amount=amount * cf
    print(final_amount)

    return {
        "fulfillmentText": f"{amount} {source_currency} equals {final_amount:.2f} {target_currency}"
    }

def fetch_conversion_factor(source, target):
        url = "https://v6.exchangerate-api.com/v6/af1728b7c74ed1477e6ee1c8/latest/{}".format(source)
        response = requests.get(url).json()
        return response["conversion_rates"][target]

if __name__ == '__main__':
    app.run(debug=True)