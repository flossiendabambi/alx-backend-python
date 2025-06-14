from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'parent_message']
        widgets = {
            'parent_message': forms.HiddenInput()
        }
