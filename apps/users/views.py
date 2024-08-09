import random

from rest_framework.exceptions import NotFound
from validate_email import validate_email
from django.core.mail import send_mail
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions, status
from .serializer import MainUserSerializer, MyTokenObtainPairSerializer, EmailConfirmSerializer, NewPasswordSerializer, \
    ForgotPasswordSetSerializer, ProfileSerializer, TemplateProfileSerializer
from .models import MainUser
from .permissions import AnnonPermission, IsOwnerOrReadOnly
from django.contrib.auth import login

from ..games.models import Room, RoomBase
from ..games.serializer import RoomBaseSerializer


def generate_code():
    random.seed
    return str(random.randint(10000, 999999))


class LoginView(TokenObtainPairView):
    permission_classes = (AnnonPermission,)
    serializer_class = MyTokenObtainPairSerializer


class UserRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = MainUserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            code = generate_code()
            is_valid = validate_email(email, verify=True)
            if is_valid:
                mainuser = MainUser(
                    email=email,
                    code=code
                )
                send_mail('Код подтверждения', code, "from@example.com", [email], fail_silently=False)
                mainuser.set_password(request.data['password'])
                mainuser.save()
                return Response({'message': 'Пользователь создан. Пожалуйста, проверьте свою почту для подтверждения.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Указанный вами email не существует'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request):
        code = request.data.get('code')
        email = request.data.get('email')

        try:
            user = MainUser.objects.get(email=email)
            if user and code == user.code:
                user.is_active = True
                user.code = 0
                user.save()
                return Response({'message': 'Email успешно подтвержден.'}, status=status.HTTP_200_OK)
            elif user.code == 0:
                return Response({'message': "Код недействителен"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Неверный код подтверждения.'}, status=status.HTTP_400_BAD_REQUEST)
        except MainUser.DoesNotExist:
            return Response({'error': 'Пользователь не найден.'}, status=status.HTTP_404_NOT_FOUND)


class NewPasswordSetView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, id):
        try:
            mainuser = MainUser.objects.get(id=id)
        except MainUser.DoesNotExist:
            raise NotFound("User not found")

        if mainuser != request.user:
            return Response({'error': 'You are not allowed to change the password of this user.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = NewPasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            mainuser.set_password(serializer.validated_data['password'])
            mainuser.save()
            return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        try:
            email = request.data.get('email')
            mainuser = MainUser.objects.get(email=email)
        except MainUser.DoesNotExist:
            raise NotFound("User not found")

        code = generate_code()
        send_mail('Код для восстановления пароля', code, "from@example.com", [email], fail_silently=False)
        mainuser.code = code
        mainuser.save()
        return Response({"message": "Вам успешно было отправлено сообщение с кодом проверьте пожалуйста почту"}, status=status.HTTP_200_OK)
        return Response({"message": "Что то пошло не так попробуйте позже"}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordSetView(APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request):
        email = request.data.get('email')
        code = request.data.get("code")

        try:
            mainuser = MainUser.objects.get(email=email)
        except MainUser.DoesNotExist:
            return Response({'error': 'Пользователь не найден.'}, status=status.HTTP_404_NOT_FOUND)

        if mainuser.code == 0:
            return Response({'message': "Код недействителен"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ForgotPasswordSetSerializer(data=request.data)
        if serializer.is_valid():
            if code == mainuser.code:
                mainuser.code = 0
                mainuser.set_password(serializer.validated_data['password'])
                mainuser.save()
                return Response({'message': 'Пароль успешно восстановлен.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Неверный код подтверждения.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        recently_games = RoomBase.objects.filter(room_players=user)
        games_data = RoomBaseSerializer(recently_games, many=True).data
        profile_data = TemplateProfileSerializer(user).data
        combinated_data = {
            'profile': profile_data,
            'room_base': games_data,
        }
        return Response(combinated_data, status=status.HTTP_200_OK)










