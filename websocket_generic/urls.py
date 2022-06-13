
from django.urls import path

from websocket_generic import views

urlpatterns = [
    path('vtoc/',views.msgfromoutside)
]