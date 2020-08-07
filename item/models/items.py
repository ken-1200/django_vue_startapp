from django.db import models
from store.models.stores import Store

# Create your models here.

# image保存方法
def load_path(instance, filename):
  return '/'.join(['image', str(instance.item_name) + str('.jpg')])

# itemクラス
class Item(models.Model):
  store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
  item_name = models.CharField(max_length=30, null=False, blank=False)
  item_img = models.ImageField(null=True, blank=True, upload_to=load_path)
  item_detail = models.TextField(null=True, blank=True)
  item_price = models.IntegerField(null=False, blank=False, default=0)
  item_total = models.IntegerField(null=False, blank=False, default=0)
  created_at = models.DateTimeField(auto_now_add=True, null=True)

  def __str__(self):
    return self.item_name