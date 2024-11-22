from django.urls import path
from .views import signup_view, signin_view, signout_view, session_signup_view, session_signin_view, session_signout_view, update_password_view

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("signin/", signin_view, name="signin"),
    path("signout/", signout_view, name="signout"),
    path("session-signup/", session_signup_view, name="session_signup"),
    path("session-signin/", session_signin_view, name="session_signin"),
    path("session-signout/", session_signout_view, name="session_signout"),
    path("update-password/", update_password_view, name="update_password"),
]