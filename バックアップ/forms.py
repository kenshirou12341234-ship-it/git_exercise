from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'ユーザー名'
        self.fields['email'].label = 'メールアドレス'
        self.fields['password1'].label = 'パスワード'
        self.fields['password2'].label = 'パスワード(確認)'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'block w-full px-3 py-2 border border-gray-300 rounded-md'

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('このメールアドレスは既に登録されています。')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='メールアドレス',
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )