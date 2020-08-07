from django.contrib import admin
from django.urls import path
from django.conf.urls import include

# image
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls'))
]

# url設定--url⇨root⇨image
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)