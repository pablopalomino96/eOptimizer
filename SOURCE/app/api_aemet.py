#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import time
import requests
from config import project_constants as const

def get_weather(city):
    weather_buffer = []
    url = const.AEMET_URL.replace('$CITY', city)
    response = requests.get(url)
    data = response.json()

    if data['estado'] == 200:
        url = data['datos']
        response = requests.get(url)
        data = response.json()[0]
        weather_buffer = create_weather_buffer(data)
        return weather_buffer
    else:
        return None

def create_weather_buffer(data):
    wb = []
    buffer_size = 0
    current_hour = time.strftime("%H")
    prediction_today = data['prediccion']['dia'][0]['estadoCielo']
    prediction_tomorrow = data['prediccion']['dia'][1]['estadoCielo']

    # adds the remaining predictions per hour of the day to the buffer
    for hour in prediction_today:
        if int(hour['periodo']) >= int(current_hour):
            wb.append(hour['descripcion'])
            buffer_size += 1
    # adds tomorrow's predictions per hour until complete the 24 h of the buffer
    for hour in prediction_tomorrow:
        if buffer_size < 24:
            wb.append(hour['descripcion'])
            buffer_size += 1
    return wb
