from django.http import HttpResponse
from django.template import loader
from jinja2 import Environment, PackageLoader
from cityscape.yelling import Yelling
from cityscape.traffic import Traffic

def index(request):
    env = Environment(loader=PackageLoader('cityscape', 'templates'))
    template = env.get_template('jinja2/index.html')
    return HttpResponse(template.render())
    # HttpResponse("Hello, World")

def traffic(request):
    return HttpResponse(Traffic.recent_tweets().to_s())

def yelling(request):
    return HttpResponse(Yelling.recent_tweets().to_s())
