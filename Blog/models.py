from django.db import models

# Create your models here.
class user_model(models.Model):
    user_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=50) 
    lname = models.CharField(max_length=50)
    profile_image = models.ImageField(upload_to='profile/',default='') 
    email = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=12)
    password = models.CharField(max_length=30)
    
    def __str__(self):
        return self.fname

class blog_model(models.Model):
    blog_id = models.AutoField(primary_key=True)
    user_email = models.CharField( max_length=50)
    title = models.CharField( max_length=80)
    brief = models.CharField(max_length=100)
    discription = models.TextField()
    blogImage =models.ImageField(upload_to='blogImage/',default='') 
    visibility = models.BooleanField(default=False)
    pub_Date = models.DateField()
    def __str__(self):
        return self.title

class message(models.Model):
    message_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=50) 
    lname = models.CharField(max_length=50)
    email_address = models.CharField(max_length=50)
    message = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.email_address

