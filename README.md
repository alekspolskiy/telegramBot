# Exhange currency telegram bot
This project is small exchange rate telegram bot which uses exchange rate data.
## How to install
Recommended to use [virtualenv/venv](https://docs.python.org/3/library/venv.html)
or [conda env](https://conda.io/projects/conda/en/latest/index.html).
Python3 should be already installed. Then use pip (or pip3, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```
After requirements was successfully installed use [docker-compose](https://docs.docker.com/):
```
docker-compose up
```
## How to use
When bot launched use commands:

/start - start bot

/help - see what the bot can (all commands with description)

/list or /lst - list of all available rates

/exchange - converts dollars to the second currency. For example:
```
/exchange $10 to CAD 
```
or 
```
/exchange 10 USD to CAD
```
/history - image graph chart which shows the exchange rate graph of the dollars to any selected currency for the last 7 days. For example:
```
/history USD/CAD
```