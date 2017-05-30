from django.shortcuts import render


def done_make_call(request, callid):
    return render(request, 'admin/xoxzo_call_api/done.html', {'callid': callid})
