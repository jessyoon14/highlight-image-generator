from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
# Create your views here.
import sys, os
print (sys.path)

sys.path.append(os.path.dirname('/Users/jessyoon/KAIST/1-intro-to-deep-learning/final-proj/highlight-generator/separator'))

from separator.constants import IMAGE_RES_DIR
from separator.run import run_end_to_end

import shutil


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


@api_view(['GET'])
def index(request):
    print('enter index')
    youtube_link = request.data['youtube_link']
    start_time = request.data['start_time']
    end_time = request.data['end_time']
    print(f'youtube_link is {youtube_link}')


    video_name = youtube_link[-5:]

    # call
    try:
        # run_end_to_end(youtube_link, start_time, end_time) # TODO: enable

        # create image zip file
        image_dir = f'{IMAGE_RES_DIR}/{video_name}'
        zip_file_path = f'{image_dir}.zip'
        make_archive(image_dir, zip_file_path)
        response = HttpResponse(open(zip_file_path, 'rb').read())
        response['Content-Type'] = 'application/zip'
        response['Content-Disposition'] = f'attachment; filename=highlight_images.zip'
        return response
    except Exception as e:
        print(e)
        return HttpResponse(f'Error while processing')

