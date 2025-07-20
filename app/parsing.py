from app.settings import url_avito, driver, url_head_avito
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import datetime
import random
import time
import pandas as pd


def get_page(url):
    driver.get(url)
    
    if 'Авито' in driver.title:
        html = BeautifulSoup(driver.page_source, 'lxml')
        print('Успешное подключение')

    else:
        while not('Авито' in driver.title):
            print('Повторная попытка подключения через 1 минуту...')
            time.sleep(60)
            driver.refresh()

        html = BeautifulSoup(driver.page_source, 'lxml')
        print('Успешное подключение')

    return html

#переход на следующую страницу
def next_page(all_data):
    body = driver.find_element(By.TAG_NAME, 'body')

    for _ in range(16):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

    next_page_button = driver.find_element(By.CSS_SELECTOR, "[data-marker='pagination-button/nextPage']")
    next_page_button.click()

    if 'Авито' in driver.title:
        print('Успешный переход на страницу')
        html = BeautifulSoup(driver.page_source, 'lxml')

    else:
        while not('Авито' in driver.title):
            print('Повторная попытка через 1 мин...')
            time.sleep(60)
            driver.refresh()

        html = BeautifulSoup(driver.page_source, 'lxml')
        print('Успешный переход на страницу')

    return html
    

#получение объявлений
def get_items(html):
    items = html.find_all('div', attrs={'data-marker': 'item'})
    return items


#получение ссылки на объявление
def get_itemLink(item):
    itemLink = url_head_avito + item.find('div', {'class': re.compile(r'iva-item-title')}).find('a')['href']
    return itemLink


#получение имени продавца
def get_name(item):
    try:
        name = item.find('div', attrs={'class': re.compile('iva-item-sellerInfo')}).find('div').find('div').find('a').find('p').contents[0]
    except:
        name = '\'Без имени\''
    return name

#получение даты объявления
def get_date():
    now_date = datetime.datetime.now()
    item_time = f'{now_date.day}.{now_date.month}.{now_date.year}'
    return item_time

#получение адреса
def get_address(item):
    try:
        address = item.find('div', attrs={'class': re.compile('iva-item-content')}).find('div', attrs={'class': re.compile('geo-root')}).find('p').find('span').contents[-1]
    except:
        address = '\'Без адреса\''
    return address

#получение цены товара
def get_price(item):
    try:
        item_price = item.find('p', attrs={'data-marker': 'item-price'}).find('span').contents[0]
    except:
        item_price = '0'
    item_price = item_price.replace('\\', '')
    item_price = item_price.replace('xa', '')
    return item_price


#объединение всей полученной информации
def get_data(html):
    data = []

    items = get_items(html)

    for el in items:
        item_link = get_itemLink(el)
        seller_name = get_name(el)
        item_date = get_date()
        seller_address = get_address(el)
        item_price = get_price(el)

        about_item = {
            'Seller_Name': seller_name,
            'Item_Data': item_date,
            'Address': seller_address,
            'Item_Price': item_price,
            'Item_Link': item_link
        }

        data.append(about_item)

    return data


def process(data):
    df = pd.DataFrame(data)
    out = df.to_json(orient='records', force_ascii=False)[1:-1].replace('},', '},\n').replace('\/', '/')

    with open('DB/DB.json', 'w') as f:
        f.write(out)

    df.to_csv('DB/all_data.csv', index=False)




def start_parsing():
    html = get_page(url_avito)

    all_data = []
    data = get_data(html)

    for el in data:
        all_data.append(el)

    process(data)

    while True:
        try:
            time.sleep(random.randint(5, 7))

            html = next_page(all_data)

            data = get_data(html)

            for el in data:
                all_data.append(el)

            process(all_data)
        except:
            print('It is last page\nParsing end')
            driver.quit()
            break





# if __name__ == "__main__":
#     html = get_page(url_avito)

#     all_data = []
#     data = get_data(html)

#     for el in data:
#         all_data.append(el)

#     process(data)

#     while True:
#         try:
#             all_data = next_page(all_data)
#         except:
#             print('It is last page\nParsing end')
#             driver.quit()
#             break




