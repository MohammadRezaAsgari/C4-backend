from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .models import Project,C4Group,Participation
from myauth.models import Profile
from .exceptions import ParticipationDoesNotExistsException, ParticipationExistsException,ParticipationOwnerException, ParticipationPaymentException
from .serializers import ProjectListSerializer, ProjectRetrieveSerializer, ParticipateProjectSerializer, ParticipationPhotoSerializer,swagger_participation_create
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action

class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    permission_classes = [AllowAny,]

class ProjectRetrieveView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectRetrieveSerializer
    permission_classes = [AllowAny,]


class ParticipationCreateView(APIView):
    permission_classes = [IsAuthenticated,]

    @swagger_auto_schema(request_body=swagger_participation_create,responses={200: ParticipateProjectSerializer})
    def post(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        profile = Profile.objects.get(user=request.user.id)

        if Participation.objects.filter(profile=profile, project=project).exists():
            raise ParticipationExistsException
        
        participation_serializer = ParticipateProjectSerializer(data=request.data)
        if participation_serializer.is_valid():
            
            participation_serializer.save(profile=profile, project=project)
            return Response(participation_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(participation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParticipationListView(APIView):
    permission_classes = [IsAuthenticated,]

    @swagger_auto_schema(responses={200: ParticipateProjectSerializer})
    def get(self, request):
        profile = Profile.objects.get(user=request.user.id)
        
        try:
            participation = Participation.objects.get(profile=profile)
        except Participation.DoesNotExist:
            raise ParticipationDoesNotExistsException

        if not participation.payment_valid:
            raise ParticipationPaymentException

        participation_serializer = ParticipateProjectSerializer(participation)
        return Response(participation_serializer.data, status=status.HTTP_200_OK)

