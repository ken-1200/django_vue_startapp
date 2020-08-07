from django.db import models
from payment.models.payments import Payment
from item.models.items import Item

# Create your models here.

# roleクラス
class Role(models.Model):
  pay_id = models.ForeignKey(Payment, on_delete=models.PROTECT)
  item_id = models.ForeignKey(Item, on_delete=models.PROTECT)
  item_quantity = models.IntegerField(null=False, blank=False, default=0)

  def __str__(self):
    return self.pay_id