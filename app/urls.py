from django.contrib import admin
from django.urls import path
from django.conf.urls import include

# image
from django.conf.urls.static import static
from app.settings import base

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls'))
]

# url設定--url⇨root⇨image
urlpatterns += static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)