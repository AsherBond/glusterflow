from django.http import HttpResponse

def index(request):
    return HttpResponse("Glusterflow UI index page")
