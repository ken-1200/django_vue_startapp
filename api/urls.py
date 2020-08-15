from rest_framework import routers
from django.urls import path
from django.conf.urls import include, re_path
from store.views import store
from api.views.stores import StoreViewSet
from api.views.items import ItemViewSet

# drf_yasg code starts here
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
  openapi.Info(
    title="Ecsite API",
    default_version='v1.0.0', # 必須APIドキュメントのバージョン情報
    description="Welcome to test Ecsite",# APIの詳細説明を記載
    terms_of_service="https://www.jaseci.org",# サービス利用規約
    contact=openapi.Contact(# 連絡先情報を定義
      email="jason@jaseci.org", 
      name="Customer Support"),
    license=openapi.License(name="Awesome IP"),# ライセンス名 urlも定義できる。イセンス名はSPDXを参考にするのがオススメ
  ),
  public=True,
  permission_classes=(permissions.AllowAny,),
)
# ends here

# ViewSet
router = routers.DefaultRouter()
router.register('stores', StoreViewSet)
router.register('items', ItemViewSet)


urlpatterns = [
  re_path('swagger(?P<format>\.json|\.yaml)$',
    schema_view.without_ui(cache_timeout=0), name='schema-json'),
  path('swagger/', 
    schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
  path('redoc/', 
    schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
  path('', include(router.urls))
]