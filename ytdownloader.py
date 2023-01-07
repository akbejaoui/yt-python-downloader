import sys
import os

from pytube import YouTube
from pick import pick
from pathlib import Path


def onProgress(stream, chunk, bytes_remaining):
    size = stream.filesize
    current = ((size - bytes_remaining)/size)

    percent = ('{0:.1f}').format(current*100)
    
    progress = int(50*current)
    status = '█' * progress + '-' * (50 - progress)

    sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent))
    sys.stdout.flush()
                
def fetchAllResolutions(yt):
    resolutionList = []
    for stream in yt.streams.filter(progressive=True).order_by('resolution'):
        if (stream.resolution not in resolutionList):
            resolutionList.append(stream.resolution)
    
    return resolutionList

def printVideoData(yt):
    print ("availble:", yt.check_availability())
    #Title of video
    print("Title: ",yt.title)
    #Number of views of video
    print("Number of views: ",yt.views)
    #Length of the video
    print("Length of video: ",yt.length,"seconds")
    #Rating
    print("Ratings: ",yt.rating)


def downloadVideo(resolution, yt):
    print("Selected resolution:", resolution)
    video = yt.streams.get_by_resolution(resolution)
    path_to_download_folder = str(os.path.join(Path.home(), "Downloads"))

    if video:
        video.download(path_to_download_folder)

print ('Enter youtube video link: ')
link = input()
yt = YouTube(link, on_progress_callback=onProgress)
printVideoData(yt)
title = 'Please select a resolution to download: '
options = fetchAllResolutions(yt)
option, index = pick(options, title, indicator='=>', default_index=2)
downloadVideo(option, yt)
