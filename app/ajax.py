# coding=utf-8

from django.http.response import JsonResponse
from django.views.generic import View
from json import loads as json_loads
from datetime import date

from models import SearchHistory, Terms
from core.WF_Google_Search import getGoogleSearch


def invalid(message):
    print 'invalid'
    print message
    return JsonResponse({
        'code': 1,
        'message': message,
        'data': {}
    })


MAX_COUNT = 10

class GoogleSearchView(View):
    class Response(object):
        @classmethod
        def ok(cls, value, limit=0):
            return JsonResponse({
                'code': 200,
                'message': 'OK',
                'data': {
                    'result': value,
                    'limit': limit
                },
            })

    def get(self, request):
        try:
            if SearchHistory.objects.filter(search_dt=date.today()):
                sh = SearchHistory.objects.get(search_dt=date.today())
                if sh.search_count < MAX_COUNT:
                    sh.search_count += 1
                    sh.save()
                    return self.Response.ok(sh.search_count)
                else:
                    return self.Response.ok('max')
            else:
                SearchHistory.objects.create(search_dt=date.today(), search_count=1)
                return self.Response.ok('create')
        except Exception:
            return invalid('error: get SearchHistory')

    def post(self, request):
        data = json_loads(request.body)
        if not data:
            return invalid('not data')

        try:
            terms = data['terms']

            if not SearchHistory.objects.filter(search_dt=date.today()):
                SearchHistory.objects.create(search_dt=date.today(), search_count=1)

            sh = SearchHistory.objects.get(search_dt=date.today())

            if sh.search_count >= MAX_COUNT:
                return self.Response.ok(0, 1)

            result = getGoogleSearch(terms)

            sh.search_count += 1
            sh.save()
            return self.Response.ok(result)
        except Exception:
            return invalid('error: create product')

