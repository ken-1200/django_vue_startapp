from django.db import models

# Create your models here.

# userクラス
class User(models.Model):
  user_email = models.EmailField(max_length=254, null=False, blank=False, unique=True)
  user_password = models.CharField(max_length=30, null=False, blank=False)
  withdrawal_datetime = models.DateTimeField('DeleteDate', blank=True, null=True, auto_now=True)

  def __str__(self):
    return self.user_email