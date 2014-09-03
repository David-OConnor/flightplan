from django.http import HttpResponse
from django.shortcuts import render

from diverts.forms import DivertForm

def index(request):
    if request.method == 'POST':
        form = DivertForm(request.POST)
        if not form.is_valid():
            return HttpResponse("<h2>Something went wrong - try again.</h2>")

        context_dict = {

        }
        return render('diverts/diverts_result.html', context_dict)

    else:
        form = DivertForm()
        context_dict = {}

        return render('diverts/index.html', {'form': form}, context_dict)