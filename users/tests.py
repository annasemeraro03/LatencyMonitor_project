from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser

class LoginViewTest(TestCase):
    def test_login_with_unregistered_user(self):
        url = reverse('users:login')
        data = {
            'username': 'utente_non_registrato',
            'password': 'test'
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertContains(response, 'Credenziali non valide.')

    def test_login_with_unapproved_user(self):
        self.user = CustomUser.objects.create_user(
            username='utente_non_approvato',
            password='test1234!',
            email='utente@example.com',
            is_approved=False 
        )
        
        url = reverse('users:login')
        data = {
            'username': 'utente_non_approvato',
            'password': 'test1234!'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertContains(response, 'Il tuo account non è stato ancora abilitato.')
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_login_with_approved_user(self):
        CustomUser.objects.create_user(
            username='utente_approvato',
            password='test1234!',
            email='test@test.com',
            is_approved=True
        )
        url = reverse('users:login')
        data = {
            'username': 'utente_approvato',
            'password': 'test1234!'
        }
        response = self.client.post(url, data)

        self.assertRedirects(response, reverse('core:home'))
        self.assertIn('_auth_user_id', self.client.session)
    
class RegisterViewTest(TestCase):
    def test_get_register_view(self):
        url = reverse('users:register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertIn('form', response.context)
        self.assertFalse(response.context.get('registration_sent', False))

    def test_get_register_view_with_registration_sent(self):
        url = reverse('users:register') + '?registration_sent=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get('registration_sent', False))

    def test_post_register_valid(self):
        url = reverse('users:register')
        data = {
            'username': 'utente_test_valid',
            'email': 'test@test.com',
            'password1': 'test1234!',
            'password2': 'test1234!',
            'birth_date': '1970-01-01',
        }
        response = self.client.post(url, data)

        self.assertRedirects(response, '/users/register/?registration_sent=1')

        user = CustomUser.objects.filter(username='utente_test_valid').first()
        self.assertIsNotNone(user)
        self.assertTrue(user.is_researcher)

    def test_post_register_invalid(self):
        url = reverse('users:register')
        data = {
            'username': '',
            'email': 'test@test.com',
            'password1': 'test1234!',
            'password2': 'test1234!',  
            'birth_date': '1970-01-01',
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

        user_exists = CustomUser.objects.filter(username='utente_test_invalid').exists()
        self.assertFalse(user_exists)
        
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(form.errors)

class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='test',
            email='test@test.com',
            password='test1234!',
            is_approved=True
        )
        self.client.login(username='test', password='test1234!')
        self.url = reverse('users:profile')

    def test_get_profile_view_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertEqual(form.instance, self.user)

    def test_get_profile_view_unauthenticated_redirect(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)

    def test_post_profile_view_valid_data(self):
        data = {
            'email': 'test2@test.com',
            'birth_date': '1970-01-01',
        }
        response = self.client.post(self.url, data)

        self.assertRedirects(response, self.url)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'test2@test.com')
        self.assertEqual(str(self.user.birth_date), '1970-01-01')

    def test_post_profile_view_invalid_data(self):
        data = {
            'email': 'test', 
            'birth_date': '1970-01-01',
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(form.errors)