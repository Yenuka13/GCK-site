# myapp/middleware.py
from django.shortcuts import render
from .models import SiteSettings


class MaintenanceModeMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        is_maintenance = False
        site_settings = None

        try:
            # Safely fetch or auto-create the singleton settings row
            site_settings = SiteSettings.load()
            if site_settings:
                is_maintenance = site_settings.is_maintenance_mode
        except Exception:
            is_maintenance = False

        if is_maintenance:
            # Allow access to Django Admin, media/static files
            if not request.path.startswith('/admin/') and not request.path.startswith('/static/'):
                # Bypass only if user is a superuser
                if not request.user.is_superuser:
                    message = site_settings.maintenance_message if site_settings else "System is currently undergoing scheduled maintenance."

                    # Convert target datetime to milliseconds timestamp for JavaScript
                    target_timestamp = 0
                    if site_settings and site_settings.countdown_target:
                        target_timestamp = int(
                            site_settings.countdown_target.timestamp() * 1000)

                    context = {
                        'maintenance_message': message,
                        'countdown_timestamp': target_timestamp
                    }
                    return render(request, 'maintenance.html', context, status=503)

        response = self.get_response(request)
        return response
