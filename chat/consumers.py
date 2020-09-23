import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class ChatConsumer(AsyncJsonWebsocketConsumer):
        
    # WebSocket event handlers    
    async def connect(self):
        
        # Is the client logged in?
        if self.scope['user'].is_anonymous:
            # Reject the connection
            await self.close()
        else:
            # Accept the connection
            await self.accept()
        
        # Store which rooms the user has joined on this connection
        self.rooms = set()
        
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        
        username = self.scope["user"].username
        
        # Join room goup
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from WebSocket
    async def receive_json(self, content):
            
        username = self.scope["user"].username
        message = content['message']
        print("this is the content " + str(content))
        
        # Send message to room group (the event)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message,
                'username': username,
            }
        )

# Handlers for messages sent over the channel layer

    # Receive message from room group
    async def chat_message(self, event):
        
        username = self.scope["user"].username
        message = event['message']
        username = event['username']
        print("this is the event " + str(event)) # prints in terminal for each open websocket
        
        # Send message to WebSocket seen in browswer console
        await self.send_json(
            {
                'message': message,
                'username': username,
                'client': self.scope['client'],
                'room': self.room_group_name,
            },
        )
