from django.http import HttpResponse
from django.template import loader
from jinja2 import Environment, PackageLoader
from django.http import JsonResponse
from cityscape.happy import Happy
from cityscape.weather import Weather

def index(request):
    env = Environment(loader=PackageLoader('cityscape', 'templates'))
    template = env.get_template('jinja2/index.html')
    return HttpResponse(template.render(weather = ''.join((Weather.current_weather(), ".png"))))

def chart(request):
    return JsonResponse(Happy.chart(), safe=False)




