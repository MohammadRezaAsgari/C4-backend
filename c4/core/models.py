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
    profile = models.OneToOneField(Profile,on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    receipt_photo = models.ImageField(upload_to='uploads/receipt_photos/',null=True,blank=True)
    payment_valid = models.BooleanField(default=False)


class C4Group(models.Model):
    class C4GroupStatus(models.TextChoices):
        INPROGRESS = 'Inprogress'
        DONE = 'Done'

    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    creator = models.OneToOneField(Profile,on_delete=models.CASCADE)
    core1 = models.OneToOneField(Profile,on_delete=models.CASCADE,null=True,blank=True, related_name='core_one')
    core2 = models.OneToOneField(Profile,on_delete=models.CASCADE,null=True,blank=True, related_name='core_two')
    core3 = models.OneToOneField(Profile,on_delete=models.CASCADE,null=True,blank=True, related_name='core_three')
    status = models.CharField(max_length=20, choices=C4GroupStatus.choices, default=C4GroupStatus.INPROGRESS)
