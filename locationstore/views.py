from django.shortcuts import render

def home(request):
    # The only view we use. Directly returns index.html.
    return render(request, 'index.html', {})
