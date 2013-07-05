#!/usr/bin/python
from django.template import Template, Context
from django.http import HttpResponse
import datetime


# This is a view function.
# A view is just a Python function that takes an HttpRequest as 
# its first parameter and returns an instance of HttpResponse.
def hello(request):
    return HttpResponse("Hello World")

def current_datetime(request):
    now = datetime.datetime.now()
    fp = open('../templatetest.html')
    t = Template(fp.read())
    fp.close()
    html = t.render(Context({'current_date': now}))
    return HttpResponse(html)
