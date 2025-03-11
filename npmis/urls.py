from django.conf.urls.static import static
from django.shortcuts import redirect
from django.contrib import admin

from django.urls import path, include, reverse_lazy
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from npmis.settings.base import DEBUG
from npmis.settings.base import STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path('', lambda request: redirect(reverse_lazy('swagger-ui'), permanent=False)),
    path('npmis/', include([
        path('admin/', admin.site.urls),
        path('api-auth/', include(('rest_framework.urls', 'rest_framework'), namespace='api-auth')),
        path('schema/', include([
            path('', SpectacularAPIView.as_view(), name='schema'),
            path('swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
            path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
        ])),
        path('api/v1/', include([
            path('auth/', include(('npmis.apps.authentication.urls', 'npmis.apps.authentication'), namespace="authentication")),
            path('settings/', include(('npmis.apps.settings.urls', 'npmis.apps.settings'), namespace="settings")),
            path('accounts/', include(('npmis.apps.user_management.urls', 'npmis.apps.user_management'), namespace="accounts")),
            path('projects/', include(('npmis.apps.projects.urls', 'npmis.apps.projects'), namespace="projects")),
        ])),
    ])),
]

# Serve media and static files in DEBUG mode
if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
    urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
