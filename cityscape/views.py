from django.http import HttpResponse
from django.template import loader
from jinja2 import Environment, PackageLoader
from cityscape.influx import Influx
from cityscape.mongo import Mongo
from django.http import JsonResponse

# from cityscape.weather import Weather
from cityscape.weather import Weather


def index(request):
    env = Environment(loader=PackageLoader('cityscape', 'templates'))
    template = env.get_template('jinja2/index.html')
    return HttpResponse(template.render(weather = ''.join((Weather.current_weather(), ".png"))))
    
def influx(request):
    return JsonResponse({"module": "Influx"})
    # put in mongodb object in jsonresponse
