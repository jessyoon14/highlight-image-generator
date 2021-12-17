from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view

# Create your views here.
import sys, os
base_dir = os.getcwd()
sys.path.append(os.path.dirname(f'{base_dir}/separator'))

# sys.path.append(os.path.dirname('/home/yominx/ws/highlight-image-generator/separator'))

from separator.constants import IMAGE_RES_DIR
from separator.run import run_end_to_end

import os, shutil
def make_archive(source, destination):
        base = os.path.basename(destination)
        name = base.split('.')[0]
        format = base.split('.')[1]
        archive_from = os.path.dirname(source)
        archive_to = os.path.basename(source.strip(os.sep))
        print(source, destination, archive_from, archive_to)
        shutil.make_archive(name, format, archive_from, archive_to)
        shutil.move('%s.%s'%(name,format), destination)


@api_view(['POST'])
def index(request):
    print('enter index')
    youtube_link = request.data['youtube_link']
    start_time_str = request.data['start_time'].split(':')
    end_time_str = request.data['end_time'].split(':')

    start_time = int(start_time_str[0]) * 60 + int(start_time_str[1])
    end_time   = int(end_time_str[0]) * 60 + int(end_time_str[1])
    print(f'youtube_link is {youtube_link}')


    video_name = youtube_link[-5:]

    # call
    try:
        run_end_to_end(youtube_link, start_time, end_time)
        print('finish run_end_to_end')
        # create image zip file
        print('start zip')
        image_dir = f'{IMAGE_RES_DIR}/{video_name}_final'
        zip_file_path = f'{image_dir}.zip'
        make_archive(image_dir, zip_file_path)
        print('finish zip')
        return HttpResponse('Received link and finished processing')
    except Exception as e:
        print(e)
        return HttpResponse(f'Error while processing')


@api_view(['GET'])
def download(request):
    print('enter index')

    video_name = request.GET.get('youtube_name', '')[:-1]
    if video_name == '':
        return HttpResponse(f'Bad file name (should be last 5 letters of youtube link)')

    # call
    try:
        # create image zip file
        image_dir = f'{IMAGE_RES_DIR}/{video_name}'
        zip_file_path = f'{image_dir}_final.zip'
        response = HttpResponse(open(zip_file_path, 'rb').read())
        response['Content-Type'] = 'application/zip'
        response['Content-Disposition'] = f'attachment; filename=highlight_images.zip'
        return response
    except Exception as e:
        print(e)
        return HttpResponse(f'Error while processing')
