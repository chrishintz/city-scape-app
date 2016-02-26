from django.http import HttpResponse
from django.template import loader
from jinja2 import Environment, PackageLoader
from django.http import JsonResponse
from cityscape.happy import Happy
from cityscape.pets import Pets
from cityscape.influx import Influx
from cityscape.traffic import Traffic
from cityscape.mongo import Mongo
from cityscape.weather import Weather


def index(request):
    env = Environment(loader=PackageLoader('cityscape', 'templates'))
    template = env.get_template('jinja2/index.html')
    return HttpResponse(template.render(influx_calc = Influx.score_calc(),influx =Influx.score(), traffic = Traffic.comparison(), weather = ''.join((Weather.current_weather(), ".png")), image = Happy.chart()["image"]))

def traffic(request):
    env = Environment(loader=PackageLoader('cityscape', 'templates'))
    template = env.get_template('jinja2/traffic.html')
    # return HttpResponse(template.render())
    return HttpResponse(template.render(traffic = Traffic.comparison()))
    # return HttpResponse(Traffic.comparison())

def chart(request):
    return JsonResponse(Happy.chart(), safe=False)


def pet_score(request):
    return JsonResponse(Pets.average(), safe=False)

def influx(request):
    return JsonResponse({"module": "Influx"})
    # put in mongodb object in jsonresponse
