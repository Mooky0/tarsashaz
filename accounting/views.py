import django.template.loader as loader
from django.http import HttpResponse


def index(request):
    template = loader.get_template('accounting/index.html')
    context = {}
    return HttpResponse(template.render(context, request))
    
def home(request):
    return HttpResponse('Home page')

def about(request):
    return HttpResponse('About page')

def contact(request):    
    return HttpResponse('Contact page')