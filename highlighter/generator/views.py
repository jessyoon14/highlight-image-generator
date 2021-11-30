from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
# Create your views here.
@api_view(['GET'])
def index(request):
    print('enter index')
    youtube_link = request.data['youtube_link']
    start_time = request.data['start_time']
    end_time = request.data['end_time']
    print(f'youtube_link is {youtube_link}')



    return HttpResponse(f"Hello, world, link is {youtube_link}")