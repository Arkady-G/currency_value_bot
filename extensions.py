import requests
import json
from config import keys


class ConvertionException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if quote == base:
            raise ConvertionException('Невозможно конвертировать одинаковые валюты')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}.\nДоступные валюты: /values')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}.\nДоступные валюты: /values')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://api.exchangeratesapi.io/latest?&base={base_ticker}&symbols={quote_ticker}')
        total_base = json.loads(r.content)
        total_base = total_base.pop('rates')[keys[quote]]

        return total_base
