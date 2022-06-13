from django.contrib import admin

# Register your models here.
from websocket_generic.models import Chat, Group


@admin.register(Chat)
class ChatModelAdmin(admin.ModelAdmin):
    list_display=['id','content','time','group']
@admin.register(Group)
class GroupModelAdmin(admin.ModelAdmin):
    list_display=['id','name']