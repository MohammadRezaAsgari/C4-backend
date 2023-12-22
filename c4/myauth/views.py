from rest_framework.permissions import AllowAny
from rest_framework import generics
from .models import Profile,OTPRequest
from .serializers import RegisterSerializer, RequestOtpSerializer, VerifyOtpRequestSerializer, ObtainTokenSerializer
from rest_framework import status
from rest_framework.response import Response
from datetime import timedelta
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from .sender import send_otp
from .exceptions import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action

class ProfileRegisterView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny, ]

class OtpCreateView(generics.CreateAPIView):
    queryset = OTPRequest.objects.all()
    serializer_class = RequestOtpSerializer

    def perform_create(self, serializer):
        serializer.save()
        send_otp(serializer.instance)
        return


def handle_login(data):
    try:
        profile = Profile.objects.get(phone_number=data['receiver'])
        refresh = RefreshToken.for_user(profile.user)

        return ObtainTokenSerializer({
            'refresh': str(refresh),
            'token': str(refresh.access_token)
        }).data
    
    except:
        raise UserNotExistsException
    

class OtpCheckView(generics.CreateAPIView):
    @action(detail=True, methods=['POST'])
    @swagger_auto_schema(request_body=VerifyOtpRequestSerializer,responses={200: ObtainTokenSerializer})
    def post(self, request):
        serializer = VerifyOtpRequestSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            current_time = timezone.now()
            if OTPRequest.objects.filter(
                    receiver = data['receiver'],
                    request_id = data['request_id'],
                    password = data['password'],
                    created_at__lt = current_time,
                    created_at__gt = current_time-timedelta(seconds=120),
                    ).exists():
                return Response(handle_login(data))
            else:
                raise PassIncorrectException

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)
