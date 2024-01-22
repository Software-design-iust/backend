from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class  User(AbstractUser):
    email = models.EmailField()
    is_recruiter = models.BooleanField(default=False)
    is_applicant = models.BooleanField(default=False)
    
    has_resume = models.BooleanField(default=False)
    has_company = models.BooleanField(default=False)