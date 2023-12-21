from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile,OTPRequest
from .exceptions import *


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True, max_length=50)
    last_name = serializers.CharField(required=True, max_length=50)

    phone_number = serializers.CharField(required=True, max_length=50)
    national_code = serializers.CharField(required=True, max_length=50)

    def validate(self, attrs):
        if User.objects.filter(username=attrs["national_code"]).exists():
            raise UserExistsException
        if Profile.objects.filter(phone_number=attrs["phone_number"]).exists():
            raise PhoneIsUsedException
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            username=validated_data["national_code"]
        )
        Profile.objects.create(
            user=user,
            phone_number=validated_data["phone_number"],
        )
        return validated_data


class RequestOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPRequest
        fields = ['receiver','request_id']
        extra_kwargs = {'request_id': {'read_only': True},
                        'receiver': {'write_only': True},
                        }
        
class VerifyOtpRequestSerializer(serializers.Serializer):
    request_id = serializers.UUIDField(required=True)
    password = serializers.CharField(max_length=4, required=True)
    receiver = serializers.CharField(max_length=50, required=True)

class ObtainTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=128, allow_null=False)
    refresh = serializers.CharField(max_length=128, allow_null=False)