# tickerish
Ticker server

## Setup
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

6. Install Redis, start Redis Server and check if it is working. [Follow these instructions](https://redis.io/topics/quickstart)

7. Run server
   `python3.8 manage.py runserver`
   
8.  Run Celery beat.
   `celery -A tickerish beat -l info`

11. Run Celery worker.
   `celery -A tickerish worker -l info`

10. Wait for it.... (2-3 minutes, just to be safe)

11. Hit it! [Get BTC to ETH rate in Bitfinex](http://localhost:8000/tickerer/exchange-rate/?exchange=bitfinex&fromCurrency=btc&toCurrency=eth)

12. To check server response time, check `X-Data-Generation-Duration-ms` response header. Alternatively, go through the network tab in developer console and reload the page.

13. To monitor celery tasks, run:
    `celery flower -A tickerish --address=127.0.0.1 --port=5555`
    and open [this](http://localhost:5555/)

## Known issues
1. `Error: Updated tickers unavailable.` encountered some times.
   Possible explanation: Prices are updated by source of truth once per minute and fetched by server thrice per minute. Ideally, it shouldn't sustain for more than 20 seconds, given that third party API responds at all times.

2. Difference in response time header and developer console.
   Possible explanation: Since the header time doesn't include the time taken between the server and the client, it will always be lower (<10 ms locally)
