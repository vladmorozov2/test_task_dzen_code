import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer
from .serializers import CommentSerializer

class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("comments", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("comments", self.channel_name)

    async def receive(self, text_data):
      
        pass


    async def new_comment(self, event):
        print("New comment received:", event)
        print("Comment:", event["comment"])
        comment = event["comment"]
        await self.send(
            text_data=json.dumps({"type": "new_comment", "comment": comment})
        )
    
def notify_new_comment(comment_instance):
    print("notify_new_comment called with:", comment_instance)
    channel_layer = get_channel_layer()
    serializer = CommentSerializer(comment_instance)
    async_to_sync(channel_layer.group_send)(
        "comments",
        {
            "type": "new_comment",
            "comment": serializer.data,
        }
    )