import hmac
import hashlib
import base64
import json
import requests

from django.conf import settings
from django.utils import timezone

api_key = settings.SHRIMPY_API_KEY
secret = settings.SHRIMPY_API_SECRET

base_url = 'https://dev-api.shrimpy.io'


def form_headers(request_path, body, method):
    nonce = int(timezone.now().timestamp() * 1000)
    prehash_string = ''.join([request_path, method, str(nonce), body])
    secret_key = base64.b64decode(secret)
    prehash_string = prehash_string.encode('ascii')

    signature = hmac.new(secret_key, prehash_string, hashlib.sha256)
    signature_b64 = base64.b64encode(signature.digest()).decode('utf-8')

    headers = {
        'Content-Type': 'application/json',
        'DEV-SHRIMPY-API-KEY': api_key,
        'DEV-SHRIMPY-API-NONCE': str(nonce),
        'DEV-SHRIMPY-API-SIGNATURE': signature_b64
    }
    return headers


def get_ticker(exchange):
    request_path = '/v1/exchanges/{}/ticker'.format(exchange)
    body = ''
    method = 'GET'
    headers = form_headers(request_path, body, method)
    return requests.get(base_url + request_path, headers=headers)


def get_exchanges():
    request_path = '/v1/list_exchanges'
    body = ''
    method = 'GET'
    headers = form_headers(request_path, body, method)
    return requests.get(base_url + request_path, headers=headers)
