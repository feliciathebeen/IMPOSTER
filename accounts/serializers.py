from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "nickname",
            "birth",
            "first_name",
            "last_name",
            "profile_image",
        )
    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            nickname=validated_data.get("nickname"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            birth=validated_data.get("birth"),
            profile_image=validated_data.get("profile_image"),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserSigninSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields = ["username", "password"]

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("아이디 또는 비밀번호가 잘못되었습니다.")
        
        data["user"] = user
        return data


class UserSignoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        self.token = data["refresh"]
        return data
        
    
    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except Exception as e:
            raise serializers.ValidationError("유효하지 않은 토큰입니다.")
        
class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields = (
            "username",
            "nickname",
        )