from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(blank=True, null=True, max_length=10)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def save(self,*args,**kwargs):
        self.email = self.email.lower()
        return super().save(*args,**kwargs)
    
    def get_profile(self):
        return profiles.objects.get_or_create(user=self)[0]
    
@receiver(post_save,sender = CustomUser)
def save_username_when_user_is_created(sender,instance,created,*args,**kwargs):
    if created:
        email = instance.email
        sliced_email = email.split('@')[0]
        instance.username = sliced_email
        instance.save()

class profiles(models.Model):
    GENDER = {"male": "male", "female": "female"}
    Name = models.CharField(max_length=30, null=True, blank=True)
    Phone_Number = models.IntegerField(null=True, blank=True)
    Gender = models.CharField(max_length=30, null=True, blank=True, choices=GENDER)
    Address = models.CharField(max_length=100, null=True, blank=True)
    Aadhar_Number = models.IntegerField(null=True, blank=True)
    Father_Name = models.CharField(max_length=30, null=True, blank=True)
    Mother_Name = models.CharField(max_length=30, null=True, blank=True)
    Father_Occupation = models.CharField(max_length=50, null=True, blank=True)
    Mother_Occupation = models.CharField(max_length=30, null=True, blank=True)
    Father_Phone_Number = models.IntegerField(null=True, blank=True)
    mother_Phone_Number = models.IntegerField(null=True, blank=True)
    Annual_Income = models.IntegerField(null=True, blank=True)
    Religion = models.CharField(max_length=50, null=True, blank=True)
    Caste = models.CharField(max_length=50, null=True, blank=True)
    Community = models.CharField(max_length=50, null=True, blank=True)
    Mother_Language = models.CharField(max_length=50, null=True, blank=True)
    # date_of_birth = models.DateField(blank = True,null =True)
    profile_user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )   