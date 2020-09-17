from django.db import models

# Create your models here.

# userクラス
class User(models.Model):
  user_email = models.EmailField(max_length=254, null=False, blank=False)
  user_password = models.CharField(max_length=30, null=False, blank=False)
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  updated_at = models.DateTimeField(auto_now=True)
  withdrawal_at = models.DateTimeField(null=True, blank=True)

  def __str__(self):
    return self.user_email