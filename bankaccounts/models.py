from django.db import models
import uuid
from django.contrib.auth.models import User
from shortuuid.django_fields import ShortUUIDField
from django.db.models.signals import post_save

ACCOUNT_STATUS = (
    ['in_active','IN_ACTIVE'],
    ['active','ACTIVE']
)

MARITAL_STATUS = (
    ['single','SINGLE'],
    ['married','MARRIED'],
    ['others','OTHERS']
)

GENDER =(
    ['male','MALE'],
    ['female','FEMALE'],
    ['others','OTHERS']
)

IDENTITY_TYPE = (
    ['driving_license','DRIVING_LICENSE'],
    ['aadhar_card','AADHAR_CARD'],
    ['pan_card','PAN_CARD'],
    ['voter-id','VOTER-ID'],
    ['others','OTHERS']
)


# Create your models here.
class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=12,decimal_places=2,default=0.00)
    account_number = ShortUUIDField(unique=True,length=12,max_length=25,prefix="217",alphabet="1234567890")
    account_id = ShortUUIDField(unique=True,length=10,max_length=25,prefix="DIGP",alphabet="1234567890")
    pin_number = ShortUUIDField(unique=True,length=4, max_length=7, alphabet="1234567890")
    account_status = models.CharField(max_length=100, choices=ACCOUNT_STATUS,default="in-active")
    date = models.DateTimeField(auto_now_add=True)
    kyc_submitted = models.BooleanField(default=False)
    kyc_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}'
    
class KYC(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account = models.OneToOneField(Account,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="kyc/")
    marital_status = models.CharField(max_length=200,choices = MARITAL_STATUS)
    gender = models.CharField(max_length=100,choices = GENDER)
    identity_type = models.CharField(max_length=100,choices = IDENTITY_TYPE)
    identity_image = models.ImageField(upload_to="kyc/")
    date_of_birth = models.DateTimeField(auto_now_add=False)
    signature = models.ImageField(upload_to="kyc/")
    
    #Address
    country = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    city = models.CharField(max_length=200)

    #Contact
    phone = models.CharField(max_length=100)
    email = models.EmailField(unique=True,blank=True)


def create_account(sender,instance,created,**kwargs):
    if created:
        Account.objects.create(user = instance)

def save_account(sender,instance,**kwargs):
    instance.account.save()

post_save.connect(create_account,sender=User)
post_save.connect(save_account,sender=User)


    