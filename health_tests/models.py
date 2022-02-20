from django.db import models
import uuid
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class UserMood(models.Model):
    """Class to track user mood swings"""

    uid = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=False, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    # Mood data
    mood_score = models.IntegerField(default=1, validators=[
        MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.uid}"
