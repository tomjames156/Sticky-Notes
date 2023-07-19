from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from notes.models import DisplayMode
from notes_app.settings import EMAIL_HOST_USER
from .tokens import generate_token
from django.core.mail import send_mail

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if not(user == None):
            login(request, user)
            messages.info(request, (f'Welcome back {user.username}'))
            return redirect('notes:home')
        else:
            messages.error(request, ("Username or Password Incorrect"))
            return redirect('users:login')
    else:
        return render(request, 'authenticate/login.html')

def validate_username(username_input):
    import re

    UserNameRegex = re.compile(r'^([a-zA-Z0-9_]*)$')
    valid_username = UserNameRegex.match(username_input).group()
    return valid_username

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        context = {
                "details": {
                    'username': username,
                    'email': email,
                    'fname': fname,
                    'lname': lname
                    }
                }

        if User.objects.filter(username=username):
            messages.error(request, (f"The username \"{username}\" already exists. Please try a different one"))
            context['details'].pop('username')
            return render(request, 'authenticate/signup.html', context)
        
        if User.objects.filter(email=email):
            messages.error(request, ("Email already registered to an account"))
            context['details'].pop('email')
            return render(request, 'authenticate/signup.html', context)
        
        if len(username) > 30:
            messages.error(request, ("Username must be 30 characters or less"))
            context['details'].pop('username')
            return render(request, 'authenticate/signup.html', context)
        
        try:
            validate_username(username)
        except AttributeError:
            messages.error(request, ("Usernames must contain only letters, numbers or underscores \"_\""))
            context['details'].pop('username')
            return render(request, 'authenticate/signup.html', context)

        if password1 == password2:
            new_user = User.objects.create_user(first_name=fname, last_name=lname, username=username, email=email, password=password1)
            new_user.is_active = False
            new_user.save()
            messages.success(request, ('Your account has successfully been created. We have sent you a confirmation email, please confirm your email in order to activate your account.'))

            """Welcome email"""

            # Define the email details
            from_email = EMAIL_HOST_USER
            to_email = new_user.email
            subject = "Welcome to Sticky Notes App"
            body = f"Welcome {new_user.first_name}!!\nWelcome to Sticky Notes.\nThankyou for visiting the website \nWe have also sent you a confirmation email, please confirm your email address in order to activate your account.\n\nThanking You,\nAkinwande Tomisin"

            send_mail(subject, body, from_email, recipient_list=[to_email])

            # Email Address Confirmation Email

            current_site = get_current_site(request)
            email_subject = "Confirm your email for Sticky Notes App"
            email_body = render_to_string('authenticate/email_confirmation.html', {
                'fname': new_user.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': generate_token.make_token(new_user)
            })

            send_mail(email_subject, email_body, EMAIL_HOST_USER, recipient_list=[new_user.email], fail_silently=False)

            return redirect('users:login')
        else:
            messages.error(request, ("Passwords do not match"))
            return render(request, 'authenticate/signup.html', context)

    return render(request, 'authenticate/signup.html')

def sign_out(request):
    logout(request)
    messages.success(request, 'Logged Out Successfully')
    return redirect('notes:home')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        new_user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        new_user = None

    if new_user is not None and generate_token.check_token(new_user, token):
        new_user.is_active = True
        new_user.save()
        login(request, new_user)
        DisplayMode.objects.create(user=new_user, display_mode="light-mode")
        return redirect('notes:home')
    else:
        return render(request, 'authenticate/activation_failed.html')
    
def forgot_pass(request):
    if request.method == "POST":
        user_email = request.POST['email']
        try:
            user = User.objects.get(email=user_email)

            # Password Reset Email

            current_site = get_current_site(request)
            email_subject = "Reset your Password for Sticky Notes App"
            email_body = render_to_string('authenticate/password_reset.html', {
                'fname': user.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })

            send_mail(email_subject, email_body, EMAIL_HOST_USER, recipient_list=[user.email], fail_silently=False)
            messages.success(request, ("A Password Reset Link has been sent. Check your Email."))
        except User.DoesNotExist:
            messages.error(request, (f'There are no registered accounts with the email "{user_email}"'))
    
    return render(request, 'authenticate/forgot_pass.html')

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        login(request, user)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    global reset_link
    reset_link = request.path_info

    return render(request, 'authenticate/reset_password.html', {"username": user.username})

def change_password(request):
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        if request.method == "POST":
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']

            if pass1 == pass2 :
                user.set_password(pass1)
                user.save()
                logout(request)
                messages.success(request, ("Your password was successfully changed. Login with your new password"))
                return redirect('users:login')
            else:
                messages.error(request, ('Passwords do not match'))
                return redirect(reset_link)
    else:
        messages.error(request, ("Password Reset Failed🥲"))
        return render('users:forgot_pass')