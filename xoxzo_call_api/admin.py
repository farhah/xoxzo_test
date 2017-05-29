from django.contrib import admin
from django import forms
from .models import XoxzoPhoneBook
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from django.conf.urls import url
from .settings import caller_num, api_call, recording_url, auth, sid, auth_token
from django.template.response import TemplateResponse
import requests
from urllib.parse import quote


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

    def rest_call(self, recipient):
        caller_num_en = quote(caller_num)
        recipient_en = quote(recipient)
        recording_url_en = quote(recording_url)

        payload = "caller={}&recipient={}&recording_url={}".format(caller_num_en, recipient_en, recording_url_en)
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            # 'authorization': auth,
        }

        authentication = (sid, auth_token)

        response = requests.request("POST", api_call, data=payload, headers=headers, auth=authentication)

        return response.text

    def process_call(self, request, recipient, name, *args, **kwargs):
        return self.process_action(
            request=request,
            recipient=recipient,
            name=name,
            action_title='You have made a call to {} at {}'.format(name, recipient),
        )

    def process_action(self, request, recipient, name, action_title):

        # if request.method != 'POST':
        #     form = action_form()

        context = self.admin_site.each_context(request)
        context['recipient'] = recipient
        context['name'] = name
        context['title'] = action_title
        context['caller_num'] = caller_num
        context['api_call'] = api_call
        context['recording_url'] = recording_url
        context['auth'] = auth
        context['callid'] = self.rest_call(recipient)

        return TemplateResponse(
            request,
            'admin/xoxzo_call_api/call_action.html',
            context,
        )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<recipient>.+)/(?P<name>.+)/call/$',
                self.admin_site.admin_view(self.process_call),
                name='make-call',
            ),
        ]
        return custom_urls + urls

    def call_action(self, obj):
        return format_html(
            '<p><ul class="object-tools"><li><a class="focus" href="{}">Call this person</a></li></ul></p>',
            # '<input type="button" value="Call this person"></input>',
            reverse('admin:make-call', args=[obj.phone_num, obj.name])
            # '<p><ul class="object-tools"><li><a class="focus" href="#" title="Make a call using xoxzo api" '
            # 'onclick="MyFunction();return false;">'
            # 'Call this person</a></li></ul></p>'
        )

    call_action.short_description = 'Call'
    call_action.allow_tags = True


admin.site.register(XoxzoPhoneBook, XoxzoAdmin)
