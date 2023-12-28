from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .models import Project,C4Group,Participation,ProjectStatus
from myauth.models import Profile
from .exceptions import *
from .serializers import *
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q

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
        
        if project.status != ProjectStatus.REGISTERATION:
            raise ProjectIsNotRegisteringException

        profile = Profile.objects.get(user=request.user.id)

        if Participation.objects.filter(profile=profile, project=project).exists():
            raise ParticipationExistsException
        
        participation_serializer = ParticipateProjectSerializer(data=request.data)
        if participation_serializer.is_valid():
            
            participation_serializer.save(profile=profile, project=project)
            project.applied_people_number
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


class C4GroupListCreateView(APIView):
    permission_classes = [IsAuthenticated,]

    @swagger_auto_schema(request_body=C4GroupCreateSerializer,responses={200: C4GroupSerializer})
    def post(self, request):
        profile = Profile.objects.get(user=request.user)

        try:
            participation = Participation.objects.get(profile=profile)
        except Participation.DoesNotExist:
            raise ParticipationDoesNotExistsException
        
        project = Project.objects.get(id=participation.project_id)
        
        if C4Group.objects.filter(creator=profile).exists():
            raise C4GroupExistsException
        
        c4_group_serializer = C4GroupCreateSerializer(data=request.data)
        if c4_group_serializer.is_valid():
            
            instance = c4_group_serializer.save(profile=profile, project=project)
            return Response(C4GroupSerializer(instance).data, status=status.HTTP_201_CREATED)
        else:
            return Response(c4_group_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @swagger_auto_schema(responses={200: C4GroupSerializer})
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        filter = Q(creator = profile) | Q(core1 = profile) | Q(core2 = profile) | Q(core3 = profile)
        try:
            c4_group = C4Group.objects.filter(filter)
        except C4Group.DoesNotExist:
            raise C4GroupDoesNotExistsException
        
        return Response(C4GroupSerializer(c4_group,many=True).data, status=status.HTTP_200_OK)



