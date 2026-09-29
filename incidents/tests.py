from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Incident


class SkyShieldTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='capt_sully',
            email='sully@skyshield.aero',
            password='TestPassword123!'
        )
        self.staff_user = User.objects.create_user(
            username='admin_officer',
            email='admin@skyshield.aero',
            password='AdminPassword123!',
            is_staff=True
        )
        self.incident = Incident.objects.create(
            title='Dual Engine Bird Ingestion',
            description='Flock of Canadian geese collided with engines during climbout.',
            date_time=timezone.now(),
            location='LGA / LaGuardia Departure',
            aircraft_type='Airbus A320',
            category=Incident.CATEGORY_BIRD_STRIKE,
            severity=Incident.SEVERITY_CRITICAL,
            status=Incident.STATUS_INVESTIGATING,
            reported_by=self.user
        )
        self.staff_incident = Incident.objects.create(
            title='Runway Incursion Safety Audit',
            description='Supervisory investigation of runway 28L crossing without authorization.',
            date_time=timezone.now(),
            location='SFO / San Francisco',
            aircraft_type='Boeing 787-9',
            category=Incident.CATEGORY_HUMAN_ERROR,
            severity=Incident.SEVERITY_HIGH,
            status=Incident.STATUS_UNDER_REVIEW,
            reported_by=self.staff_user
        )

    def test_incident_model_str(self):
        self.assertIn('Critical', str(self.incident))
        self.assertIn('Dual Engine Bird Ingestion', str(self.incident))
        self.assertIn('Airbus A320', str(self.incident))

    def test_incident_list_view(self):
        response = self.client.get(reverse('incident_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dual Engine Bird Ingestion')
        self.assertContains(response, 'Airbus A320')
        self.assertTemplateUsed(response, 'incidents/incident_list.html')
        # Check 3D tilted world map and animated flight elements
        self.assertContains(response, 'world-radar-hero')
        self.assertContains(response, 'world-radar-tilt-container')
        self.assertContains(response, 'radar-svg-canvas')
        self.assertContains(response, 'flight-del-lhr')
        # Check 4 flashcards
        self.assertContains(response, 'Incident Reporting')
        self.assertContains(response, 'Report New Incident')
        self.assertContains(response, 'Superuser Incidents')
        self.assertContains(response, 'Admin Console')

    def test_incident_list_filtering(self):
        # Filter by category
        res = self.client.get(reverse('incident_list'), {'category': 'bird_strike'})
        self.assertEqual(len(res.context['incidents']), 1)

        # Filter by non-matching category
        res2 = self.client.get(reverse('incident_list'), {'category': 'weather'})
        self.assertEqual(len(res2.context['incidents']), 0)

    def test_incident_list_staff_only_filtering(self):
        # Filter by staff/superuser only
        res = self.client.get(reverse('incident_list'), {'staff_only': '1'})
        self.assertEqual(len(res.context['incidents']), 1)
        self.assertEqual(res.context['incidents'][0].title, 'Runway Incursion Safety Audit')

    def test_incident_detail_view(self):
        response = self.client.get(reverse('incident_detail', kwargs={'pk': self.incident.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dual Engine Bird Ingestion')
        self.assertContains(response, 'Flock of Canadian geese')
        self.assertTemplateUsed(response, 'incidents/incident_detail.html')

    def test_incident_detail_404(self):
        response = self.client.get(reverse('incident_detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)

    def test_incident_create_requires_login(self):
        response = self.client.get(reverse('incident_create'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_incident_create_authenticated(self):
        self.client.login(username='capt_sully', password='TestPassword123!')
        response = self.client.get(reverse('incident_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'incidents/incident_form.html')

        post_data = {
            'title': 'Hydraulic Pressure Fluctuation',
            'description': 'System B hydraulic pressure fluctuated below 2500 psi on approach.',
            'date_time': '2026-09-28T14:30',
            'location': 'ORD / O\'Hare',
            'aircraft_type': 'Boeing 737-800',
            'category': 'technical_fault',
            'severity': 'high',
            'status': 'reported',
        }
        post_res = self.client.post(reverse('incident_create'), post_data)
        self.assertEqual(post_res.status_code, 302)

        new_incident = Incident.objects.get(title='Hydraulic Pressure Fluctuation')
        self.assertEqual(new_incident.reported_by, self.user)
        self.assertEqual(new_incident.severity, 'high')

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'first_officer',
            'password1': 'SecureOfficerPass123!',
            'password2': 'SecureOfficerPass123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='first_officer').exists())

    def test_user_logout(self):
        self.client.login(username='capt_sully', password='TestPassword123!')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
