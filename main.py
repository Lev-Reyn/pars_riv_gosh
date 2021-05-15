from bs4 import BeautifulSoup
import requests
import json
import csv

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 YaBrowser/21.3.0.740 Yowser/2.5 Safari/537.36',
    'accept': '*/*'
}

URL = 'https://rivegauche.ru/category/parfyumeriya-3/zhenskie-aromaty-4'
lst_with_inf = []


def parser():
    r = requests.get(url=URL, headers=HEADERS)

    soup = BeautifulSoup(r.text, 'lxml')
    items = soup.find_all('div', class_='col-6 col-md-4 px-2 mb-3 d-flex flex-wrap ng-star-inserted')
    for item in items:
        link = 'https://rivegauche.ru' + \
               item.find('a', {'class': 'b-product-item__title d-flex h-50 f-w600 ng-star-inserted'})['href']
        name = item.find('a', {'class': 'b-product-item__title d-flex h-50 f-w600 ng-star-inserted'}).text.strip()
        price = item.find('span', class_='ng-star-inserted').text.strip()
        if 'от ' in price:
            price = price[3::]
        description = item.find('div',
                                class_='pt-3 pb-1 fs-small line text-black-50 b-product-item__subtitle w-100 d-flex h-50').text.strip()
        lst_with_inf.append({
            'name': name,
            'link': link,
            'price': price,
            'description': description
        })


def parser_json():
    global lst_with_inf
    for i in range(85):
        url = f'https://api.rivegauche.ru/rg/v1/newRG/products/search?fields=FULL&currentPage={i}&pageSize=24&categoryCode=Perfumery_Woman&tag=7133082534944522'
        r = requests.get(url, headers=HEADERS)
        data = r.json()
        items = data['results']
        for item in items:
            try:
                name = item['name']
            except:
                name = None
            try:
                link = 'https://rivegauche.ru' + item['url']
            except:
                link = None
            try:
                description = item['description']
            except:
                description = None
            try:
                price = int(item['price']['value'])
            except:
                price = None
            lst_with_inf.append({
                'name': name,
                'link': link,
                'price': price,
                'description': description
            })
        print(f'прошли по {i} странице из 85')

    with open('data.json', 'w') as file:
        json.dump(lst_with_inf, file, indent=4, ensure_ascii=False)

    with open('data.json') as file:
        lst_with_inf = json.load(file)

    with open('data.csv', 'w') as file:
        fieldnames = ['name', 'link', 'price', 'description']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in lst_with_inf:
            writer.writerow(row)


if __name__ == '__main__':
    parser_json()
