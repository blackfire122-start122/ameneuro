from django.shortcuts import render

def home(request):
	return render(request, "home/home.html")

def chats(request):
	return render(request, "chats/chats.html")