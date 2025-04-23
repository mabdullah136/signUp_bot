from django import forms
from .models import BotJob

class BotJobForm(forms.ModelForm):
    class Meta:
        model = BotJob
        fields = ['target_url', 'username_prefix', 'limit']