from django.http import HttpResponse

def home(request):
    return HttpResponse('<p>Home</p>')
