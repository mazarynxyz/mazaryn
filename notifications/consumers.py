import json
from django.core import serializers
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .serializers import NotificationSerializer
from .models import CustomNotification


class FriendRequestConsumer(AsyncJsonWebsocketConsumer):
    # notifications = CustomNotification.objects.select_related('actor').filter(recipient=user,type="friend")
    async def fetch_messages(self):
        user = self.scope['user']
        notifications = CustomNotification.objects.select_related(
            'actor').filter(recipient=user, type="friend")
        serializer = NotificationSerializer(notifications, many=True)
        content = {
            'command': 'notifications',
            'notifications': json.dumps(serializer.data)
        }

        await self.send_json(content)

        @staticmethod
        def notification_to_json(notification):
            return {
                'actor': serializers.serialize('json', [notification.actor]),
                'recipient': serializers.serialize('json', [notification.recipient]),
                'verb': notification.verb,
                'created_at': str(notification.timestamp)
            }

        def notifications_to_json(self, notifications):
            return [
                self.notification_to_json(notification)
                for notification in notifications
            ]  # serialize message

        async def connect(self):
            user = self.scope['user']
            grp = 'notifications_{}'.format(user.username)
            await self.accept()
            await self.channel_layer.group_add(grp, self.channel_name)

        async def disconnect(self, close_code):
            user = self.scope['user']
            grp = 'notifications_{}'.format(user.username)
            await self.channel_layer.group_discard(grp, self.channel_name)

        async def notify(self, event):
            await self.send_json(event)

        async def receive(self, text_data=None, bytes_data=None, **kwargs):
            data = json.loads(text_data)
            if data['command'] == 'fetch_friend_notifications':
                await self.fetch_messages()
