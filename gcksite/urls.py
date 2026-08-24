# gcksite/urls.py
from django.contrib import admin
from django.urls import include, path

# Admin Branding Customizations
admin.site.site_header = "GCK Media Control Panel"
admin.site.site_title = "GCK Admin Portal"
admin.site.index_title = "Welcome to GCK Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),  # Includes app routes
]
