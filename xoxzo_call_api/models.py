from django.db import models
from django.core.validators import RegexValidator


class XoxzoPhoneBook(models.Model):
    phone_regex = RegexValidator(regex=r'^\+\d{9,15}$',
                                 message='Phone number must be between 9 to 15 digits and in the format +999999999')

    name = models.CharField(max_length=200, blank=False, null=False)
    phone_num = models.CharField(max_length=16, unique=True, validators=[phone_regex], blank=False)
    address = models.CharField(max_length=500, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Xoxzo phone book"
