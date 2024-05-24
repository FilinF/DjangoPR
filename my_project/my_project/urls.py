from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from applications.views import upload_excel, display_excel, FileListView, delete_files_view,button_view

schema_view = get_schema_view(
    openapi.Info(
        title="My Project API",
        default_version='v1',
        description="API documentation for My Project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myproject.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload_excel/', upload_excel, name='upload_excel'),
    path('display_excel/<str:file_name>/', display_excel, name='display_excel'),
    path('api/list_files/', FileListView.as_view(), name='api_list_files'),
    path('delete-files/', delete_files_view, name='delete_files'),
    path('delete/', button_view, name='button'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]