from typing import Iterable
from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(blank=True, null=True, max_length=10)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    # def save(self,*args,**kwargs):
    #     self.email = self.email.lower()
    #     return super().save(*args,**kwargs)


class folders(models.Model):
    name = models.CharField(max_length=50)
    folder_name = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.name


class file_uplode(models.Model):
    notes = models.FileField(upload_to="image/")
    file_from = models.ForeignKey(folders, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        file_name = self.notes.name.split("/")[-1]
        return file_name


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

    # def __str__(self) -> str:
    #     return self.name


class messages(models.Model):
    message = models.TextField(null=True, blank=True)
