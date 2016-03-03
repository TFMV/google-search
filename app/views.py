# coding=utf-8

from django.shortcuts import render_to_response
from django.contrib import auth
from django.http import HttpResponseRedirect#, HttpResponse, Http404, JsonResponse
from models import SearchHistory, Terms
from datetime import date

MAX_COUNT = 10

def home(request):
    if request.user.is_authenticated():
        terms = Terms.objects.order_by('term')
        count = SearchHistory.objects.get(search_dt=date.today()).search_count
        return render_to_response('index.html', {
            'terms': terms,
            'searchesToday': count,
            'remainingSearches': MAX_COUNT - count,
            })
    else:
        return HttpResponseRedirect('/signin/')

def signin(request):
    if request.method == 'GET':
        return render_to_response('signin.html', {'user': request.user})
    elif request.method == 'POST':
        if 'username' in request.POST and request.POST['username']:
            username = request.POST['username']
        else:
            return HttpResponseRedirect('/signin/')
        if 'password' in request.POST and request.POST['password']:
            password = request.POST['password']
        else:
            return HttpResponseRedirect('/signin/')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/signin/')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/signin/')
