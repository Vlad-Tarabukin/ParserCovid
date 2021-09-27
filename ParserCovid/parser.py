# Парсер для сайтов с данными по короновирусу, полученные данные выводятся в буфер обмена вместе с датой использования скрипта, каждые значения отделяются табуляцией (TAB)
# Принимаются только данные на настоящий день т.е. обновлялись сегодня

import datetime  # Библ. узнающая сегодняшнее число
import re  # Библ. regular expression

import pyperclip as pc  # Библ. имеющая доступ к буферу обмена
# Библеотеки
import requests  # Библ. предоставляющая доступ программе к сайтам или файлам в сети
from bs4 import BeautifulSoup  # Библ. читающая HTML страницу

worldURL = 'https://jhucoronavirus.azureedge.net/jhucoronavirus/homepage-featured-stats.json'  # JSON файл с данными по миру
countryURL = 'https://xn--80aesfpebagmfblc0a.xn--p1ai/'  # Сайт с данными по стране
regionURL = 'https://xn--b1ag8a.xn--p1ai/%D1%81%D1%82%D0%BE%D0%BF%D0%B2%D0%B8%D1%80%D1%83%D1%81'  # Сайт с данными по области


def get_file(URL):  # Функция получаящая файл с сайта
    r = requests.get(URL)
    return r


def parse_world():  # Функция достающая данные из сайта мира
    response = get_file(worldURL)  # Файл с данными
    if response.ok:  # Проверка файла
        world_update_date = int(
            re.search(r'\d+', response.headers.get('Last-Modified')).group(0))  # Получаем дату обновления файла
        if world_update_date == datetime.date.today().day:  # Проверка свежести файла
            world_cases = response.json()['cases']['global']  # Достаём количество заболеваний
            world_deaths = response.json()['deaths']['global']  # Достаём количество смертей
            return [world_cases, world_deaths]
        else:  # Если же файл устаревший то возвращаем пустые значения
            return ['', '']


def parse_country():  # Функция достающая данные из сайта страны
    soup = BeautifulSoup(get_file(countryURL).text, 'html.parser')  # Получаем HTML элементы страницы
    country_update_date = soup.find('div', class_='cv-banner__description').text  # Получаем дату обновления файла
    if int(re.search(r'\d+', country_update_date)[0]) == int(datetime.date.today().day):  # Проверка свежести файла
        country_cases = soup.find('div', class_='cv-countdown__item-value _accent').find('span').text.replace(' ',
                                                                                                              '')  # Достаём количество заболеваний
        country_deaths = soup.findAll('div', class_='cv-countdown__item')[4].find('div',
                                                                                  class_='cv-countdown__item-value').find(
            'span').text.replace(' ', '')  # Достаём количество смертей
        return [country_cases, country_deaths]
    else:  # Если же файл устаревший то возвращаем пустые значения
        return ['', '']


def parse_region():  # Функция достающая данные из сайта области
    soup = BeautifulSoup(get_file(regionURL).text, 'html.parser')  # Получаем HTML элементы страницы
    details = soup.find('div', class_='content').findAll('p')[1].text.replace(' ', '')  # Получаем большой текст с данными
    region_update_date = soup.find('div', class_='content').findAll('span')[1].text  # Получаем дату обновления файла
    if int(re.search(r'\d+', region_update_date)[0]) == int(datetime.date.today().day):  # Проверка свежести файла
        region_cases = soup.find('table', class_='region-table').find('span').text  # Достаём количество заболеваний
        region_deaths = soup.find('table', class_='region-table').findAll('td')[2].find('span').text  # Достаём количество смертей
        values = re.findall(r'\d+', details)

        return [region_cases, region_deaths, values[1], values[2], values[3], values[4]]
    else:  # Если же файл устаревший то возвращаем пустые значения
        return ['', '', '', '', '', '']


date = (str(datetime.date.today()).replace('-', '.'))  # Сегодняшнее число
world_states = parse_world()  # Данные по миру
country_states = parse_country()  # Данные по стране
region_states = parse_region()  # Данные по области

pc.copy(f'{date}\t{world_states[0]}\t{world_states[1]}\t{country_states[0]}\t{country_states[1]}\t{region_states[0]}\t'  # Копирование в буфер обмена
        f'{region_states[1]}\t{region_states[2]}\t{region_states[3]}\t{region_states[4]}\t{region_states[5]}')
