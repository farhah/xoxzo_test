from django.contrib import admin
from django import forms
from .models import XoxzoPhoneBook
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from django.conf.urls import url
import requests
from urllib.parse import quote
from mezzanine.conf import settings
from .settings import api_call
from .forms import XoxzoCallForm
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from .views import done_make_call


class AddressForm(forms.ModelForm):
    name = forms.CharField()
    phone_num = forms.CharField()
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = XoxzoPhoneBook
        fields = ('name', 'phone_num', 'address')


class XoxzoAdmin(admin.ModelAdmin):
    form = AddressForm
    list_display = ('name', 'phone_num', 'call_action')

    def rest_call(self, recipient, caller_num, recording_url):
        caller_num_en = quote(caller_num)
        recipient_en = quote(recipient)
        recording_url_en = quote(recording_url)

        payload = "caller={}&recipient={}&recording_url={}".format(caller_num_en, recipient_en, recording_url_en)
        headers = {
            'content-type': "application/x-www-form-urlencoded",
        }

        authentication = (settings.XOXZO_SID, settings.XOXZO_AUTH)

        response = requests.request("POST", api_call, data=payload, headers=headers, auth=authentication)

        return response.text

    def process_call(self, request, recipient, name):
        if request.method == 'POST':
            form = XoxzoCallForm(request.POST)

            if form.is_valid():
                caller_num = form.cleaned_data['caller_num']
                recording_url = form.cleaned_data['recording_url']
                callid = self.rest_call(recipient, caller_num, recording_url)
                callid = callid.split('callid')[1].split('"')[2]
                # return redirect(done_make_call, callid=callid)
                return HttpResponseRedirect('/admin/xoxzo_call_api/xoxzophonebook/done/{}'.format(callid))
        else:
            form = XoxzoCallForm()

        context = self.admin_site.each_context(request)
        context['recipient'] = recipient
        context['name'] = name
        context['form'] = form
        context['title'] = 'Make a call to {} at {}'.format(name, recipient)

        return render(request, 'admin/xoxzo_call_api/call_action.html', context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<recipient>.+)/(?P<name>.+)/call/$',
                self.admin_site.admin_view(self.process_call),
                name='make-call',
            ),
            url(r'^done/(?P<callid>.*?)/$',
                done_make_call,
                name='make-call-done',)
        ]
        return custom_urls + urls

    def call_action(self, obj):
        return format_html(
            '<p><ul class="object-tools"><li><a class="focus" href="{}">Call this person</a></li></ul></p>',
            reverse('admin:make-call', args=[obj.phone_num, obj.name])

        )

    call_action.short_description = 'Call'
    call_action.allow_tags = True


admin.site.register(XoxzoPhoneBook, XoxzoAdmin)
