import requests
import json
from config import keys


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if base == quote:
            raise APIException('Невозможно перевести валюту саму в себя')

        try:
            base_val = keys[base]
        except KeyError:
            raise APIException(f'Проверьте правильность ввода валюты: {base}')

        try:
            quote_val = keys[quote]
        except KeyError:
            raise APIException(f'Проверьте правильность ввода валюты: {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Сумма конвертации <{amount}> имеет не числовое значение')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_val}&tsyms={quote_val}')
        quote_num = json.loads(r.content)[quote_val]
        return quote_num

