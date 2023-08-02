from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from forum.models import *

class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cat"].empty_label = "Категория не выбрана"

    class Meta:
        model = Posts
        fields = ["title", "content", "cat", "is_allow_comments"]
        widgets = {"content": forms.Textarea(attrs={"cols": 60, "rows": 10, 'placeholder': 'Введите содержание поста'}), 'title': forms.TextInput(attrs={'placeholder': 'Введите заголовок поста'})}

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) > 250:
            raise ValidationError("Длина превышает 250 символов", len(title))
        return title
    
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))    
    class Meta:
        model = Users
        fields = ('username', 'email', 'password1', 'password2')


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ["title", "content", "is_allow_comments"]
        widgets = {
            "content": forms.Textarea(),
        }
           
class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ["content"]
        widgets = {"content": forms.Textarea(attrs={'placeholder': 'Введите текст комментария', 'class': 'comment_textarea'})}