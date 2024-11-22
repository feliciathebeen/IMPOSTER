from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])  # 비밀번호 검증 추가

    class Meta:
        model = User  # 커스텀 User 모델
        fields = (
            "username",
            "password",
            "nickname",
            "birth",
            "first_name",
            "last_name",
            "profile_image",
        )

    def validate(self, attrs):
        # 중복된 username 및 nickname 확인
        if User.objects.filter(username=attrs["username"]).exists():
            raise serializers.ValidationError({"username": "이미 존재하는 사용자 이름입니다."})
        if User.objects.filter(nickname=attrs["nickname"]).exists():
            raise serializers.ValidationError({"nickname": "이미 존재하는 닉네임입니다."})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")  # 비밀번호는 따로 처리
        user = super().create(validated_data)  # 나머지 필드는 기본 생성자로 처리
        user.set_password(password)  # 비밀번호 해싱
        user.save()  # 데이터베이스에 저장
        return user


class UserSigninSerializer(serializers.ModelSerializer):
    username = serializers.CharField() # 사용자 이름 필드
    password = serializers.CharField(write_only=True) # 비밀번호 쓰기 전용 필드

    class Meta:
        model=User # 커스텀 유저 모델
        fields = ["username", "password"] # 로그인에 필요한 필드만 포함

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password) # username과 password로 사용자 인증

        if user is None: 
            raise serializers.ValidationError("아이디 또는 비밀번호가 잘못되었습니다.") # 인증 실패시 에러 반환
        
        data["user"] = user # 인증된 사용자 객체 반환
        return data


class UserSignoutSerializer(serializers.Serializer):
    refresh = serializers.CharField() # Refresh Token 필드 생성

    def validate(self, data):
        self.token = data["refresh"] # Refresh Token 저장
        return data
        
    
    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)  # Refresh Token 객체 생성
            token.blacklist()  # 토큰을 블랙리스트에 추가
        except Exception as e:
            raise serializers.ValidationError("유효하지 않은 토큰입니다.")  # 토큰이 유효하지 않을 시 오류 반환
        
class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields = (
            "username",
            "nickname",
        )

class UserPasswordUpdateSerializer(serializers.Serializer):
    # 사용자가 입력한 기존 비밀번호
    old_password = serializers.CharField(write_only=True)  # 쓰기 전용 필드
    # 사용자가 입력한 새 비밀번호
    new_password = serializers.CharField(write_only=True, validators=[validate_password])  # Django의 비밀번호 검증 사용

    def validate(self, data):
        """
        - 기존 비밀번호 확인 및 새 비밀번호 검증
        - 요청한 사용자(`request.user`)가 입력한 기존 비밀번호가 올바른지 확인
        - 새 비밀번호가 기존 비밀번호와 다르게 설정되었는지 확인
        """
        user = self.context["request"].user  # 요청한 사용자 객체 가져오기

        # 기존 비밀번호 확인
        if not user.check_password(data["old_password"]):  # 비밀번호 검증 메서드
            raise serializers.ValidationError({"old_password": "기존 비밀번호와 일치하지 않음"})

        # 새 비밀번호가 기존 비밀번호와 동일한지 확인
        if data["old_password"] == data["new_password"]:
            raise serializers.ValidationError({"new_password": "기존 비밀번호랑 다르게 해주셈"})

        return data  # 유효성 검사를 통과한 데이터 반환
    
    def save(self, **kwangs):
        """
        - 새 비밀번호 저장
        - `user.set_password`를 사용하여 비밀번호를 해싱한 뒤 저장
        """
        user = self.context["request"].user  # 요청한 사용자 객체 가져오기
        user.set_password(self.validated_data["new_password"])  # 새 비밀번호 설정 (해싱 포함)
        user.save()  # 사용자 정보를 데이터베이스에 저장
        return user  # 변경된 사용자 객체 반환