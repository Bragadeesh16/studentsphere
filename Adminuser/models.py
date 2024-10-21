from django.db import models

# Create your models here.
from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.db.models.signals import post_save
from django.dispatch import receiver





class folders(models.Model):
    name = models.CharField(max_length=50)
    folder_from = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.name


class file_uplode(models.Model):
    notes = models.FileField(upload_to="image/")
    file_from = models.ForeignKey(folders, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        file_name = self.notes.name.split("/")[-1]
        return file_name