import random
from django.db import models
from myauth.models import Profile
from django.dispatch import receiver
from django.db.models.signals import post_save
import os
from django.db.models import Q

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
    unit = models.PositiveIntegerField(null=True, blank=True)
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
    unit = models.PositiveIntegerField(null=True,blank=True)

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
    
@receiver(post_save, sender=Participation)
def handle_payment_valid_change(sender, instance, **kwargs):
    """
    A function to be called when the payment_valid field of a Participation instance changes.
    """
    if kwargs.get('update_fields') is None or 'payment_valid' in kwargs['update_fields']:
        # The payment_valid field has been changed
        if instance.payment_valid:
            update_c4group(instance)

def update_c4group(participation_instance):
    profile = Profile.objects.get(id=participation_instance.profile_id)
    filter = Q(creator = profile) | Q(core1 = profile) | Q(core2 = profile) | Q(core3 = profile)
    try:
        c4_groups = C4Group.objects.filter(filter,status=C4GroupStatus.INPROGRESS)

        for c4_group in c4_groups:
            creator_participation = Participation.objects.get(profile=c4_group.creator)
            c1_participation = Participation.objects.get(profile=c4_group.core1)
            c2_participation = Participation.objects.get(profile=c4_group.core2)
            c3_participation = Participation.objects.get(profile=c4_group.core3)

            if creator_participation.payment_valid and c1_participation.payment_valid and c2_participation.payment_valid and c3_participation.payment_valid:
                c4_group.status = C4GroupStatus.DONE
                unit_number = calculate_unit_number(c4_group.project_id)
                c4_group.unit = unit_number
                c4_group.save()

                creator_participation.unit = unit_number
                creator_participation.save()
    except :
        return
    
def calculate_unit_number(project_id):
    project = Project.objects.get(id=project_id)
    existing_unit_numbers = C4Group.objects.filter(project=project).values_list('unit', flat=True)

    # Generate a list of available unit numbers
    available_unit_numbers = [unit for unit in range(1, project.units_number + 1) if unit not in existing_unit_numbers]

    if not available_unit_numbers:
        raise ValueError("No available unit numbers for the project")

    # Choose a random available unit number
    chosen_unit_number = random.choice(available_unit_numbers)
    return chosen_unit_number
