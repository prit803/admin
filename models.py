from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone






from django.db import models
from django.core.exceptions import ValidationError
import re
from django.utils import timezone
from django.contrib.auth.hashers import make_password

class UserMaster(models.Model):
    UserId = models.BigAutoField(primary_key=True, null=False)
    email = models.EmailField(max_length=100, null=True , unique=True)
    password = models.CharField(max_length=25)
    firstname = models.CharField(max_length=50, null=True)
    lastname = models.CharField(max_length=50, null=True)
    mobileNumber = models.CharField(max_length=10, null=True)
    UserAddress = models.TextField(null=True)
    AdharNumber = models.CharField(max_length=20, null=True)
    PanNumber = models.CharField(max_length=10, null=True)
    isActive = models.BooleanField(default=True)
    isDelete = models.BooleanField(default=False)
    CreatedBy = models.CharField(max_length=50, null=True)
    CreatedDate = models.DateTimeField(default=timezone.now, null=True)
    ModifiedBy = models.CharField(max_length=100, null=True)
    ModifiedDate = models.DateTimeField(null=True)

    class Meta:
        db_table = "AdminUser"  # Specify the custom table name
    
    def __str__(self):
        if not self.firstname and not self.lastname:
            return "User information not available"  # Default message for null fields
        return f"{self.firstname or ''} {self.lastname or ''} ({self.email or ''})"

    

    # Password policy validation in the clean method
    def clean(self):


        if self.AdharNumber:
            if not re.match(r'^\d{4}-\d{4}-\d{4}-\d{4}$', self.AdharNumber):
                raise ValidationError("Aadhaar Number must be in the format '1234-1234-1234-1234'")
            

        if self.password:
            # Enforce minimum length
            if len(self.password) < 8:
                raise ValidationError("Password must be at least 8 characters long")
            
            # Enforce at least one uppercase letter
            if not any(char.isupper() for char in self.password):
                raise ValidationError("Password must contain at least one uppercase letter")
            
            # Enforce at least one lowercase letter
            if not any(char.islower() for char in self.password):
                raise ValidationError("Password must contain at least one lowercase letter")
            
            # Enforce at least one digit
            if not any(char.isdigit() for char in self.password):
                raise ValidationError("Password must contain at least one digit")
            
            # Enforce at least one special character
            if not re.search(r'[\W_]', self.password):  # Non-alphanumeric character
                raise ValidationError("Password must contain at least one special character")
        
        super(UserMaster, self).clean()  # Call the default clean method


   
    
    
    def save(self, *args, **kwargs):
        super(UserMaster, self).save(*args, **kwargs)

    def soft_delete(self):
        self.isdeleted = True
        self.save()



