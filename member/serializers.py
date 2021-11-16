from rest_framework import serializers
from .models import Users

class UsersSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    ranking = serializers.FloatField(required=False)
    
    class Meta:
        model = Users
        #fields = ('name', 'username')
        fields = '__all__'
