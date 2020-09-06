from django.db import models

# Create your models here.

# storeクラス
class Store(models.Model):
  store_name = models.CharField(max_length=30, null=False, blank=False)
  store_email = models.EmailField(max_length=254, null=False, blank=False)
  store_password = models.CharField(max_length=30, null=False, blank=False)
  created_at = models.DateTimeField(auto_now_add=True, null=True)
  updated_at = models.DateTimeField(auto_now=True)
  deleted_at = models.DateTimeField(null=True, blank=True)

  def __str__(self):
    return self.store_name