from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project,C4Group,Participation
#from .exceptions import *
from myauth.serializers import ProfileSerializer

class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title','units_number','project_area','completed_units_number','sold_units_number','location_x','location_y']

class ProjectRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'status', 'units_number', 'project_area', 
                  'completed_units_number', 'contractor_name', 'units_facilities', 
                  'applied_people_number','sold_units_number', 'total_invitations_sent', 
                  'seen_invitations_number', 'paid_invitations_number','image_url','location_x','location_y']


class ParticipateProjectSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    project = ProjectRetrieveSerializer(read_only=True)
    class Meta:
        model = Participation
        fields = '__all__'
        extra_kwargs = {
                        'payment_valid': {'read_only': True},
                        }
    
class ParticipationPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participation
        fields = ['receipt_photo']

    
class swagger_participation_create(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = ['unit']
