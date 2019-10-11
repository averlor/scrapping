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
    # with open('avito.txt', 'a', encoding="utf-8") as f:
    #     info = f"Заголовок: {data['title']}\nURL: {data['url']}\n" \
    #            f"Дата публикации: {data['date']}\nАдрес: " \
    #            f"{data['address']}\nОписание: {data['description']}\n" \
    #            f"Цена: {data['price']}\n" \
    #            f"Номер: {data['number']}\n******\n\n"
    #     # print(info)
    #     f.write(info)

    with open('avito.csv', 'a', encoding="utf-8") as f:
        writer = csv.writer(f);
        writer.writerow((data['title'], data['url'], data['date'],
                         data['address'], data['description'], data['price'], data['number']))


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
            description = ads.find('div', {"class": "description"}).find('a',
                                                                         {
                                                                             "class":
                                                                                 "item_table-extended-description"}).find(
                'span', {"class": "item_table-item-param-label"}).text.strip()
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
    url = 'https://www.avito.ru/krasnodar/kvartiry/sdam/posutochno/1' \
          '-komnatnye?p=1'
    base_url = 'https://www.avito.ru/krasnodar/kvartiry/sdam/posutochno/1-komnatnye?'
    page_part = 'p='

    total_pages = get_total_pages(get_html(url))

    # back total_pages+1
    for i in range(1, 3):
        url_gen = base_url + page_part + str(i)
        html = get_html(url_gen)
        get_page_data(html)


if __name__ == '__main__':
    main()
