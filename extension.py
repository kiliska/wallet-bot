import requests
import json

from config import *

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(quote, base, amount):
        try:
            quote_key = keys[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")
        try:
            base_key = keys[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        if quote_key == base_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        headers = {
            "apikey": "NWxFeL09G0xSpWw66uDsSsNKvK96pp6G"
        }
        r = requests.get(
            f'https://api.apilayer.com/exchangerates_data/convert?to={quote_key}&from={base_key}&amount={amount}',
            headers=headers)
        text = json.loads(r.content)['result']
        return text
