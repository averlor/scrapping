# -*- coding: utf-8 -*-
import csv
import requests
from bs4 import BeautifulSoup


def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', {'class': "pagination-pages"}).find_all('a',
                                                                     {
                                                                         'class': 'pagination-page'})[
        -1].get('href')
    total_pages = int(pages.split('=')[1].split('&')[0])

    return total_pages


def write_file(data):
    with open('avito.csv', 'a', encoding="utf-8") as f:
        writer = csv.writer(f);
        writer.writerow((data['title'], data['url'], data['date'],
                         data['address'], data['description'], data['price'], data['number']))


def get_detail_page_data(html):

    html = get_html(html)
    detail_soup = BeautifulSoup(html, 'lxml')

#     ищем desciption и number


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads_list = soup.find('div', {"class": "catalog-list"}).find_all('div',
                                                                    {"class":
                                                                         "item_table"})
    for ads in ads_list:
        # title, url, date, address, description, price, number
        try:
            title = ads.find('div', {'class': 'description'}).find(
                'h3').text.strip()
        except:
            title = ''

        try:
            url = 'https://www.avito.ru' + ads.find('div', {
                'class': 'description'}).find(
                'h3').find('a').get('href')
        except:
            url = ''

        try:
            date = ads.find('div', {"class": "description"}).find('div',
                                                                  {"class":
                                                                       "data"}).find(
                "div", {"class": "item-date"}).find("div").text.strip()

        except:
            date = ''

        try:
            address = ads.find('div', {"class": "description"}).find('span',
                                                                     {"class":
                                                                          "item-address__string"}).text.strip()
        except:
            address = ''

        try:
            description_url = get_html(url)

        except:
            description = ''

        try:
            price = ads.find('div', {"class": "description"}).find('div',
                                                                   {"class":
                                                                        "about"}).find(
                'span', {"class": "price"}).text.strip()
        except:
            price = ''

        try:
            number = '899994575659'
        except:
            number = ''

        data = {
            "title": title,
            "url": url,
            "date": date,
            "address": address,
            "description": description,
            "price": price,
            "number": number
        }

        # print(price)
        write_file(data)


def main():

    price_max = int(input('масимальная цена: '))
    district = input('предпочитаемый район: ')

    if (district.lower() == 'западный'):
        district = 359
    elif (district.lower() == 'карасунский'):
        district = 360
    elif (district.lower() == 'прикубанский'):
        district = 361
    elif (district.lower() == 'старокорсунская'):
        district = 547
    elif (district.lower() == 'центральный'):
        district = 362
    else:
        district=''

    params = {
        "price_max": str(price_max),
        'district': district
    }

    base_url = 'https://www.avito.ru/krasnodar/kvartiry/sdam/posutochno/?'
    page_part = 'p='
    query_params = f'pmax={params["price_max"]}&district={params["district"]}'
    url = f'https://www.avito.ru/krasnodar/kvartiry/sdam/posutochno/?{query_params}'

    total_pages = get_total_pages(get_html(url))

    # back total_pages+1
    for i in range(1, 3):
        url_gen = base_url + page_part + str(i) + '&' + query_params
        html = get_html(url_gen)
        get_page_data(html)


if __name__ == '__main__':
    main()
