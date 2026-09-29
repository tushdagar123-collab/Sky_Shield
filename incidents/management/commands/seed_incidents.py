from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from incidents.models import Incident


class Command(BaseCommand):
    help = 'Seeds database with realistic demo aviation incident records'

    def handle(self, *args, **options):
        # Create or fetch demo user
        user, created = User.objects.get_or_create(
            username='demo_pilot',
            defaults={
                'email': 'pilot@skyshield.aero',
                'first_name': 'Aero',
                'last_name': 'Captain'
            }
        )
        if created:
            user.set_password('Pilot1234!')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created demo user: "demo_pilot" (password: Pilot1234!)'))
        else:
            self.stdout.write('Using existing user "demo_pilot"')

        now = timezone.now()

        sample_incidents = [
            {
                'title': 'Dual Engine Ingestion During Takeoff Roll',
                'description': 'Aircraft encountered a flock of Canada geese at approximately 180 knots during rotation. Multiple strikes ingested into engine #1 and engine #2. Crew initiated immediate emergency return and executed safe overweight landing on Runway 04R.',
                'date_time': now - timedelta(days=2, hours=3),
                'location': 'JFK / John F. Kennedy International',
                'aircraft_type': 'Boeing 777-300ER',
                'category': Incident.CATEGORY_BIRD_STRIKE,
                'severity': Incident.SEVERITY_CRITICAL,
                'status': Incident.STATUS_INVESTIGATING,
            },
            {
                'title': 'Severe Clear-Air Turbulence Enroute FL360',
                'description': 'Aircraft experienced unexpected severe clear-air turbulence over mountainous terrain without radar precipitation echo. Altitude deviation of +/- 450 feet occurred. Two flight attendants sustained minor contusions.',
                'date_time': now - timedelta(days=5, hours=7),
                'location': 'Waypoint BUM / Denver FIR Airspace',
                'aircraft_type': 'Airbus A350-900',
                'category': Incident.CATEGORY_WEATHER,
                'severity': Incident.SEVERITY_HIGH,
                'status': Incident.STATUS_UNDER_REVIEW,
            },
            {
                'title': 'Unscheduled Hydraulic System B Depressurization',
                'description': 'Low pressure caution alert triggered for Hydraulic System B during descent through 14,000 feet. Fluid quantity indicated near zero. Alternate flap extension protocol completed successfully.',
                'date_time': now - timedelta(days=8, hours=1),
                'location': 'ORD / Chicago O\'Hare International',
                'aircraft_type': 'Boeing 737-800',
                'category': Incident.CATEGORY_TECHNICAL_FAULT,
                'severity': Incident.SEVERITY_MEDIUM,
                'status': Incident.STATUS_CLOSED,
            },
            {
                'title': 'Taxiway Centerline Deviation During Low Visibility',
                'description': 'During night CAT III operations with 300m RVR, nose gear briefly deviated onto the soft shoulder taxiway edge due to confusing lighting signals during construction.',
                'date_time': now - timedelta(days=12, hours=11),
                'location': 'FRA / Frankfurt Airport',
                'aircraft_type': 'Airbus A330-300',
                'category': Incident.CATEGORY_HUMAN_ERROR,
                'severity': Incident.SEVERITY_LOW,
                'status': Incident.STATUS_REPORTED,
            },
        ]

        created_count = 0
        for item in sample_incidents:
            obj, was_created = Incident.objects.get_or_create(
                title=item['title'],
                defaults={
                    **item,
                    'reported_by': user
                }
            )
            if was_created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {created_count} demo incident records!'))
