import requests
import telebot
import json
import os
import db
from datetime import datetime, timedelta
from statistics import get_rates_changes
from constants import (
    API_ENDPOINT,
    LATEST_ENDPOINT,
)


def round_to_two_decimals(num_obj, digits=2):
    return f"{num_obj:.{digits}f}"


def get_latest(app_id):
    url = f'{API_ENDPOINT}{LATEST_ENDPOINT}'
    params = {
        'app_id': app_id,
        'base': 'USD'
    }
    response = requests.get(url, params=params)
    db.set_last_request()
    rates = response.json().get('rates')
    db.clear_table()
    rate = ''
    for count, data in enumerate(rates.items(), start=1):
        rate += f'{data[0]} {round_to_two_decimals(data[1])}\n'
        db.save_currency_exchanges_to_db(count, data[0], str(round_to_two_decimals(data[1])))
    return rate


def convert(value, currency_to):
    exchange_rate = float(db.get_currency_rate(currency_to)[0])
    value = value.replace('$', '')
    return f'{float(value)*exchange_rate}'


def check_last_request(app_id):
    time_to_new_request = timedelta(minutes=10)
    last_request = db.get_last_request()[0][0] if db.get_last_request() else datetime.utcnow() - time_to_new_request
    now = datetime.utcnow()
    delta = now - last_request
    if delta > time_to_new_request:
        return get_latest(app_id)
    else:
        rate = ''
        for rates in db.get_all_currency_exchanges_data():
            rate += f'{rates[0]} {rates[1]}\n'
        return rate


def telegram_bot(token, app_id):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, '''Hi there!
Type /help to see what I can do
        ''')

    @bot.message_handler(commands=['help'])
    def send_text(message):
        bot.send_message(message.chat.id, '''
Choose the command:
/list or /lst - list of all available rates,
/exchange - converts dollars to the second currency. For example:
'/exchange $10 to CAD' or '/exchange 10 USD to CAD',
/history - image graph chart which shows the exchange rate graph of the dollars to any selected currency for the last 7 days. For example:
'/history USD/CAD'
        ''')

    @bot.message_handler(commands=['list', 'lst'])
    def send_text(message):
        bot.send_message(message.chat.id, check_last_request(app_id))

    @bot.message_handler(commands=['exchange'])
    def send_text(message):
        user_message = message.text.upper()
        try:
            value = user_message.split(' ')[1]
            currency_to = user_message.split(' ')[-1]
            bot.send_message(message.chat.id, convert(value, currency_to))
        except:
            bot.send_message(message.chat.id, 'Check that you wrote the command correctly')

    @bot.message_handler(commands=['history'])
    def send_text(message):
        try:
            user_message = message.text.upper()
            base = user_message.split(' ')[1].split('/')[0]
            symbols = user_message.split('/')[-1]
            get_rates_changes(base, symbols, app_id)
            img = open('graph.png', 'rb')
            bot.send_photo(message.chat.id, img)
            img.close()
            os.remove('graph.png')
        except:
            bot.send_message(message.chat.id, 'Сheck that you wrote the command correctly')

    bot.polling()


def main():
    with open('./config.json', 'r') as file:
        CONFIG = json.load(file)

    telegram_bot(CONFIG.get('bot_token'), CONFIG.get('app_id'))


if __name__ == '__main__':
    main()
