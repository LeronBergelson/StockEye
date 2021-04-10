"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import WatchList

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class CreateWatchListForm(forms.ModelForm):
    class Meta:
        model = WatchList
        fields = ['watchList_name']
        exclude = ['user', 'stockResults', 'watchList_id']

class EditWatchListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditWatchListForm, self).__init__(*args, **kwargs)
        self.initial['stockResults'] = [s.pk for s in self.instance.stockResults.all()]
        self.initial['watchList_id'] = [self.instance.watchList_id]

    class Meta:
        model = WatchList
        fields = ['stockResults']
        exclude = ['watchList_name', 'user', 'watchList_id']

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']


