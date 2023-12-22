from django.db import models
from myauth.models import Profile


class Project(models.Model):
    class ProjectStatus(models.TextChoices):
        REGISTERATION = 'Registeration'
        FUNDRAISING = 'Fundraising'
        CONSTRUCTION = 'Construction'
        END = 'End'


    title = models.CharField(max_length=50,unique=True)
    status = models.CharField(max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.REGISTERATION)
    units_number = models.PositiveIntegerField()
    project_area = models.PositiveIntegerField()
    completed_units_number = models.PositiveIntegerField()
    sold_units_number = models.PositiveIntegerField(default=0)
    applied_people_number = models.PositiveIntegerField(default=0)
    contractor_name = models.CharField(max_length=20)
    #
    #
    #
    #
    #

class Participation(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False)
    payment_accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ("profile", "project")

class C4Group(models.Model):
    class C4GroupStatus(models.TextChoices):
        INPROGRESS = 'Inprogress'
        DONE = 'Done'

    creator = models.ForeignKey(Profile,on_delete=models.CASCADE)
    core1 = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    core2 = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    core3 = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    status = models.CharField(max_length=20, choices=C4GroupStatus.choices, default=C4GroupStatus.INPROGRESS)

    class Meta:
        unique_together = ("creator", "core1","core2","core3")
