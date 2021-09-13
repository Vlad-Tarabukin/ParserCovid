import csv

import requests
from bs4 import BeautifulSoup

worldURL = 'https://coronavirus.jhu.edu/map.html'  # Сайт с данными по миру
countryURL = 'https://xn--80aesfpebagmfblc0a.xn--p1ai/'  # Сайт с данными по стране
regionURL = 'https://xn--b1ag8a.xn--p1ai/%D1%81%D1%82%D0%BE%D0%BF%D0%B2%D0%B8%D1%80%D1%83%D1%81'  # Сайт с данными по области

total_states = []
file_path = 'covid.csv'


def get_html(URL):  # Получаем HTML файл сайта
    r = requests.get(URL)
    return r


def parse_world():
    response = requests.get('https://jhucoronavirus.azureedge.net/jhucoronavirus/homepage-featured-stats.json')
    if response.ok:
        world_cases = response.json()['cases']['global']
        world_deaths = response.json()['deaths']['global']
        print('В мире: \n', 'Заболевших:', world_cases, '\n', 'Смертей:', world_deaths, '\n')
        total_states.append(world_cases)
        total_states.append(world_deaths)


def parse_country():
    soup = BeautifulSoup(get_html(countryURL).text, 'html.parser')
    country_cases = soup.find('div', class_='cv-countdown__item-value _accent').find('span').text.replace(' ', '')
    country_deaths = soup.findAll('div', class_='cv-countdown__item')[4].find('div',
                                                                              class_='cv-countdown__item-value').find(
        'span').text.replace(' ', '')
    print('В России: \n', 'Заболевших', country_cases, '\n', 'Смертей:', country_deaths, '\n')
    total_states.append(country_cases)
    total_states.append(country_deaths)


def parse_region():
    soup = BeautifulSoup(get_html(regionURL).text, 'html.parser')
    details = soup.find('div', class_='content').findAll('p')[1].text.replace('.', '').split(' ')
    region_cases = soup.find('table', class_='region-table').find('span').text
    region_deaths = soup.find('table', class_='region-table').findAll('td')[2].find('span').text
    last_num = 0
    states = []
    i = 0
    for word in details:
        if word[0].isdigit():
            if last_num != 0:
                states.append(str(last_num) + str(word))
                last_num = 0
            else:
                last_num = word
                if not details[i + 1][0].isdigit():
                    states.append(last_num)
                    last_num = 0
        i += 1
    region_heavy_cases = states[1]
    region_reanimation = states[2]
    region_mechanical_ventilaion = states[3]
    region_medium_heavy_cases = states[4]
    print('В Свердловской обл:\n', 'Заболевания:', region_cases, '\n', 'Смерти:', region_deaths, '\n',
          'Тяжкие заболевания:',
          region_heavy_cases, '\n', 'Заболевшие в реанимации:', region_reanimation, '\n',
          'Заболевших на аппаратах ИВЛ:',
          region_mechanical_ventilaion, '\n', 'Заболевания средней тяжести:', region_medium_heavy_cases)
    total_states.append(region_cases)
    total_states.append(region_deaths)
    total_states.append(region_heavy_cases)
    total_states.append(region_reanimation)
    total_states.append(region_mechanical_ventilaion)
    total_states.append(region_medium_heavy_cases)


parse_world()
parse_country()
parse_region()
try:
    file = open(file_path, 'r', newline='')
    file = open(file_path, 'a', newline='')
    writer = csv.writer(file, delimiter=';')
    writer.writerow(
        [total_states[0], total_states[1], total_states[2], total_states[3], total_states[4], total_states[5],
         total_states[6], total_states[7], total_states[8], total_states[9]])
except FileNotFoundError:
    file = open(file_path, 'w', newline='')
    writer = csv.writer(file, delimiter=';')
    writer.writerow([''])
    writer.writerow(
        [total_states[0], total_states[1], total_states[2], total_states[3], total_states[4], total_states[5],
         total_states[6], total_states[7], total_states[8], total_states[9]])
