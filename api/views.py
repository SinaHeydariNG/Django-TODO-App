from django.utils import timezone
from rest_framework import generics , permissions
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from . import serializer
from todo.models import Todo
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(username=data['username'], password=data['password'])
            user.save()
            token = Token.objects.create(user = user)
            return JsonResponse({'token' : str(token)} , status = 201)
        except IntegrityError:
            return JsonResponse({'error' : 'This username has already taken please chose another one'} , status = 400)
@csrf_exempt
def login(request):
    if request.method == 'POST':
            data = JSONParser().parse(request)
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is None:
                return JsonResponse({'error' : 'could not match any result from db consider changing eather username or password'} , status = 400)
            else:  
                token = Token.objects.get(user=user)          
                return JsonResponse({'token' : str(token)} , status = 200)



class CompletedList(generics.ListAPIView):
    serializer_class = serializer.TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user = user , datecompleted__isnull = False).order_by('-datecompleted')

class CurrentListCreate(generics.ListCreateAPIView):
    serializer_class = serializer.TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        print(user)
        return Todo.objects.filter(user = user , datecompleted__isnull = True).order_by('-created')    

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)       

class CurrentListReriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializer.TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user = user).order_by('-created')    

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  

class CompleteTodo(generics.UpdateAPIView):
    serializer_class = serializer.TodoCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user = user)  

    def perform_update(self, serializer):
        serializer.instance.datecompleted = timezone.now()   
        serializer.save()     