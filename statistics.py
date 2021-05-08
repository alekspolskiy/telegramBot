import matplotlib.pyplot as plt
import requests
from datetime import datetime, timedelta
from constants import (
    API_ENDPOINT,
    HISTORICAL_ENDPOINT,
)


def get_days_for_weekly_statistic():
    today = datetime.utcnow().date()
    delta = timedelta(days=1)
    days = []
    for day in range(7):
        days.append(datetime.strftime(today, '%Y-%m-%d'))
        today = today - delta
    return days


def get_rates_changes(base: str, symbols: str, app_id):
    params = {
        'app_id': app_id,
        'base': base,
        'symbols': symbols
    }
    daily_rates = {}
    for day in get_days_for_weekly_statistic():
        url = f'{API_ENDPOINT}{HISTORICAL_ENDPOINT.format(date=day)}'
        response = requests.get(url, params=params)
        daily_rates[day] = response.json().get('rates').get(symbols)
    design_graph(daily_rates)


def design_graph(daily_rates: dict):
    x_list = [key[5:] for key, values in daily_rates.items()]
    y_list = [value for key, value in daily_rates.items()]
    plt.cla()
    plt.title('Exchange rates graph')
    plt.xlabel('days')
    plt.ylabel('rate')
    plt.plot(list(reversed(x_list)), list(reversed(y_list)), label='Mark', marker='o')
    plt.savefig('graph.png')
