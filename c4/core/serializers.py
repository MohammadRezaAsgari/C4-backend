from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project,C4Group,Participation
from myauth.models import Profile
from .exceptions import *
from rest_framework.response import Response
from django.db.models import Q
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
                  'applied_people_number','sold_units_number','location_x','location_y']


class ParticipateProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participation
        fields = ['id', 'receipt_photo','unit', 'payment_valid', 'total_invitations_sent', 'seen_invitations_number', 'paid_invitations_number']
        extra_kwargs = {'unit': {'read_only': True},
                        'payment_valid': {'read_only': True},
                        'total_invitations_sent': {'read_only': True},
                        'seen_invitations_number': {'read_only': True},
                        'paid_invitations_number': {'read_only': True},
                        }
    
class swagger_participation_create(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = ['receipt_photo']

class C4GroupSerializer(serializers.ModelSerializer):
    project = ProjectRetrieveSerializer(read_only=True)
    creator = ProfileSerializer(read_only=True)
    core1 = ProfileSerializer(read_only=True)
    core2 = ProfileSerializer(read_only=True)
    core3 = ProfileSerializer(read_only=True)
    class Meta:
        model = C4Group
        fields = '__all__'

class C4GroupCreateSerializer(serializers.Serializer):
    core1 = serializers.CharField()
    core2 = serializers.CharField()
    core3 = serializers.CharField()

    def validate(self, attrs):
        try:
            core1 = Profile.objects.get(phone_number=attrs["core1"])
        except Profile.DoesNotExist:
            raise Core1NotExistsException
        
        try:
            core2 = Profile.objects.get(phone_number=attrs["core2"])
        except Profile.DoesNotExist:
            raise Core2NotExistsException
        
        try:
            core3 = Profile.objects.get(phone_number=attrs["core3"])
        except Profile.DoesNotExist:
            raise Core3NotExistsException
        
        core1_filter = Q(creator = core1) | Q(core1 = core1) | Q(core2 = core1) | Q(core3 = core1)
        core2_filter = Q(creator = core2) | Q(core1 = core2) | Q(core2 = core2) | Q(core3 = core2)
        core3_filter = Q(creator = core3) | Q(core1 = core3) | Q(core2 = core3) | Q(core3 = core3)

        if C4Group.objects.filter(core1_filter).exists():
            raise Core1ExistsException
        if C4Group.objects.filter(core2_filter).exists():
            raise Core2ExistsException
        if C4Group.objects.filter(core3_filter).exists():
            raise Core3ExistsException
        return attrs
    
    def save(self, project, profile, **kwargs):
        data = self.validated_data
        core1 = Profile.objects.get(phone_number=data["core1"])
        core2 = Profile.objects.get(phone_number=data["core2"])
        core3 = Profile.objects.get(phone_number=data["core3"])
        return C4Group.objects.create(creator=profile, project=project, core1=core1, core2=core2, core3=core3)
