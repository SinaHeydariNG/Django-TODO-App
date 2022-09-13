from django.urls import path , include
from . import views

app_name = 'api'

urlpatterns = [
    path('completed/' , views.CompletedList.as_view() , name='completed'),
    path('<int:pk>/completed/' , views.CompleteTodo.as_view() , name='completed'),
    path('current/' , views.CurrentListCreate.as_view() , name='current'),
    path('all/<int:pk>/' , views.CurrentListReriveUpdateDestroy.as_view() , name='all'),

    path('signup/' , views.signup , name='signup'),
    path('login/' , views.login , name='login')
]
 