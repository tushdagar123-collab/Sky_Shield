from django.db import models
from django.conf import settings


class Incident(models.Model):
    CATEGORY_BIRD_STRIKE = 'bird_strike'
    CATEGORY_TECHNICAL_FAULT = 'technical_fault'
    CATEGORY_WEATHER = 'weather'
    CATEGORY_HUMAN_ERROR = 'human_error'
    CATEGORY_OTHER = 'other'

    CATEGORY_CHOICES = [
        (CATEGORY_BIRD_STRIKE, 'Bird Strike'),
        (CATEGORY_TECHNICAL_FAULT, 'Technical Fault'),
        (CATEGORY_WEATHER, 'Weather'),
        (CATEGORY_HUMAN_ERROR, 'Human Error'),
        (CATEGORY_OTHER, 'Other'),
    ]

    SEVERITY_LOW = 'low'
    SEVERITY_MEDIUM = 'medium'
    SEVERITY_HIGH = 'high'
    SEVERITY_CRITICAL = 'critical'

    SEVERITY_CHOICES = [
        (SEVERITY_LOW, 'Low'),
        (SEVERITY_MEDIUM, 'Medium'),
        (SEVERITY_HIGH, 'High'),
        (SEVERITY_CRITICAL, 'Critical'),
    ]

    STATUS_REPORTED = 'reported'
    STATUS_UNDER_REVIEW = 'under_review'
    STATUS_INVESTIGATING = 'investigating'
    STATUS_CLOSED = 'closed'

    STATUS_CHOICES = [
        (STATUS_REPORTED, 'Reported'),
        (STATUS_UNDER_REVIEW, 'Under Review'),
        (STATUS_INVESTIGATING, 'Investigating'),
        (STATUS_CLOSED, 'Closed'),
    ]

    title = models.CharField(max_length=200, help_text="Brief summary of the incident")
    description = models.TextField(help_text="Detailed narrative of what occurred")
    date_time = models.DateTimeField(verbose_name="Date & Time of Incident", help_text="When the incident occurred")
    location = models.CharField(max_length=200, help_text="Airport code, airspace waypoint, or geographic coordinates")
    aircraft_type = models.CharField(max_length=100, help_text="e.g., Boeing 737-800, Airbus A320, Cessna 172")
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default=CATEGORY_OTHER,
        help_text="Primary classification of the incident"
    )
    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default=SEVERITY_MEDIUM,
        help_text="Impact severity level"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_REPORTED,
        help_text="Current investigation status"
    )
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reported_incidents',
        help_text="User who logged this incident"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Reported At")

    class Meta:
        ordering = ['-date_time', '-created_at']
        verbose_name = 'Aviation Incident'
        verbose_name_plural = 'Aviation Incidents'

    def __str__(self):
        return f"[{self.get_severity_display()}] {self.title} ({self.aircraft_type})"
