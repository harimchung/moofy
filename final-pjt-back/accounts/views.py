# Create your views here.
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.hashers import check_password
#from django.views import View
#from django.http import JsonResponse

from .serializers import UserSerializer

def validate_username(username): ## 아이디 검증 메소드
    validate_condition = [
        lambda s: all(x.islower() or x.isdigit() or '_' for x in s), ## 영문자 대소문자, 숫자, 언더바(_)만 허용
        lambda s: any(x.islower() for x in s), ## 영어 소문자 필수
        lambda s: len(s) == len(s.replace(" ","")), ##중간 공백을 허용하지 않아?
        lambda s: len(s) >= 4, ## 글자수 제한
        #lambda s: len(s) <= 20, ## 글자수 제한
    ]

    for validator in validate_condition:
        if not validator(username):
            return True

# def validate_password(self, password): ## 비밀번호 검증 메소드
#     validate_condition = [
#         lambda s: all(x.islower() or x.isupper() or x.isdigit() or (x in ['!', '@', '#', '$', '%', '^', '&', '*', '_']) for x in s), ## 영문자 대소문자, 숫자, 특수문자(리스트)만 허용
#         lambda s: any(x.islower() or x.isupper() for x in s), ## 영어 대소문자 필수
#         lambda s: len(s) == len(s.replace(" ","")),
#         lambda s: len(s) >= 8, ## 글자수 제한
#         lambda s: len(s) <= 20, ## 글자수 제한
#     ]

#     for validator in validate_condition:
#         if not validator(password):
#             return True


# 회원가입 요청
@api_view(["POST"])
def signup(request):

    ##아이디 검증

    username = request.data.get("username")

    # 비밀번호, 비밀번호 확인
    password = request.data.get("password")
    password_confirm = request.data.get("passwordConfirm")
    
    ## 입력/검증 통과 여부 확인

    if not username: ## 아이디를 입력 안 했다면

        return Response({"error" : [0,"아이디를 입력하세요"]}, status = status.HTTP_400_BAD_REQUEST)

    if validate_username(username): #올바른 아이디를 입력하지 않았다면...

        return Response({"error" : [2,"올바른 아이디를 입력해주세요. (영어 소문자(필수), 숫자, 언더바(_), 4자 이상)"]}, status = status.HTTP_400_BAD_REQUEST)
    
    if not password: # 비밀번호를 입력 안했다면..

        return Response({"error" : [1,"비밀번호를 입력하세요"]}, status = status.HTTP_400_BAD_REQUEST)
    
    if password != password_confirm: #비밀번호가 일치하지 않는다면..

        return Response({"error" : [3,"비밀번호가 일치하지 않습니다!"]}, status = status.HTTP_400_BAD_REQUEST)
    
    # if validate_password(password): ## 비밀번호가 검증을 통과하지 못했다면
    #   return Response({"error : 올바른 비밀번호를 입력해주세요. (영문(대소문자)(필수), 숫자, 특수문자(!, @, #, $, %, ^, &, *, _))"}, status = status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(data=request.data)

    # 데이터가 유효한지 검증
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        # 사용자의 암호를 해쉬함수를 통해 바꿔줌(암호화)
        user.set_password(request.data.get("password"))
        # 바꾼 비밀번호로 다시 저장
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


#회원정보 수정 & 삭제
@api_view(['POST','DELETE', 'PUT'])
def user_update_delete(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    
    #회원정보 삭제
    if request.method=="DELETE":
        serializer = UserSerializer(user)
        # 확인하려는 비밀번호
        password = request.data.get("password")

        if check_password(password,user.password):
            user.delete()
            data = {
                "delete" : f'{user_pk}번째 회원님이 탈퇴하셨습니다.'
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        else:

            data = {
                "error" : '비밀번호가 일치하지 않습니다.',
            }
            return Response(data, status = status.HTTP_400_BAD_REQUEST)
    
    #회원정보 수정전 비밀번호 인증단계
    elif request.method == 'POST':
        password = request.data.get("password")
    
        if check_password(password,user.password):
            data = {
                "Authenticated" : "인증 완료" 
            }
            return Response(data,status=status.HTTP_200_OK)
        else:
            data = {
                "error" : "비밀번호가 일치하지 않습니다."
            }
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
    
    #인증에 성공하고, 수정하는 단계
    elif request.method=="PUT":
        password = request.data.get("password")
        password_confirm = request.data.get("passwordConfirm")
        if password != password_confirm:
            data = {"error_type": 3, "error" : "비밀번호가 일치하지 않습니다!"}
            return Response(data, status = status.HTTP_400_BAD_REQUEST) #400을 쓰지 않으면 에러로 반환하지 않음
        elif len(request.data.get("nickname")) < 2:
            data = {"error_type": 7, "error" : "최소 2자 이상의 닉네임을 입력하세요."}
            return Response(data,status = status.HTTP_400_BAD_REQUEST)
        
        else:
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):

                user = serializer.save()
                
                #사용자의 암호를 해쉬함수로 바꿔주는 함수
                user.set_password(request.data.get("password"))
                user.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
    

# 프로파일 업데이트 요청
@api_view(["GET"])
def profile(request):
    user = get_object_or_404(get_user_model(), pk=request.user.pk)
    # User 조회해서 반환하기
    if request.method == 'GET':
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    


@api_view(["PUT"])
def profileupdate(request, user_pk):
        # User 정보 업데이트
    user = get_object_or_404(get_user_model(), pk=user_pk)
    if request.method == "PUT":
        profile = request.data.get('profile')

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

