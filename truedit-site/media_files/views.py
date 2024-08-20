from django.shortcuts import render
from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
from .models import Videos, Thumbnails
from .utils import format_count
from urllib.parse import urljoin
from django.urls import reverse

# Create your views here.

from .models import Thumbnails, Videos

def index(request):
    video_url = urljoin(settings.MEDIA_URL, 'media/videos/home_video.mp4')

    context = {
        'home_video': video_url,
    }

    return render(request, 'index.html', context)

def tos(request):
    return render(request, 'tos.html')

def pricing(request):
    """View function for pricing page of site."""

    # the videos
    videos = Videos.objects.all()

    # the thumbnails
    thumbnails = Thumbnails.objects.all()

    # Generate counts of the main objects
    num_thumbnails = Thumbnails.objects.all().count()
    num_videos = Videos.objects.all().count()

    # If Thumbnail does not have a client field, set num_thumbnail_clients to 0
    num_thumbnail_clients = 0

    # Check if the Thumbnail model has a client field
    try:
        if hasattr(Thumbnails, 'client'):
            num_thumbnail_clients = Thumbnails.objects.exclude(client__isnull=True).exclude(client__exact='').values('client').distinct().count()
    except FieldDoesNotExist:
        pass  # Field does not exist, num_thumbnail_clients remains 0

    # Count distinct non-null, non-blank clients in Video model
    num_video_clients = Videos.objects.exclude(client__isnull=True).exclude(client__exact='').values('client').distinct().count()

    # Add the client counts together
    num_clients = num_thumbnail_clients + num_video_clients

    # Format counts for display
    formatted_videos = [
        {
            'video': video.video,  # This assumes video.video contains the URL or embed code
            'likes': format_count(video.likes),
            'views': format_count(video.views),
        }
        for video in videos
    ]

    # Print paths to verify
    for thumbnail in thumbnails:
        print(thumbnail.image.url)  # Should print something like /media/thumbnails/example.jpg

    context = {
        'num_videos': num_videos,
        'num_thumbnails': num_thumbnails,
        'num_clients': num_clients,
        'videos': formatted_videos,
        'thumbnails': thumbnails,
    }

    return render(request, 'pricing.html', context=context)