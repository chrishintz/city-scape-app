from django.http import HttpResponse
from django.template import loader
from jinja2 import Environment, PackageLoader
from django.http import JsonResponse
from cityscape.yell import Yell
from cityscape.pets import Pets
from cityscape.influx import Influx
from cityscape.traffic import Traffic
from cityscape.mongo import Mongo
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
    # return HttpResponse(template.render())

def pet_score(request):
    return JsonResponse(Pets.recent_average(), safe=False)

def influx(request):
    return JsonResponse({"module": "Influx"})
    # put in mongodb object in jsonresponse
