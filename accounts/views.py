from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, logout
from .serializers import UserSignupSerializer, UserSigninSerializer, UserSignoutSerializer

@api_view(["POST"])
def signup_view(request):
    serializer = UserSignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # 회원가입 처리
        return Response({"message": "회원가입 성공"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def signin_view(request):
    serializer = UserSigninSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data["user"]  # 인증된 사용자 객체
        refresh = RefreshToken.for_user(user)  # JWT 토큰 생성
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user_id": user.id,
                "username": user.username,
            },
            status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def signout_view(request):
    serializer = UserSignoutSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # Refresh Token 블랙리스트 처리
        return Response({"message": "로그아웃 성공"}, status=status.HTTP_205_RESET_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def session_signup_view(request):
    serializer = UserSignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "회원가입했다 이 자식아"}, status=200)
    return Response(serializer.errors, status=400)

@api_view(["POST"])
def session_signin_view(request):
    # UserSigninSerializer를 사용하여 입력 데이터 검증
    serializer = UserSigninSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data["user"]  # 인증된 사용자 객체
        login(request, user)  # Django 세션에 사용자 정보 저장
        return Response({"message": "로그인 성공!", "username": user.username}, status=200)
    
    # 검증 실패 시 오류 반환
    return Response(serializer.errors, status=400)

@api_view(["POST"])
def session_signout_view(request):
    logout(request)
    return Response({"message": "로그아웃 완료!"}, status=200)


