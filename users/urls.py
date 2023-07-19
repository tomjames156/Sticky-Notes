from django.urls import path, include
from .views import *

app_name = 'users'

urlpatterns = [
    path('login', login_user, name="login"),
    path('signup', signup, name="signup"),
    path('signout', sign_out, name="sign_out"),
    path('change_password', change_password, name="change_pass"),
    path('reset_password/<uidb64>/<token>', reset_password, name="reset_pass"),
    path('login/forgot_password', forgot_pass, name="forgot_pass"),
    path('activate/<uidb64>/<token>', activate, name="activate" )
]