from django.db import models
from django.contrib.auth.models import User
import uuid
import random
import string

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50,unique=True)


def generate_otp():
    rand = random.SystemRandom()
    digits = rand.choices(string.digits, k=4)
    return  ''.join(digits)

class OTPRequest(models.Model):
    request_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    receiver = models.CharField(max_length=50)
    password = models.CharField(max_length=4, default=generate_otp)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
