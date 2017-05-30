from django import forms
from django.core.validators import RegexValidator


class XoxzoCallForm(forms.Form):
    phone_regex = RegexValidator(regex=r'^\+\d{9,15}$',
                                 message='Phone number must be between 9 to 15 digits and in the format +999999999')
    caller_num = forms.CharField(label='Caller number', max_length=16, validators=[phone_regex])
    recording_url = forms.URLField(label='Recording url', max_length=500)