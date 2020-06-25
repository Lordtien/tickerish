import redis
import json

from datetime import datetime

from django.http import JsonResponse
from django.utils import timezone
from django.conf import settings

from tickerer.utils import rate_convertor

redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


def get_exchange_rate(request):
    # Check for GET requests
    if request.method != 'GET':
        return JsonResponse({
            'error': 'Only GET requests are served.'
        })

    # Check for request params
    if (request.GET.get('exchange', '') and
        request.GET.get('fromCurrency', '') and
            request.GET.get('toCurrency', '')):

        exchange = request.GET.get('exchange')
        from_currency = request.GET.get('fromCurrency')
        to_currency = request.GET.get('toCurrency')

        # Check and extraction of exchange
        exchange_data = redis_instance.get(exchange.lower())
        if (exchange_data == None):
            return JsonResponse({
                'error': 'Exchange unavailable.'
            })
        exchange_data = json.loads(exchange_data)

        # Check and extraction of fromCurrency
        from_ticker = exchange_data.get(from_currency.lower(), '')
        if (from_ticker == ''):
            return JsonResponse({
                'error': '{} unavailable in {} exchange'.format(from_currency, exchange)
            })

        # Check and extraction of to_currency
        to_ticker = exchange_data.get(to_currency.lower(), '')
        if (to_ticker == ''):
            return JsonResponse({
                'error': '{} unavailable in {} exchange'.format(to_currency, exchange)
            })

        # Check for fromCurrency's priceUsd = 0 (If null prices are received, they're saved as 0)
        from_ticker_price = from_ticker['price_usd']
        if (from_ticker_price == 0):
            return JsonResponse({
                'error': '{} is temporarily unavailable at {} or no longer supported.'.format(
                    from_currency,
                    exchange
                )
            })

        # Check for toCurrency's priceUsd = 0 (If null prices are received, they're saved as -1)
        to_ticker_price = to_ticker['price_usd']
        if (to_ticker_price == -1):
            return JsonResponse({
                'error': '{} is temporarily unavailable at {} or no longer supported.'.format(
                    to_currency,
                    exchange
                )
            })

        # Check for time differences
        threshold_time = timezone.now() - timezone.timedelta(seconds=60)

        from_ticker_time = datetime.strptime(
            from_ticker['last_updated'], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
        to_ticker_time = datetime.strptime(
            to_ticker['last_updated'], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
        if (from_ticker_time < threshold_time or to_ticker_time < threshold_time):
            return JsonResponse({
                'error': 'Updated tickers unavailable.'
            })

        return JsonResponse({
            'rate': rate_convertor(from_ticker_price, to_ticker_price)
        })

    else:
        return JsonResponse({
            'error': 'Too few or wrong parameters.'
        })
