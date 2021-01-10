import requests
import json
from config import keys
class ApiExeptions(Exception):
    pass

class API:
    @staticmethod
    def get_price(quote:str, base:str,amount:str):

        if quote == base:
            raise ApiExeptions(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ApiExeptions(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ApiExeptions(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ApiExeptions(f'Не удалось обработать количество {amount}')
        para = {'base': quote_ticker, 'symbols': base_ticker}
        r = requests.get('https://api.exchangeratesapi.io/latest', params=para)
        text = float(amount) * float(json.loads(r.content)['rates'][base_ticker])
        return text
        # para = {'base': quote, 'symbols': base}
        # r = requests.get('https://api.exchangeratesapi.io/latest', params=para)
        # text = float(amount) * float(json.loads(r.content)['rates'][base])
        # return text




