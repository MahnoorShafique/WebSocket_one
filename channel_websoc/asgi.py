import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from websocket_generic import routing
import websocket_generic

application=ProtocolTypeRouter({
    'http':get_asgi_application(),

     'websocket':URLRouter(websocket_generic.routing.ws_patterns)
})