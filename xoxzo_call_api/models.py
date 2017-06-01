from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class XoxzoPhoneBook(models.Model):
    phone_regex = RegexValidator(regex=r'^\+\d{9,15}$',
                                 message='Phone number must be between 9 to 15 digits and in the format +999999999')

    name = models.CharField(max_length=200, blank=False, null=False)
    phone_num = models.CharField(max_length=16, validators=[phone_regex], blank=False)
    address = models.CharField(max_length=500, blank=True, null=True)
    owner = models.ForeignKey(User)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Xoxzo phone book"
        unique_together = (("phone_num", "owner"),)


class XoxzoCallStatus(models.Model):
    recipient = models.CharField(max_length=16, blank=False, null=False)
    caller_num = models.CharField(max_length=16, blank=False, null=False)
    recording_url = models.URLField(max_length=500, blank=False, null=False)
    call_made_by = models.ForeignKey(User)
    status_code = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    call_id = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Xoxzo call statuses"

