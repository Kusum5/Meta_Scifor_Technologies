from django.shortcuts import render
from yt_dlp import YoutubeDL
# Create your views here.
#defining function
def youtube(request):
    #checking whether request is post or not
    if request.method == 'POST':
        #getting link for form url
        url = request.POST['link']
        ydl_opts = {
            'format':'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        #returning HTML page
        return render(request,'templates/downloader/home.html')
    return render(request,'templates/downloader/home.html')

