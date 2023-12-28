from django.db import models
from myauth.models import Profile
from django.dispatch import receiver
import os

class ProjectStatus(models.TextChoices):
    REGISTERATION = 'درحال ثبت نام'
    FUNDRAISING = 'جذب سرمایه'
    CONSTRUCTION = 'درحال ساخت'
    END = 'پایان کار'

class C4GroupStatus(models.TextChoices):
    INPROGRESS = 'درحال انجام'
    DONE = 'قطعی'

class Project(models.Model):
    title = models.CharField(max_length=100,unique=True)
    status = models.CharField(max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.REGISTERATION)
    units_number = models.PositiveIntegerField()
    project_area = models.PositiveIntegerField()
    completed_units_number = models.PositiveIntegerField()
    contractor_name = models.CharField(max_length=50)
    units_facilities = models.TextField()
    location_x = models.FloatField()
    location_y = models.FloatField()
    image_url = models.URLField()

    @property
    def applied_people_number(self):
        number = Participation.objects.filter(project=self.id).count()
        if number == self.units_number:
            self.status = ProjectStatus.FUNDRAISING
        return number
    
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
    
    def __str__(self) -> str:
        return self.title



class Participation(models.Model):
    profile = models.OneToOneField(Profile,on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    unit = models.PositiveIntegerField()
    receipt_photo = models.ImageField(upload_to='uploads/receipt_photos/')
    payment_valid = models.BooleanField(default=False)

    class Meta:
        unique_together = ['project','profile']

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




@receiver(models.signals.post_delete, sender=Participation)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.receipt_photo:
        if os.path.isfile(instance.receipt_photo.path):
            os.remove(instance.receipt_photo.path)

@receiver(models.signals.pre_save, sender=Participation)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Participation.objects.get(pk=instance.pk).receipt_photo
        new_file = instance.receipt_photo
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

    except:
        return False