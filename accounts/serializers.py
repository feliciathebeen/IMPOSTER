from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password

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

class UserPasswordUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    def validate(self, data):
        user = self.context["request"].user
        if not user.check_password(data["old_password"]):
            raise serializers.ValidationError({"old_password": "기존 비밀번호와 일치하지 않음"})
        if data["old_password"] == data["new_password"]:
            raise serializers.ValidationError({"new_password": "기존 비밀번호랑 다르게 해주셈"})
        return data
    
    def save(self, **kwangs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user