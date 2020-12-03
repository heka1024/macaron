import datetime
from functools import reduce

from django.core.management.base import BaseCommand
import requests
import re

from food.models import Menu, Restaurant


def parse_menu_row(row, restaurant, now, x):
    def string2price(s):
        try:
            if "," in s:
                return int(s.replace(",", ""))
            return int(s)
        except ValueError:
            return None

    if not row:
        return []

    pattern = re.compile(r'(\D+) +(\d+.\d+)원?')
    matched = pattern.findall(row)
    ret = []
    for i in matched:
        name, price_string = i
        is_vegetarian = False
        without_fork = False
        if '*' in name:
            is_vegetarian = True
            without_fork = True
        elif '#' in name:
            without_fork = True

        price = string2price(price_string)
        if price:
            name_revised = name.replace("&amp", "&")\
                .replace(";", "")\
                .replace("(#)", "")\
                .replace("(*)", "")\
                .replace("&nbsp", "")\
                .replace(" ", "")

            menu = Menu(
                name=name_revised,
                restaurant=restaurant,
                price=price,
                is_vegetarian=is_vegetarian,
                without_fork=without_fork,
                date=now,
                time=x+1
            )
            ret.append(menu)
    return ret


def scrap_menu(date):
    ds = [int(i) for i in date.split('-')]
    now = datetime.date(ds[0], ds[1], ds[2])
    print(now)

    url = f'http://mob.snu.ac.kr/api/findRestMenuList.action?date={date}'
    data = {
        "requestUrl": "http://mob.snu.ac.kr/mob/mcin/mfood/todayFood.html",
        "requestUri": "/mob/mcin/mfood/todayFood.html",
        "ssoCheckYn": "Y",
        "authUrl": "/mob/mcin/mfood/todayFood.html"
    }
    # data = '{"requestUrl":"http://mob.snu.ac.kr/mob/mcin/mfood/todayFood.html","requestUri":"/mob/mcin/mfood/todayFood.html","ssoCheckYn":"Y","authUrl":"/mob/mcin/mfood/todayFood.html"}'
    headers = {'Content-Type': 'application/json; charset=utf-8'}

    res = requests.post(url, json=data, headers=headers).json()['api']
    for r in res:
        code = int(r['code'])
        restaurant = Restaurant.objects.get(code=code)
        helper = lambda row, i: row.split('|') if r[i] and '|' in r[i] else []

        menus = reduce(
            lambda a, i: a + i,
            [parse_menu_row(x, restaurant, now, idx) for (idx, i) in enumerate(('breakfast', 'lunch', 'dinner')) for x in helper(r[i], i)],
            []
        )
        Menu.objects.bulk_create(menus)
        for menu in menus:
            menu.restaurant = restaurant
            menu.save()


        # menus = [r[i].split('|') if r[i] and '|' in r[i] else N`one for i in ]
        # print(code, restaurant, menus)
        # if menus:
        #     print(menus[0], menus[0].restaurant)



class Command(BaseCommand):
    help = 'scrap menu of given date'

    def add_arguments(self, parser):
        parser.add_argument('date', nargs='+')

    def handle(self, *args, **options):
        dates = options['date']
        if dates:
            for date in dates:
                scrap_menu(date)
        else:
            print('give date arguments')
