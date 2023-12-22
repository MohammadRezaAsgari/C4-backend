from django.shortcuts import render
from rest_framework import generics
from .models import Project,C4Group,Participation
from .serializers import ProjectSerializer
from rest_framework.permissions import AllowAny


class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny,]