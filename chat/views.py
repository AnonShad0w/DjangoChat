from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .models import Room

def index(request):
	room_list = Room.objects.order_by('title')
	return render(request, 'chat/index.html', {'room_list': room_list})

def room(request, room_name):
	return render(request, 'chat/room.html', {'room_name': room_name})
