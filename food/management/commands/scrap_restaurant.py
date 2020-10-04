from django.core.management.base import BaseCommand
import requests

from food.models import Restaurant


class Command(BaseCommand):
    help = 'add restaurant to db'

    def handle(self, *args, **options):
        url = 'http://mob.snu.ac.kr/api/M/new/findRestList.action'
        res = requests.post(url).json()['GRD_SNUCO_RESTAURANT']

        rs = [Restaurant(code=int(r['code']), name=r['restaurant']) for r in res]

        Restaurant.objects.bulk_create(rs)
