from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile,Role

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password')
        extra_kwargs = {'password': {'write_only':True} }
    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            password = validated_data['password'],
        )
        role , _ =  Role.objects.get_or_create(role_name = 'student')
        Profile.objects.get_or_create(user=user, defaults={'role': role})
        return user
    