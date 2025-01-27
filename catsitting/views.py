from django.http import HttpResponse

def welcome_view(request):
    return HttpResponse("<h1>Welcome at LuckyCat!</h1><p>The App is running succesfully</p>")
