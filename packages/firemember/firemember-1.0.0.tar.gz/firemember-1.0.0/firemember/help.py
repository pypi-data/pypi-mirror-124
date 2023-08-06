import hashlib
import requests
import subprocess
import uuid
import socket
import os
import time

BY_IP = False
NAMEPC = socket.gethostname()
SPLITHASH = ".."

BASE_URL = "https://teak-fin-138114.firebaseio.com"


def popen(cmd):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    process = subprocess.Popen(cmd, startupinfo=startupinfo,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
    return process.stdout.read().decode('utf-8')


def get_ip():
    urlwiki = 'https://www.wikipedia.org'
    myip = requests.get(urlwiki).headers['X-Client-IP']
    IPAddr = socket.gethostbyname(NAMEPC)
    return hashlib.sha256(str(myip+IPAddr).encode('utf-8'))


def get_id(by_ip=False):
    hash_object = hashlib.sha256(uuid.uuid4().hex.encode('utf-8'))
    if by_ip:
        try:
            hash_home = get_ip()
        except Exception as e:
            time.sleep(1)
            print('ERROR get_id', e)
            return get_id()
    else:
        x = popen('wmic csproduct get UUID').replace('UUID', '').strip()
        hash_home = hashlib.sha256(x.encode('utf-8'))
    return NAMEPC+SPLITHASH+hash_home.hexdigest()+SPLITHASH+hash_object.hexdigest()


def check_offline(hash: str):
    _host, _home, _ = hash.split(SPLITHASH)
    host, home, _ = get_id().split(SPLITHASH)
    if host == _host and home == _home:
        return True
    return False


def check_online(base, key, hash):
    url = "%s/lisensi/%s/device/activation.json" % (base, key)
    v = requests.get(url)
    return v.json() == hash


def add_device(base, key, hash):
    url = "%s/lisensi/%s/device.json" % (base, key)
    data_ = {"id": NAMEPC, "activation": hash}
    res = requests.put(url, json=data_)
    return res.json() == data_
