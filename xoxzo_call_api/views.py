from django.shortcuts import render


def done_make_call(request):
    return render(request, 'admin/xoxzo_call_api/done.html', {})
