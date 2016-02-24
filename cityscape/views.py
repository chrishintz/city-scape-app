from django.http import HttpResponse
from django.template import loader
from jinja2 import Environment, PackageLoader
from django.http import JsonResponse
from cityscape.pets import Pets
from cityscape.weather import Weather


def index(request):
    env = Environment(loader=PackageLoader('cityscape', 'templates'))
    template = env.get_template('jinja2/index.html')
    return HttpResponse(template.render(weather = ''.join((Weather.current_weather(), ".png"))))

    # return HttpResponse(template.render())

def pet_score(request):
    return JsonResponse(Pets.recent_average(), safe=False)

# def weather(request):
#     return HttpResponse(Weather.recent_tweets().to_s())  ##doesn't work, needs to be a string
