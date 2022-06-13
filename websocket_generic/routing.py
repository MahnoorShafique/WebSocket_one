from django.urls import path
from . import consumers


ws_patterns=[
    path('ws/wsc/<str:GroupName>/',consumers.MyWebSocketConsumer.as_asgi()),
    path('ws/awsc/<str:GroupName>/',consumers.MyAsyncWebSocketConsumer.as_asgi()),
    # path('ws/ac/<str:groupName>/',consumers.MyAsyncConsumer.as_asgi())
]