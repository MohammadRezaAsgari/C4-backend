from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project,C4Group,Participation
#from .exceptions import *

class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['title','units_number','project_area','completed_units_number','applied_people_number','sold_units_number',]

class ProjectRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
