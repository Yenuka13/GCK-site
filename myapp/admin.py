from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm
from simple_history.admin import SimpleHistoryAdmin

from .models import Event, AboutPageContent, TeamMember, HomePageContent, SiteSettings


# --- REUSABLE DELETE ACTION MIXIN ---
class DeleteActionMixin:
    """Adds a custom styled Delete action button to list displays."""

    def get_list_display(self, request):
        list_display = list(super().get_list_display(request))
        if 'quick_actions' not in list_display:
            list_display.append('quick_actions')
        return list_display

    @admin.display(description="Actions")
    def quick_actions(self, obj):
        opts = self.model._meta
        delete_url = reverse(
            f'admin:{opts.app_label}_{opts.model_name}_delete', args=[obj.pk])
        return format_html(
            '<a class="bg-red-600 hover:bg-red-700 text-white text-xs font-semibold px-2.5 py-1 rounded transition-colors inline-block" href="{}">Delete</a>',
            delete_url
        )


# --- EVENT ADMIN ---
@admin.register(Event)
class EventAdmin(DeleteActionMixin, ModelAdmin, SimpleHistoryAdmin):
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
class AboutPageAdmin(DeleteActionMixin, ModelAdmin):
    list_display = ('title', 'updated_at')


# --- HOME PAGE ADMIN ---
@admin.register(HomePageContent)
class HomePageAdmin(DeleteActionMixin, ModelAdmin):
    list_display = ('hero_title', 'updated_at')


# --- TEAM MEMBER ADMIN ---
@admin.register(TeamMember)
class TeamMemberAdmin(DeleteActionMixin, ModelAdmin):
    list_display = ('name', 'role_category', 'position', 'display_order')
    list_filter = ('role_category',)
    search_fields = ('name', 'position')
    list_editable = ('display_order',)


# --- SITE SETTINGS & MAINTENANCE CONTROL ADMIN ---
@admin.register(SiteSettings)
class SiteSettingsAdmin(DeleteActionMixin, ModelAdmin):
    list_display = ('is_maintenance_mode', 'maintenance_message')

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


# --- AUTH GROUP ADMIN (For Managing User Groups) ---
admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(DeleteActionMixin, ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# --- CUSTOM USER ADMIN ---
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = BaseUserAdmin.list_display + ('quick_actions',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_superuser=False)

    def has_change_permission(self, request, obj=None):
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

    @admin.display(description="Actions")
    def quick_actions(self, obj):
        delete_url = reverse('admin:auth_user_delete', args=[obj.pk])
        return format_html(
            '<a class="bg-red-600 hover:bg-red-700 text-white text-xs font-semibold px-2.5 py-1 rounded transition-colors inline-block" href="{}">Delete</a>',
            delete_url
        )


# Re-register UserAdmin with custom configuration
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
