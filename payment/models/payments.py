from django.db import models

# Create your models here.

# paymentクラス
class Payment(models.Model):
  pay_totalprice = models.IntegerField(null=False, blank=False, default=0)
  user_email = models.EmailField(max_length=254, null=False, blank=False)
  bought_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.pay_totalprice