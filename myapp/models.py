# myapp/models.py
from django.db import models
from simple_history.models import HistoricalRecords


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=250)
    image_url = models.URLField(blank=True, null=True)
    rsvp_link = models.URLField(
        blank=True,
        null=True,
        help_text="Link to sign-up form (e.g., Google Forms, Typeform)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Tracks every edit/delete operation in the database
    history = HistoricalRecords()

    def __str__(self):
        return self.title


class AboutPageContent(models.Model):
    title = models.CharField(max_length=200, default="ABOUT OUR SOCIETY")
    subtitle = models.CharField(
        max_length=200, default="// SYSTEM ORIGIN &amp; ARCHITECTURE")
    main_heading = models.CharField(
        max_length=300, default="PIONEERING IT, OPTICS &amp; MEDIA ENGINEERING")
    body_text = models.TextField(
        default="We are a collective of developers, engineers, and digital artists dedicated to pushing the boundaries of high-performance computing, optics, and broadcast technology.")
    mission_statement = models.TextField(
        default="To build robust systems, foster open technical education, and explore advanced media production techniques.")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "About Page Configuration"


# Add this model to your existing myapp/models.py
class TeamMember(models.Model):
    ROLE_CHOICES = [
        ('teacher', 'Teacher-in-Charge'),
        ('committee', 'Committee Member'),
        ('member', 'General Member'),
    ]

    name = models.CharField(max_length=200)
    role_category = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='member')
    position = models.CharField(max_length=150, blank=True, null=True,
                                help_text="e.g., President, Secretary, Lead Developer")
    image_url = models.URLField(
        blank=True, null=True, help_text="Profile picture URL")
    display_order = models.PositiveIntegerField(
        default=0, help_text="Order in which they appear (lower numbers first)")

    def __str__(self):
        return f"{self.name} ({self.get_role_category_display()})"


class HomePageContent(models.Model):
    hero_title = models.CharField(
        max_length=200, default="Welcome back to GCK Media Control Panel")
    hero_subtitle = models.CharField(
        max_length=300, default="Manage your systems, media, and events seamlessly.")
    welcome_banner_text = models.TextField(
        default="System operational and ready for deployment.")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Home Page Configuration"

    class Meta:
        verbose_name_plural = "Home Page Configuration"
