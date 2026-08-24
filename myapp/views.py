from django.shortcuts import render
from django.utils import timezone
from .models import Event, AboutPageContent, TeamMember  # Removed TeamModel


def home(request):
    """Renders the main landing homepage."""
    return render(request, 'myapp/index.html')


def events_list(request):
    """Fetches all events, showing upcoming ones first."""
    # Fetch all events so past events aren't completely hidden
    all_events = Event.objects.all().order_by('-date')

    # Optional: Filter specifically for upcoming events
    upcoming_events = Event.objects.filter(
        date__gte=timezone.now()
    ).order_by('date')

    # Pass all_events if you want to troubleshoot missing entries
    return render(request, 'myapp/events.html', {'events': all_events})


def about_view(request):
    # Gets the dynamic content, or falls back to a default if none is created yet
    about_content = AboutPageContent.objects.first()

    # Fetch team members sorted by display order
    teachers = TeamMember.objects.filter(
        role_category='teacher').order_by('display_order')
    committee = TeamMember.objects.filter(
        role_category='committee').order_by('display_order')
    members = TeamMember.objects.filter(
        role_category='member').order_by('display_order')

    context = {
        'about': about_content,
        'teachers': teachers,
        'committee': committee,
        'members': members,
    }

    # Renders template from the myapp subfolder
    return render(request, 'myapp/about.html', context)
