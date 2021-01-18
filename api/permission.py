from rest_framework import permissions
from rest_framework import exceptions

# item権限機能
class CustomItemPermission(permissions.BasePermission):
  def has_permission(self, request, view):
    print('認証されました。')
    return super().has_permission(request, view)

  """
  オーナーのみ編集を可能にするカスタム権限
  """
  def has_object_permission(self, request, view, obj):
    # メソッドがGET, HEAD もしくは OPTIONSは常に許可
    if request.method in permissions.SAFE_METHODS:
      return True
    # 権限があるユーザーのみ編集可
    print('権限があるユーザーが編集しました。')
    return obj.store_owner == request.user

# store権限
class CustomStorePermission(permissions.BasePermission):
  def has_permission(self, request, view):
    print('ストアユーザー情報返却しました。')
    return super().has_permission(request, view)

# Payment権限
class PaymentPermission(permissions.BasePermission):
  def has_permission(self, request, view):
    print('認証されました。')
    return super().has_permission(request, view)

# User権限
class CustomUserPermission(permissions.BasePermission):
  def has_permission(self, request, view):
    print('ユーザー情報返却しました。')
    return super().has_permission(request, view)