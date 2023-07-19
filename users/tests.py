from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from notes.models import Note
from django.contrib.auth import login
from notes_app import settings

# Create your tests here.

def create_default_user():
    User.objects.create_user(username='te_amo', email="amote@hotmail.com", password="him")

def create_new_active_user():
    User.objects.create_user(username='tomer', email='icecoldtomi@hotmail.hot', password='greenIgzNHem')

def create_new_inactive_user():
    new_user = User.objects.create_user(username='timmytim', email='stickynotesapp605@gmail.com', password='rosettastown')
    new_user.is_active = False
    new_user.save()

class TestBasicAuthentication(TestCase):
    def setUp(self):
        create_new_inactive_user()
        create_new_active_user()
        create_default_user()

    def test_new_user_created_successfully(self):
        new_user = User.objects.get(pk=1)
        existing_users = len(User.objects.filter(is_active=False))
        self.assertEqual(existing_users, 1)
        self.assertEqual(new_user.username, 'timmytim')
        self.assertEqual(new_user.email, 'stickynotesapp605@gmail.com')

    def test_user_default_permission(self):
        new_user = User.objects.get(pk=1)
        self.assertNotEqual(new_user.is_superuser, True)
        self.assertNotEqual(new_user.is_active, True)

    def test_user_login(self):
        login = self.client.login(username='te_amo', password="him")
        self.assertEqual(login, True)

    def test_user_login_view(self):
        login_details = {"username": 'tomer', "password": 'greenIgzNHem'}
        response = self.client.post('/users/login', login_details, follow=True)
        redirected_path = response.request["PATH_INFO"]
        self.assertEqual(redirected_path, '/')

    def test_user_logout(self):
        self.client.login(username='tomer', password="greenIgzNHem")
        self.client.logout()


class TestUserAuthentication(TestCase):

    def setUp(self):
        create_new_inactive_user()
        create_new_active_user()
        create_default_user()

    def test_signup_user_correctly(self):
        signup_details = {
            'username': 'test_user', 
            'email': 'tomisinak156@gmail.com',
            'fname': 'Tomi',
            'lname': 'Snow',
            'password1': 'tombelwied',
            'password2': 'tombelwied'
        }
        try:
            response = self.client.post('/users/signup', signup_details, follow=True)
            self.assertEqual(response.request['PATH_INFO'], '/users/login')
            new_user = User.objects.get(username="test_user")
            self.assertFalse(new_user.is_active == True)
        except TimeoutError:
            print('SMTP not working')

    def test_signup_user_incorrectly_username_exists(self):
        signup_details = {
            'username': 'te_amo', 
            'email': 'tomisinak156@gmail.com',
            'fname': 'Tomi',
            'lname': 'Snow',
            'password1': 'tombelwied',
            'password2': 'tombelwied'
        }
        
        response = self.client.post('/users/signup', signup_details, follow=True)
        error_message = str(list(response.context['messages'])[0])
        self.assertNotEqual(response.request['PATH_INFO'], '/users/login')
        self.assertEqual("The username \"te_amo\" already exists. Please try a different one", error_message)

    def test_signup_user_incorrectly_username_not_alphanumeric(self):
        signup_details = {
            'username': 'test_user*', 
            'email': 'tomisinak156@gmail.com',
            'fname': 'Tomi',
            'lname': 'Snow',
            'password1': 'tombelwied',
            'password2': 'tombelwied'
        }
        
        response = self.client.post('/users/signup', signup_details, follow=True)
        error_message = str(list(response.context['messages'])[0])
        self.assertNotEqual(response.request['PATH_INFO'], '/users/login')
        self.assertEqual("Usernames must contain only letters, numbers or underscores \"_\"", error_message)
        

    def test_signup_user_incorrectly_username_too_long(self):
        signup_details = {
            'username': 'test_usertest_usertest_usertest_user', 
            'email': 'tomisinak156@gmail.com',
            'fname': 'Tomi',
            'lname': 'Snow',
            'password1': 'tombelwied',
            'password2': 'tombelwied'
            }
        
        response = self.client.post('/users/signup', signup_details, follow=True)
        error_message = str(list(response.context['messages'])[0])
        self.assertNotEqual(response.request['PATH_INFO'], '/users/login')
        self.assertEqual("Username must be 30 characters or less", error_message)


    def test_signup_user_incorrectly_email_exists(self):
        signup_details = {
            'username': 'test_user', 
            'email': 'amote@hotmail.com',
            'fname': 'Tomi',
            'lname': 'Snow',
            'password1': 'tombelwied',
            'password2': 'tombelwied'
            }
        
        response = self.client.post('/users/signup', signup_details, follow=True)
        error_message = str(list(response.context['messages'])[0])
        self.assertNotEqual(response.request['PATH_INFO'], '/users/login')
        self.assertEqual("Email already registered to an account", error_message)

    def test_signup_user_incorrectly_password_not_matching(self):
        signup_details = {
            'username': 'test_user', 
            'email': 'tomisinak156@gmail.com',
            'fname': 'Tomi',
            'lname': 'Snow',
            'password1': 'tombelwied',
            'password2': 'tombelweid'
            }
        
        response = self.client.post('/users/signup', signup_details, follow=True)
        error_message = str(list(response.context['messages'])[0])
        self.assertNotEqual(response.request['PATH_INFO'], '/users/login')
        self.assertEqual("Passwords do not match", error_message)

    # test user activation

    def test_user_change_password(self):
        self.client.login(username="tomer", password="greenIgzNHem")
        new_password_info = {
            'pass1': 'tomado',
            'pass2': 'tomado'
            }
        response  = self.client.post('/users/change_password', new_password_info, follow=True)
        login_status = self.client.login(username='tomer', password='tomado')
        self.assertEqual(login_status, True)

    def test_user_forgot_password_email_registered(self):
        context = {
            'email': 'stickynotesapp605@gmail.com'
        } 
        try:
            response = self.client.post('/users/login/forgot_password', context, follow=True)
            response_message = str(list(response.context['messages'])[0])
            self.assertTrue(response_message == "A Password Reset Link has been sent. Check your Email.")
        except TimeoutError:
            print('SMTP not working')

    def test_user_forgot_password_email_not_registered(self):
        context = {
            'email': 'tomskiii@gmail.com'
        } 
        response = self.client.post('/users/login/forgot_password', context, follow=True)
        response_message = str(list(response.context['messages'])[0])
        self.assertTrue(response_message == f'There are no registered accounts with the email "{context["email"]}"')
