from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project,C4Group,Participation
#from .exceptions import *


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        # extra_kwargs = {'request_id': {'read_only': True},
        #                 'receiver': {'write_only': True},
        #                 }
        
