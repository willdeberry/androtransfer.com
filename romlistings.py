#!/usr/bin/python

import cgi
import json
import os
from datetime import datetime

params = cgi.FieldStorage()
user = params.getvalue('user')
device = params.getvalue('device')

def showDevs():
    data = []
    with open(".users") as f:
        contents = f.read().splitlines()
        for dev in contents:
            data.append({"name":dev})

    print(json.dumps(data))

def showDevices(user):
    data = []
    for f in os.listdir(user):
        if not f.startswith('.'):
            data.append({"devices":f})

    print(json.dumps(data))

def showRoms(user,device):
    data = {}
    for f in os.listdir("%s/%s" % (user, device)):
        if not f.startswith('.'):
            url = "http://xfer.aokp.co/%s/%s/%s" % (user, device, f)
            modified_date = os.path.getmtime("%s/%s/%s" % (user, device, f))
            readable_date = datetime.fromtimestamp(modified_date).strftime("%D")
            data[readable_date] = url

    print(json.dumps(data))

def main():
    print("Content-type:application/json\n")
    if user:
        if device:
            showRoms(user,device)
        else:
            showDevices(user)
    else:
        showDevs()

if __name__ == "__main__":
     main()
