from celery.decorators import task, periodic_task
from celery.utils.log import get_task_logger

from django.utils import timezone

from tickerer.utils import get_exchanges_list, update_tickers_for_exchange

logger = get_task_logger(__name__)


@periodic_task(run_every=timezone.timedelta(seconds=20), name="update_ticker_data", ignore_result=True)
# Periodic task that runs every 30 seconds and fetches all ticker prices for all exchanges
def update_ticker_data():
    """Updates ticker data at a fixed interval"""
    logger.info("Updated tickers successfully at {}".format(timezone.now()))

    exchanges = get_exchanges_list()

    for exchange in exchanges:
        print('Fetching ticker prices for {}'.format(exchange))
        update_tickers_task.delay(exchange)


@task(bind=True, name="update_tickers_for_exchange", max_retries=2)
# Task that fetches ticker prices for a particular exchange. Triggered by the periodic task
def update_tickers_task(self, exchange):
    """Updates tickers for an exchange"""
    try:
        if update_tickers_for_exchange(exchange):
            raise Exception
    except Exception as exc:
        self.retry(exc=exc)
