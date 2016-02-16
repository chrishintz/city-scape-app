from django.http import HttpResponse
from django.template import loader
from jinja2 import Environment, PackageLoader

def index(request):
    env = Environment(loader=PackageLoader('cityscape', 'templates'))
    template = env.get_template('jinja2/index.html')
    print template.render('jinja2/index.html')
    # HttpResponse("Hello, World")
