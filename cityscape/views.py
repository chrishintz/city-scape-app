from django.http import HttpResponse
from django.template import loader
from jinja2 import Environment, PackageLoader
from cityscape.yell import Yell
from cityscape.traffic import Traffic
from cityscape.weather import Weather


def index(request):
    env = Environment(loader=PackageLoader('cityscape', 'templates'))
    template = env.get_template('jinja2/index.html')
    return HttpResponse(template.render())


def traffic(request):
    return HttpResponse(Traffic.comparison())

def yell(request):
    return HttpResponse(Yell.recent_tweets().to_s())

    return HttpResponse(template.render(weather = ''.join((Weather.current_weather(), ".png"))))
