from django_rq import job
from urllib.parse import quote
from .settings import api_call
import requests
from .models import XoxzoCallStatus


@job
def call_task(user, recipient, caller_num, recording_url, sid, auth):
    caller_num_en = quote(caller_num)
    recipient_en = quote(recipient)
    recording_url_en = quote(recording_url)

    payload = "caller={}&recipient={}&recording_url={}".format(caller_num_en, recipient_en, recording_url_en)
    headers = {
        'content-type': "application/x-www-form-urlencoded",
    }

    authentication = (sid, auth)

    data = XoxzoCallStatus(call_made_by=user, recipient=recipient, caller_num=caller_num,
                           status_code='PENDING',
                           status='PENDING',
                           call_id='PENDING',
                           recording_url=recording_url)

    data.save()

    res = requests.request("POST", api_call, data=payload, headers=headers, auth=authentication)

    if res.status_code == 201:
        status_code = res.status_code
        status = 'Called'
        callid = res.text
        callid = callid.split('callid')[1].split('"')[2]
    else:
        status_code = res.status_code
        status = res.text.split('detail')[1].split('"')[2]
        callid = 'None'

    XoxzoCallStatus.objects.filter(id=data.pk).update(status_code=status_code, status=status, call_id=callid)

