from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.
# custom user manager
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """create and save user with given email and password"""
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """ while creating user we are adding extra fields"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email, password, **extra_fields)


# my user model
class PortalUser(AbstractUser):
    USER_TYPES = (
        ('patient', 'patient'),
        ('doctor', 'doctor')
    )
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    username = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=20, null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey('self', on_delete=models.CASCADE, related_name='user_updated_by', null=True,
                                   blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True, upload_to='media/images/users/')
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        return self.email
