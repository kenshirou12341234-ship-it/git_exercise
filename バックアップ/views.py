from django.contrib.auth import login
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import EmailAuthenticationForm, RegistrationForm
from django.contrib import messages

class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('for_reinhardt')

    def form_valid(self, form):
        print("=== form_valid が呼ばれました ===")
        user = form.save()
        print(f"=== ユーザーを作成しました: {user.username}, {user.email} ===")
    
        login(self.request, user, backend='accounts.backends.EmailBackend')
        messages.success(self.request, f"ようこそ、{user.username} さん。")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("=== form_invalid が呼ばれました ===")
        print(f"=== フォームエラー: {form.errors} ===")
        return super().form_invalid(form)

class LoginView(DjangoLoginView):
    template_name = 'accounts/login.html'
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True

class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy('accounts:login')