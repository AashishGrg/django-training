from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


# Create your models here.
class Hospital(models.Model):
    name = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=50)
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True, upload_to='media/images/hospitals/%Y-%m-%d')
    created_by = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='hospital_created_by')
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name
