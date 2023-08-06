import inspect

import requests
from simplejson import JSONDecodeError
import json

from src.phinix.exceptions import *


def validate_response(response: dict) -> bool:
    return response.get('success') or str(response.get('success')).lower() == 'true'


def get_token(mobile_number: str, password: str) -> str:
    func_name = inspect.currentframe().f_code.co_name

    payload = json.dumps({
        "mobile_number": mobile_number,
        "password": password
    })
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        r = requests.post('https://api.phinix.ir/auth/login', headers=headers, data=payload)
    except Exception as e:
        raise RequestsExceptions(func_name, e)

    status_code = r.status_code

    if status_code == 200:
        try:
            resp = r.json()
        except JSONDecodeError as e:
            raise JsonDecodingError(func_name, e)

        if validate_response(resp):
            return resp.get('result').get('token')
        else:
            raise JsonDecodingError(func_name, r.text)
    else:
        raise StatusCodeError(func_name, status_code, r.text)


class Phinix:
    def __init__(self, token: str):
        self.base_url = "https://api.phinix.ir/v1/"
        self.session = requests.Session()
        self.session.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        pass

    def order_book(self, symbol: str):
        func_name = inspect.currentframe().f_code.co_name
        try:
            r = self.session.get(self.base_url + f'depth?symbol={symbol}')
        except Exception as e:
            raise RequestsExceptions(func_name, e)

        status_code = r.status_code

        if status_code == 200:
            try:
                resp = r.json()
            except JSONDecodeError as e:
                raise JsonDecodingError(func_name, e)

            if validate_response(resp):
                return resp.get('result')
            else:
                raise JsonDecodingError(func_name, r.text)

        else:
            raise StatusCodeError(func_name, status_code, r.text)

    def all_recent_trades(self, symbol: str):
        func_name = inspect.currentframe().f_code.co_name
        try:
            r = self.session.get(self.base_url + f'trades?symbol={symbol}')
        except Exception as e:
            raise RequestsExceptions(func_name, e)

        status_code = r.status_code

        if status_code == 200:
            try:
                resp = r.json()
            except JSONDecodeError as e:
                raise JsonDecodingError(func_name, e)

            if validate_response(resp):
                return resp.get('result')
            else:
                raise JsonDecodingError(func_name, r.text)

        else:
            raise StatusCodeError(func_name, status_code, r.text)

    def all_balances(self):
        func_name = inspect.currentframe().f_code.co_name
        try:
            r = self.session.get(self.base_url + 'account/balances')
        except Exception as e:
            raise RequestsExceptions(func_name, e)

        status_code = r.status_code

        if status_code == 200:
            try:
                resp = r.json()
            except JSONDecodeError as e:
                raise JsonDecodingError(func_name, e)

            if validate_response(resp):
                return resp.get('result').get('balances')
            else:
                raise JsonDecodingError(func_name, r.text)

        else:
            raise StatusCodeError(func_name, status_code, r.text)

    def coin_balance(self, coin: str):
        coin = coin.upper()
        func_name = inspect.currentframe().f_code.co_name
        try:
            r = self.session.get(self.base_url + 'account/balances')
        except Exception as e:
            raise RequestsExceptions(func_name, e)

        status_code = r.status_code

        if status_code == 200:
            try:
                resp = r.json()
            except JSONDecodeError as e:
                raise JsonDecodingError(func_name, e)

            if validate_response(resp):
                return resp.get('result').get('balances').get(coin)
            else:
                raise JsonDecodingError(func_name, r.text)

        else:
            raise StatusCodeError(func_name, status_code, r.text)

    def coin_available_balance(self, coin: str):
        coin = coin.upper()
        func_name = inspect.currentframe().f_code.co_name
        try:
            r = self.session.get(self.base_url + 'account/balances')
        except Exception as e:
            raise RequestsExceptions(func_name, e)

        status_code = r.status_code

        if status_code == 200:
            try:
                resp = r.json()
            except JSONDecodeError as e:
                raise JsonDecodingError(func_name, e)

            if validate_response(resp):
                _ = resp.get('result').get('balances').get(coin)
                return float(_.get('value')) - float(_.get('locked'))
            else:
                raise JsonDecodingError(func_name, r.text)

        else:
            raise StatusCodeError(func_name, status_code, r.text)

    def create_order(self, price: str, quantity: str, side: str, symbol: str, type_: str, client_id: str = None):
        func_name = inspect.currentframe().f_code.co_name

        try:
            payload = json.dumps({
                "price": price,
                "quantity": quantity,
                "side": side.lower(),
                "symbol": symbol.upper(),
                "type": type_.lower(),
                "client_id": client_id,
            })
            r = self.session.post(self.base_url + 'account/orders', data=payload)
        except Exception as e:
            raise RequestsExceptions(func_name, e)

        status_code = r.status_code

        if status_code == 200:
            try:
                resp = r.json()
            except JSONDecodeError as e:
                raise JsonDecodingError(func_name, e)

            if validate_response(resp):
                return resp.get('result')
            else:
                raise JsonDecodingError(func_name, r.text)

        else:
            raise StatusCodeError(func_name, status_code, r.text)

    def cancel_order(self, client_id: str):
        func_name = inspect.currentframe().f_code.co_name

        try:
            payload = json.dumps({
                "clientOrderId": client_id
            })
            r = self.session.delete(self.base_url + 'account/orders', data=payload)
        except Exception as e:
            raise RequestsExceptions(func_name, e)

        status_code = r.status_code

        if status_code == 200:
            try:
                resp = r.json()
            except JSONDecodeError as e:
                raise JsonDecodingError(func_name, e)

            if validate_response(resp):
                return resp.get('result')
            else:
                raise JsonDecodingError(func_name, r.text)

        else:
            raise StatusCodeError(func_name, status_code, r.text)

    def open_orders(self, symbol: str):
        func_name = inspect.currentframe().f_code.co_name

        try:
            r = self.session.delete(self.base_url + f'account/openOrders?symbol={symbol.upper()}')
        except Exception as e:
            raise RequestsExceptions(func_name, e)

        status_code = r.status_code

        if status_code == 200:
            try:
                resp = r.json()
            except JSONDecodeError as e:
                raise JsonDecodingError(func_name, e)

            if validate_response(resp):
                return resp.get('result').get('orders')
            else:
                raise JsonDecodingError(func_name, r.text)

        else:
            raise StatusCodeError(func_name, status_code, r.text)

    def user_recent_trades(self, symbol: str = None, side: str = None, active: bool = None):
        func_name = inspect.currentframe().f_code.co_name

        params = {}

        if symbol:
            params.update({'symbol': symbol.upper()})
        if side:
            params.update({'side': side.lower()})
        if active:
            params.update({'active': active})

        try:
            r = self.session.get(self.base_url + f'account/trades', params=params)
        except Exception as e:
            raise RequestsExceptions(func_name, e)

        status_code = r.status_code

        if status_code == 200:
            try:
                resp = r.json()
            except JSONDecodeError as e:
                raise JsonDecodingError(func_name, e)

            if validate_response(resp):
                return resp.get('result').get('AccountLatestTrades')
            else:
                raise JsonDecodingError(func_name, r.text)

        else:
            raise StatusCodeError(func_name, status_code, r.text)
