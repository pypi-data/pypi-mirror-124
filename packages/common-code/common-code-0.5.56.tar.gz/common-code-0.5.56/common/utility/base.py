import time
import uuid
from datetime import datetime, timedelta


def dt_time(sub=8):
    sub = int(sub)
    nnn = time.time() - sub * 60 * 60
    dat = datetime.fromtimestamp(nnn)
    ttt = dat.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return ttt


def dt_now_time():
    nnn = time.time()
    dat = datetime.fromtimestamp(nnn)
    ttt = dat.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return ttt


def get_uuid():
    uid = str(uuid.uuid4())
    suid = "".join(uid.split("-"))
    return suid


def convert_time(_time):
    if '+' in _time:
        times = _time.split("+")
        _time = times[0]
        v = times[1]
        f_srt = '%Y-%m-%dT%H:%M:%S.%f' if '.' in _time else '%Y-%m-%dT%H:%M:%S'
        _time = datetime.strptime(_time, f_srt) + timedelta(hours=8 - int(v.split(':')[0]))
        _time = _time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    elif 'Z' in _time:
        f_srt = '%Y-%m-%dT%H:%M:%S.%fZ' if '.' in _time else '%Y-%m-%dT%H:%M:%SZ'
        _time = datetime.strptime(_time, f_srt) + timedelta(hours=8)
        _time = _time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    return _time
