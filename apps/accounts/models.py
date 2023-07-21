from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, BaseUserManager, UserManager
from django.utils import timezone
from utils import FileUpload

class CostomUserManeger(BaseUserManager):
    def create_user(self,mobile_number, email='', name='', family='', active_code=None, gender=None, password=None):
        if not mobile_number:
            raise ValueError("It's not phone number")
        user = self.model(
            mobile_number=mobile_number,
            email=self.normalize_email(email),
            name=name,
            family=family,
            active_code=active_code,
            gender=gender
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,mobile_number, email, name, family, active_code=None, gender=None, password=None):
        user=self.create_user(
            mobile_number=mobile_number, 
            email=email,
            name=name,
            family=family,
            active_code=active_code,
            gender=gender,
            password=password,
        )
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
        

class CustomUser(AbstractBaseUser,PermissionsMixin):
    mobile_number = models.CharField(max_length=11, unique=True, verbose_name='Molbile Number')
    email = models.EmailField(max_length=254, blank=True)
    name = models.CharField(max_length=50, blank=True)
    family = models.CharField(max_length=50, blank=True)
    GENDER_CHOISES = (('True','Male'),('False','Female'))
    gender = models.CharField(max_length=50, choices=GENDER_CHOISES, default='True', null=True, blank=True)
    register_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    active_code = models.CharField(max_length=100, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['name','family','email']
    
    objects = CostomUserManeger()
    
    def __str__(self) -> str:
        return f"{self.name} {self.family}"
    
    @property
    def is_staff(self):
        return self.is_admin
    
    
class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    file_upload = FileUpload('images', 'customer')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name='Profile image', null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.user}"