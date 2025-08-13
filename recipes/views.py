from django.http import HttpResponse


def index(request):
    return HttpResponse("Recipe Book is live!")
