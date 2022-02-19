import email
from django.db import models
import uuid
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Profile(models.Model):
    """Model to Create and Store User Profile"""

    gender_choices = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Others"),
    )

    uid = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    # Profile data
    name = models.CharField(blank=False, default='User',
                            max_length=255, null=False)
    age = models.IntegerField(default=1, validators=[
                              MinValueValidator(1), MaxValueValidator(100)])
    gender = models.CharField(
        null=False, blank=False, default='M', choices=gender_choices, max_length=6)

    high_score = models.IntegerField(
        default=0, blank=False, null=False, validators=[MinValueValidator(0)])
    game_lives = models.IntegerField(
        default=0, blank=False, null=False, validators=[MinValueValidator(0)])
    last_score = models.IntegerField(
        default=0, blank=False, null=False, validators=[MinValueValidator(0)])

    # Location Data
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"User : {self.user.email}"
