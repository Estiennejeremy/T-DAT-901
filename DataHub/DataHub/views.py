from django.http import HttpResponse, HttpResponseRedirect

def home(request):
    # if request.method == 'POST':
    print("gg fichier sauvegarder !!!!!!!!!!!!!!!!!!!!!!!!!")
    return HttpResponse("No access authorized !")
