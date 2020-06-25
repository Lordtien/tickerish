# tickerish
Ticker server

1. Clone the repo
   `git clone https://github.com/Lordtien/tickerish.git`

2. cd into the repository.
   `cd tickerish`

3. Create a virtual environment using Python 3.8 (Recommended)
   `virtualenv -p=python3.8 venv`

   Install Python 3.8 if necessary.

4. Use virtual environment.
   `source venv\bin\activate`

5. Install requirements.
   `pip install -r requirements.txt`

6. Install Redis. [Follow these instructions](https://redis.io/topics/quickstart)
   
7. Run Celery beat.
   `celery -A tickerish beat -l info`

8. Run Celery worker.
   `celery -A tickerish worker -l info`

9. Hit it! [Get BTC to ETH rate in Bitfinex](http://localhost:8000/tickerer/exchange-rate/?exchange=bitfinex&fromCurrency=btc&toCurrency=eth)