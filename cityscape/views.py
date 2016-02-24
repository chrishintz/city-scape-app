from django.http import HttpResponse
from django.template import loader
from jinja2 import Environment, PackageLoader
from django.http import JsonResponse
from cityscape.happy import Happy

# from cityscape.weather import Weather


def index(request):
    env = Environment(loader=PackageLoader('cityscape', 'templates'))
    template = env.get_template('jinja2/index.html')
    return HttpResponse(template.render())

def chart(request):
    # return JsonResponse({"score": 2, "me": 3})
    return JsonResponse(Happy.average(), safe=False)

# def weather(request):
#     return HttpResponse(Weather.recent_tweets().to_s())  ##doesn't work, needs to be a string
