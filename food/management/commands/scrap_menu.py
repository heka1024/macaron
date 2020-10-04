from django.core.management.base import BaseCommand
import requests


def scrap_menu(date):
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
        print(r)

    pass


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
