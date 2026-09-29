from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q
from .models import Incident
from .forms import IncidentForm, UserRegisterForm


def home(request):
    """Homepage featuring 3D interactive flight tracking globe and dashboard flashcards."""
    total_count = Incident.objects.count()
    critical_count = Incident.objects.filter(severity='critical').count()
    active_count = Incident.objects.exclude(status='closed').count()
    superuser_incidents_count = Incident.objects.filter(
        Q(reported_by__is_staff=True) | Q(reported_by__is_superuser=True)
    ).count()

    context = {
        'total_count': total_count,
        'critical_count': critical_count,
        'active_count': active_count,
        'superuser_incidents_count': superuser_incidents_count,
    }
    return render(request, 'home.html', context)


def planes_placeholder(request):
    """Placeholder page for the aircraft fleet management module."""
    return render(request, 'incidents/planes.html')


def incident_list(request):
    """List page showing all incidents with optional search and filters."""
    incidents = Incident.objects.select_related('reported_by').all()

    # Search & filters
    search_query = request.GET.get('q', '').strip()
    category_filter = request.GET.get('category', '').strip()
    severity_filter = request.GET.get('severity', '').strip()
    status_filter = request.GET.get('status', '').strip()
    staff_only = request.GET.get('staff_only', '').strip()

    if search_query:
        incidents = incidents.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(aircraft_type__icontains=search_query)
        )

    if category_filter:
        incidents = incidents.filter(category=category_filter)

    if severity_filter:
        incidents = incidents.filter(severity=severity_filter)

    if status_filter:
        incidents = incidents.filter(status=status_filter)

    if staff_only in ('1', 'true', 'True'):
        incidents = incidents.filter(
            Q(reported_by__is_staff=True) | Q(reported_by__is_superuser=True)
        )

    # Metrics
    total_count = Incident.objects.count()
    critical_count = Incident.objects.filter(severity='critical').count()
    active_count = Incident.objects.exclude(status='closed').count()

    context = {
        'incidents': incidents,
        'search_query': search_query,
        'category_filter': category_filter,
        'severity_filter': severity_filter,
        'status_filter': status_filter,
        'staff_only': staff_only in ('1', 'true', 'True'),
        'categories': Incident.CATEGORY_CHOICES,
        'severities': Incident.SEVERITY_CHOICES,
        'statuses': Incident.STATUS_CHOICES,
        'total_count': total_count,
        'critical_count': critical_count,
        'active_count': active_count,
    }
    return render(request, 'incidents/incident_list.html', context)


def incident_detail(request, pk):
    """Detail page for a single incident."""
    incident = get_object_or_404(Incident.objects.select_related('reported_by'), pk=pk)
    return render(request, 'incidents/incident_detail.html', {'incident': incident})


@login_required
def incident_create(request):
    """Form page to report a new incident."""
    if request.method == 'POST':
        form = IncidentForm(request.POST)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.reported_by = request.user
            incident.save()
            messages.success(request, f'Incident "{incident.title}" was successfully reported!')
            return redirect('incident_detail', pk=incident.pk)
        else:
            messages.error(request, 'Please correct the errors below to submit the report.')
    else:
        form = IncidentForm()

    return render(request, 'incidents/incident_form.html', {'form': form})


def register(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('incident_list')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}! You are now logged in.')
            return redirect('incident_list')
        else:
            messages.error(request, 'Registration failed. Please check the details entered.')
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {'form': form})


def user_logout(request):
    """User logout view supporting both GET and POST."""
    logout(request)
    messages.info(request, 'You have been logged out safely.')
    return redirect('login')
