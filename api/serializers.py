from django.contrib.auth import authenticate, login, logout
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError
from .models import Article
from django.contrib.auth.models import User


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs["email"]).exists()
        if email_exists:
            raise ValidationError("Email has already been used")

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user



