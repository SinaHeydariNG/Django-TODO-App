from rest_framework import serializers
from todo.models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        created = serializers.ReadOnlyField()
        datecompleted = serializers.ReadOnlyField()
        model = Todo
        fields = ['id','title' , 'memo' , 'created' , 'datecompleted' , 'important' ]
        
class TodoCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        created = serializers.ReadOnlyField()
        datecompleted = serializers.ReadOnlyField()
        model = Todo
        fields = ['id']
        read_only_fields = ['title' , 'memo' , 'created' , 'datecompleted' , 'important']
        