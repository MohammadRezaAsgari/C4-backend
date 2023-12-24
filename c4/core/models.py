from django.db import models
from myauth.models import Profile

class ProjectStatus(models.TextChoices):
    REGISTERATION = 'Registeration'
    FUNDRAISING = 'Fundraising'
    CONSTRUCTION = 'Construction'
    END = 'End'

class C4GroupStatus(models.TextChoices):
    INPROGRESS = 'Inprogress'
    DONE = 'Done'

class Project(models.Model):
    title = models.CharField(max_length=100,unique=True)
    status = models.CharField(max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.REGISTERATION)
    units_number = models.PositiveIntegerField()
    project_area = models.PositiveIntegerField()
    completed_units_number = models.PositiveIntegerField()
    contractor_name = models.CharField(max_length=50)
    units_facilities = models.TextField()
    #map

    @property
    def applied_people_number(self):
        return Participation.objects.filter(project=self.id).count()
    
    @property
    def sold_units_number(self):
        return C4Group.objects.filter(project=self.id, status=C4GroupStatus.DONE).count()
    
    @property
    def total_invitations_sent(self):
        return C4Group.objects.filter(project=self.id).count()
    
    @property
    def seen_invitations_number(self): #what's this?
        return 
    
    @property
    def paid_invitations_number(self):
        return C4Group.objects.filter(project=self.id, status=C4GroupStatus.DONE).count()



class Participation(models.Model):
    profile = models.OneToOneField(Profile,on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    unit = models.PositiveIntegerField()
    receipt_photo = models.ImageField(upload_to='uploads/receipt_photos/',null=True,blank=True)
    payment_valid = models.BooleanField(default=False)

    class Meta:
        unique_together = ['project','unit']

class C4Group(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    creator = models.OneToOneField(Profile,on_delete=models.CASCADE)
    core1 = models.OneToOneField(Profile,on_delete=models.CASCADE,null=True,blank=True, related_name='core_one')
    core2 = models.OneToOneField(Profile,on_delete=models.CASCADE,null=True,blank=True, related_name='core_two')
    core3 = models.OneToOneField(Profile,on_delete=models.CASCADE,null=True,blank=True, related_name='core_three')
    status = models.CharField(max_length=20, choices=C4GroupStatus.choices, default=C4GroupStatus.INPROGRESS)
    unit = models.PositiveIntegerField()

    class Meta:
        unique_together = ['project','unit']