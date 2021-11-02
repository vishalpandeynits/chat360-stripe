from datetime import time
from rest_framework import serializers
from .models import CardDetail
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username']
        # write_only_fields = ['id']

class CardDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:    
        model = CardDetail
        fields = ['id', 'user', 'card_number', 'expiry_date',]
        read_only_fields = ['id']


class CardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardDetail
        fields = ['user', 'card_number', 'expiry_date']