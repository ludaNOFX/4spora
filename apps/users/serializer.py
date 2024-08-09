from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import MainUser

from apps.games.serializer import RoomBaseSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['email'] = user.email
        token['is_Seller'] = user.is_Seller
        return token


class MainUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=MainUser.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = MainUser
        fields = [
            'id',
            'email',
            'password',
            'password2',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Password fields didnt match!'}
            )
        return attrs


class EmailConfirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = ['email', 'code']


class NewPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = MainUser
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class ForgotPasswordSetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = MainUser
        fields = ('code', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs


class TemplateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = ['email', 'balance', 'deposits', 'winrate', 'loserate', 'tokenswin', 'tokenslose']


class ProfileSerializer(serializers.Serializer):
    profile = TemplateProfileSerializer()
    room_base = RoomBaseSerializer(many=True)

    class Meta:
        fields = ['profile', 'room_base']


class MainUserSerializerData(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = "__all__"

        extra_kwargs ={
            'email': {'required': 'False'},
            'password': {'required': 'False'},
            'code': {'required': 'False'},
            'balance': {'required': 'False'},
            'winrate': {'required': 'False'},
            'loserate': {'required': 'False'},
            'tokenswin': {'required': 'False'},
            'tokenslose': {'required': 'False'},
            'deposits': {'required': 'False'},
            'is_active': {'required': 'False'},
        }



