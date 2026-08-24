# myapp/admin.py
from .models import Event, AboutPageContent, TeamMember
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm
from simple_history.admin import SimpleHistoryAdmin

from .models import Event, AboutPageContent


# --- EVENT ADMIN ---
@admin.register(Event)
class EventAdmin(ModelAdmin, SimpleHistoryAdmin):
    list_display = ('title', 'date', 'location', 'rsvp_link', 'created_at')
    list_filter = ('date', 'location')
    search_fields = ('title', 'description')
    list_editable = ('location',)

    fieldsets = (
        ("General Information", {
            "fields": ("title", "description")
        }),
        ("Event Details & Links", {
            "fields": ("date", "location", "image_url", "rsvp_link")
        }),
    )


# --- ABOUT PAGE ADMIN ---
@admin.register(AboutPageContent)
class AboutPageAdmin(ModelAdmin):
    list_display = ('title', 'updated_at')


# --- CUSTOM USER ADMIN ---
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = BaseUserAdmin.list_display + ('quick_actions',)

    # 1. Hide superusers from non-superusers in list view
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_superuser=False)

    # 2. Block direct URL access to superuser profiles for non-superusers
    def has_change_permission(self, request, obj=None):
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    # 3. Block non-superusers from deleting superusers
    def has_delete_permission(self, request, obj=None):
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

    # 4. Generate quick delete button
    @admin.display(description="Actions")
    def quick_actions(self, obj):
        delete_url = reverse('admin:auth_user_delete', args=[obj.pk])
        return format_html(
            '<a class="bg-red-600 hover:bg-red-700 text-white text-xs font-semibold px-2.5 py-1 rounded transition-colors inline-block" href="{}">Delete</a>',
            delete_url
        )


# Add this registration to your existing myapp/admin.py


@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    list_display = ('name', 'role_category', 'position', 'display_order')
    list_filter = ('role_category',)
    search_fields = ('name', 'position')
    list_editable = ('display_order',)


# Re-register UserAdmin with custom configuration
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
