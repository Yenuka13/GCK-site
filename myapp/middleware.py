# myapp/middleware.py
from django.shortcuts import render
from .models import SiteSettings


class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        settings = SiteSettings.load()

        if settings.is_maintenance_mode:
            # Allow staff members and admin dashboard access
            if not request.user.is_staff and not request.path.startswith('/admin'):
                # Public routes to block
                public_paths = ['/', '/about/', '/events/']

                if request.path in public_paths or any(request.path.startswith(p) and p != '/' for p in public_paths):
                    return render(request, 'maintenance.html', {
                        'maintenance_message': settings.maintenance_message
                    }, status=503)

        response = self.get_response(request)
        return response
