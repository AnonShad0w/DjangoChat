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
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.join',
                'action': 'join',
                'username': username,
            }
        )
        
    async def disconnect(self, close_code):
        
        username = self.scope['user'].username
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.leave',
                'action': 'leave',
                'username': username,
            }
        )
                
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from WebSocket
    async def receive_json(self, content):
            
        username = self.scope["user"].username
        print("this is the content " + str(content))
        
        if content.get('type', None):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat.typing',
                    'action': content['type'],
                    'username': username,
                }
            )
        else:
            # Send message to room group (the event)
            message = content['message']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat.message',
                    'message': message,
                    'username': username,
                    'action': 'send'
                }
            )

# Handlers for messages sent over the channel layer

    # Receive message from room group
    async def chat_message(self, event):
        
        username = self.scope["user"].username
        message = event['message']
        username = event['username']
        print("message event " + str(event)) # prints in terminal for each open websocket
        
        # Send message to WebSocket seen in browswer console
        await self.send_json(
            {
                'message': message,
                'username': username,
                'client': self.scope['client'],
                'room': self.room_group_name,
                'action': 'keyboarding',
                'event': 'typing',
            },
        )
    
    async def chat_join(self, event):
        
        action = event['action']
        message = ' has joined the chat'
        username = event['username']
        print("join chat event " + str(event)) # prints in terminal for each open websocket
        
        # Send message to WebSocket seen in browswer console
        await self.send_json(
            {
                'message': message,
                'username': username,
                'client': self.scope['client'],
                'room': self.room_group_name,
                'action': 'join',
            },
        )

    async def chat_leave(self, event):
        
        action = event['action']
        message = ' has left the chat'
        username = event['username']
        print("left chat event " + str(event)) # prints in terminal for each open websocket
        
        # Send message to WebSocket seen in browswer console
        await self.send_json(
            {
                'message': message,
                'username': username,
                'client': self.scope['client'],
                'room': self.room_group_name,
                'action': 'leave',
            },
        )

    async def chat_typing(self, event):
        action = event['action']
        typing = event['type']
        username = event['username']
        print("typing chat event " + str(event)) # prints in terminal for each open websocket
        
        # Send message to WebSocket seen in browswer console
        await self.send_json(
            {
                'username': username,
                'client': self.scope['client'],
                'room': self.room_group_name,
                'action': action,
            },
        )
