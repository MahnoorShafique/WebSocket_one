from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def msgfromoutside(request):
    channel_layer=get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'pak',
        {
            'type':'chat.message',
            'message':'Message From outside consumer'
        }
    )
    return HttpResponse("message sent from view to consumer")
