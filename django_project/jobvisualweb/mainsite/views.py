from django.shortcuts import render
from .service import *

# Create your views here.
def table(request):
    return render(request, 'table.html', {'JobLists':getJobLists()})

def wordcloud(request):
    return render(request, 'wordcloud.html')

def word_cloud(request):
    data = getRequireMajors()
    return JsonResponse(json.dumps(data), safe=False)

def piechart(request):
    return render(request, 'piechart.html')

def pie_chart(request):
    data = get_piechart_data()
    return JsonResponse(json.dumps(data), safe=False)

def lollipopchart(request):
    return render(request, 'lollipopchart.html')

def lollipop_chart(request):
    data = get_lollipop_data()
    return JsonResponse(json.dumps(data), safe=False)