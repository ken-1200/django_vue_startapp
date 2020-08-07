from django.db import models


# Create your models here.

# 他のカラムを指定する方法
# from user.models.users import User と user_email = models.ForeignKey(User, db_column='user_email(自分のカラム)', to_field='user_email(リレーション先のカラム)', on_delete=models.PROTECT)

# paymentクラス
class Payment(models.Model):
  pay_totalprice = models.IntegerField(null=False, blank=False, default=0)
  user_email = models.EmailField(max_length=254, null=False, blank=False, unique=True)
  withdrawal_datetime = models.DateTimeField(auto_now_add=True, null=True)
  
  def __str__(self):
    return self.pay_totalprice