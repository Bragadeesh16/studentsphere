from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from .validators import validate_phone_number


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(
        blank=True,
        null=True,
        max_length=10,
        unique=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        return super().save(*args, **kwargs)

    def get_profile(self):
        return UserProfile.objects.get_or_create(user=self)[0]


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
    ]

    DEPARTEMENT = [
        ("Computer science", "Computer science"),
        ("Civil", "Civil"),
        ("Mechanical", "Mechanical"),
        ("ECE", "ECE"),
        ("EEE", "EEE"),
        ("IT", "IT"),
        ("Cyber security", "Cyber security"),
        ("AIDS", "AIDS"),
    ]

    YEAR = [
        ("First year", "First year"),
        ("Second year", "Second year"),
        ("Third year", "Third year"),
        ("Final year", "Final year"),
    ]

    PASSEDOUT_YEAR = [
        ("2025", "2025"),
        ("2026", "2026"),
        ("2027", "2027"),
        ("2028", "2028"),
        ("2029", "2029"),
        ("2030", "2030"),
        ("2031", "2031"),
        ("2032", "2032"),
        ("2033", "2033"),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True, blank=True)
    phone_number = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        validators=[validate_phone_number],
    )
    gender = models.CharField(
        max_length=6,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
    )
    department = models.CharField(
        max_length=17,
        choices=DEPARTEMENT,
        null=True,
        blank=True,
    )
    year = models.CharField(
        max_length=17,
        choices=YEAR,
        null=True,
        blank=True,
    )
    passedout_year = models.CharField(
        max_length=4,
        choices=PASSEDOUT_YEAR,
        null=True,
        blank=True,
    )
    address = models.CharField(max_length=100, null=True, blank=True)
    aadhar_number = models.CharField(max_length=12, null=True, blank=True)
    father_name = models.CharField(max_length=30, null=True, blank=True)
    mother_name = models.CharField(max_length=30, null=True, blank=True)
    father_occupation = models.CharField(max_length=50, null=True, blank=True)
    mother_occupation = models.CharField(max_length=30, null=True, blank=True)
    father_phone_number = models.CharField(max_length=15, null=True, blank=True)
    mother_phone_number = models.CharField(max_length=15, null=True, blank=True)
    annual_income = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    religion = models.CharField(max_length=50, null=True, blank=True)
    caste = models.CharField(max_length=50, null=True, blank=True)
    community = models.CharField(max_length=50, null=True, blank=True)
    mother_language = models.CharField(max_length=50, null=True, blank=True)


    def __str__(self):
        return self.user.email
    
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.user.username
        super(UserProfile, self).save(*args, **kwargs)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


@receiver(post_save, sender=CustomUser)
def save_username_when_user_is_created(sender, instance, created, **kwargs):
    if created:
        email = instance.email
        sliced_email = email.split("@")[0]
        instance.username = sliced_email
        instance.save()
