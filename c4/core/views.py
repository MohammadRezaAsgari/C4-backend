from django.shortcuts import render
from rest_framework import generics
from .models import Project,C4Group,Participation
from .serializers import ProjectListSerializer
from rest_framework.permissions import AllowAny


class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    permission_classes = [AllowAny,]