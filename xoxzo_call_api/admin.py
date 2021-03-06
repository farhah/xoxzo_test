from django.contrib import admin
from .models import XoxzoPhoneBook, XoxzoCallStatus
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from django.conf.urls import url
from .forms import XoxzoCallForm, AddressForm
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from .tasks import call_task


class XoxzoAdmin(admin.ModelAdmin):
    form = AddressForm
    list_display = ('name', 'phone_num', 'call_action')

    def get_queryset(self, request):
        qs = super(XoxzoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        obj.save()

    def process_call(self, request, recipient, name):
        if request.method == 'POST':
            form = XoxzoCallForm(request.POST)

            if form.is_valid():
                caller_num = form.cleaned_data['caller_num']
                recording_url = form.cleaned_data['recording_url']
                call_task.delay(request.user, recipient, caller_num, recording_url)  # send to queue to avoid io blocking
                return HttpResponseRedirect('/admin/xoxzo_call_api/xoxzophonebook/done/')
        else:
            form = XoxzoCallForm()

        context = self.admin_site.each_context(request)
        context['recipient'] = recipient
        context['name'] = name
        context['form'] = form
        context['title'] = 'Make a call to {} at {}'.format(name, recipient)

        return render(request, 'admin/xoxzo_call_api/call_action.html', context)

    def done_make_call(self, request):
        return render(request, 'admin/xoxzo_call_api/done.html', {})

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<recipient>.+)/(?P<name>.+)/call/$',
                self.admin_site.admin_view(self.process_call),
                name='make-call',
            ),
            url(r'^done/$',
                self.admin_site.admin_view(self.done_make_call),
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


class CallStatus(admin.ModelAdmin):
    list_display = ('caller_num', 'recipient', 'recording_url', 'call_made_by', 'status_code', 'status', 'call_id', 'date')

    def has_add_permission(self, request):
        #  to disable manual add of call status
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False

        return super(CallStatus, self).change_view(request, object_id, extra_context=extra_context)

    def get_queryset(self, request):
        qs = super(CallStatus, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(call_made_by=request.user)

admin.site.register(XoxzoPhoneBook, XoxzoAdmin)
admin.site.register(XoxzoCallStatus, CallStatus)
