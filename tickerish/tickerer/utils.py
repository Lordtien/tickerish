import json
import redis

from django.conf import settings

from tickerer.shrimpy import get_exchanges, get_ticker

redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


def get_exchanges_list():
    response = get_exchanges()

    if (response.status_code == 200 and response.content):
        json_data = json.loads(response.content.decode('utf8'))

        exchanges = []

        for exchange_data in json_data:
            exchanges.append(exchange_data.get('exchange'))
        redis_instance.set('exchanges', json.dumps(exchanges))

        return exchanges

    else:
        # If exchanges API doesn't respond as success, previously fetched exchanges are loaded
        return json.loads(redis_instance.get('exchanges'))


def update_tickers_for_exchange(exchange):
    response = get_ticker(exchange)

    if(response.status_code == 200 and response.content):
        json_data = json.loads(response.content.decode('utf8'))

        tickers = {}

        for ticker_data in json_data:

            # If price is None as received, then -1 is saved instead
            if (ticker_data.get('priceUsd') == None):
                price = -1
            else:
                price = ticker_data.get('priceUsd')

            tickers[ticker_data.get('symbol').lower()] = {
                'price_usd': float(price),
                'last_updated': ticker_data.get('lastUpdated')
            }

        redis_instance.set(exchange, json.dumps(tickers))
    else:
        return response


def rate_convertor(from_currency_rate, to_currency_rate):
    return from_currency_rate / to_currency_rate
