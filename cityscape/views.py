from django.http import HttpResponse
from django.template import loader
from jinja2 import Environment, PackageLoader
from cityscape.yelling import Yelling
from cityscape.influx import Influx
from cityscape.mongo import Mongo
from django.http import JsonResponse

# from cityscape.weather import Weather

def index(request):
    env = Environment(loader=PackageLoader('cityscape', 'templates'))
    template = env.get_template('jinja2/index.html')
    return HttpResponse(template.render())


def influx(request):
    return JsonResponse({"made": "by"})
    # put in mongodb object in jsonresponse

    
