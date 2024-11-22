from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, logout
from .serializers import UserSignupSerializer, UserSigninSerializer, UserSignoutSerializer, UserPasswordUpdateSerializer

# JWT 기반 회원가입 뷰
@api_view(["POST"]) # API 처리방식 
def signup_view(request):
    serializer = UserSignupSerializer(data=request.data) # UserSignupSerializer를 이용해서 데이터 검증 및 저장
    if serializer.is_valid(): # 요청한 데이터가 유효하면
        serializer.save()  # 회원가입 처리!
        return Response({"message": "회원가입 성공"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 잘못 된 요청시 오류 반환

# JWT 기반 로그인 뷰
@api_view(["POST"]) # API 처리방식 
def signin_view(request):
    serializer = UserSigninSerializer(data=request.data) # UserSigninSerializer를 이용해서 데이터 검증 및 인증
    if serializer.is_valid(): # 입력 된 데이터가 유효하면
        user = serializer.validated_data["user"]  # 인증된 사용자 객체 반환
        refresh = RefreshToken.for_user(user)  # 현재 유저의 JWT 토큰 생성
        return Response(
            {
                "refresh": str(refresh), # Refresh Token 
                "access": str(refresh.access_token), # Access Token
                "user_id": user.id, # 사용자 id
                "username": user.username, # 사용자 이름
            }, 
            status=status.HTTP_200_OK
        ) # 필요한 정보들 반환
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 로직상 알맞지 않으면 오류 반환

# JWT 기반 로그아웃 뷰
@api_view(["POST"]) # API 처리방식 
def signout_view(request):
    serializer = UserSignoutSerializer(data=request.data) # UserSignupSerializer를 사용해서 데이터 검증 후 로직 실행
    if serializer.is_valid(): # serializer로직이 유효한 경우
        serializer.save()  # Refresh Token 블랙리스트 처리
        return Response({"message": "로그아웃 성공"}, status=status.HTTP_205_RESET_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 로직상 알맞지 않으면 오류 반환

# 세션 기반 회원가입 뷰 (위 JWT 방식 회원가입 뷰랑 같이 사용해도 무관)
@api_view(["POST"]) # API 처리방식 
def session_signup_view(request):
    serializer = UserSignupSerializer(data=request.data) # UserSignupSerializer 사용해서 데이터 검증 및 저장
    if serializer.is_valid(): # 입력한 데이터가 유효하면 
        serializer.save() # 회원 정보를 저장
        return Response({"message": "회원가입했다 이 자식아"}, status=200)
    return Response(serializer.errors, status=400) # 로직상 알맞지 않으면 오류 반환

# 세션 기반 로그인 뷰
@api_view(["POST"]) # API 처리방식
def session_signin_view(request):
    serializer = UserSigninSerializer(data=request.data) # UserSigninSerializer를 사용하여 입력 데이터 검증
    if serializer.is_valid(): # 데이터 정보가 유효하면
        user = serializer.validated_data["user"]  # 인증된 사용자 객체 반환
        login(request, user)  # Django 세션에 사용자 정보 저장
        return Response({"message": "로그인 성공!", "username": user.username}, status=200)
    return Response(serializer.errors, status=400) # 검증 실패 시 오류 반환

# 세션 기반 로그아웃 뷰
@api_view(["POST"]) # API 처리방식
def session_signout_view(request): 
    logout(request) # Django 세션 삭제
    return Response({"message": "로그아웃 완료!"}, status=200)


@api_view(["POST"])  # 이 뷰는 POST 요청만 처리
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def update_password_view(request):
    """
    - 사용자 비밀번호 업데이트 뷰
    - POST 요청을 통해 기존 비밀번호와 새 비밀번호를 입력받고, 이를 검증 및 저장
    """
    serializer = UserPasswordUpdateSerializer(
        data=request.data,  # 요청 데이터를 시리얼라이저에 전달
        context={"request": request}  # 요청 객체를 context로 전달 (사용자 정보 사용)
    )
    if serializer.is_valid():  # 입력된 데이터가 유효하면
        serializer.save()  # 비밀번호 변경 로직 실행
        return Response({"message": "비밀번호 재설정 완(完)"}, status=200)  # 성공 메시지 반환
    return Response(serializer.errors, status=400)  # 유효하지 않은 경우 오류 반환