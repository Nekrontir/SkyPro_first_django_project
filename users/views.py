from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm, UserLoginForm
from .models import User

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Отправка приветственного письма
        subject = 'Добро пожаловать в наш сервис!'
        message = f'Здравствуйте, {self.object.email}!\n\nСпасибо за регистрацию.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.object.email]
        send_mail(subject, message, from_email, recipient_list)
        return response

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

class UserLogoutView(LogoutView):
    pass