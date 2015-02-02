#!/usr/bin/python

# This creates an API for xfer.AOKP.co
# Allows you to be able to poll for which users are available, which devices
# each user has, and what ROMs are available for download per device.
#
# Usage Examples:
#
# Request all available information: http://xfer.aokp.co/romlistings.py?mode=all
# Users available: http://xfer.aokp.co/romlistings.py
# Devices available for specific User: http//xfer.aokp.co/romlistings.py?user=NAME
# ROMs available for download: http//xfer.aokp.co/romlistings.py?user=NAME&device=HARDWARE

import cgi
import json
import os
from datetime import datetime

params = cgi.FieldStorage()
mode = params.getvalue('mode')
user = params.getvalue('user')
device = params.getvalue('device')

def getDevs():
    data = []
    with open(".users") as f:
        contents = f.read().splitlines()
        for dev in contents:
            data.append({"name":dev})

    print(json.dumps(data))

def getDevices(user):
    data = []
    for f in os.listdir(user):
        if not f.startswith('.'):
            data.append({"devices":f})

    print(json.dumps(data))

def getRoms(user,device):
    data = []
    for f in os.listdir("%s/%s" % (user, device)):
        if not f.startswith('.'):
            url = "http://xfer.aokp.co/%s/%s/%s" % (user, device, f)
            modified_date = os.path.getmtime("%s/%s/%s" % (user, device, f))
            readable_date = datetime.fromtimestamp(modified_date).strftime("%Y-%m-%dT%H:%M:%S")
            data.append({"date":readable_date,"url":url})

    print(json.dumps(data))

def showDevices(user):
    devices = os.listdir(user)
    return devices

def showRoms(user,device):
    rom = os.listdir("%s/%s" % (user, device))
    return rom

def showDetails(user,device,rom):
    url = "http://xfer.aokp.co/%s/%s/%s" % (user, device, rom)
    modified_date = os.path.getmtime("%s/%s/%s" % (user, device, rom))
    readable_date = datetime.fromtimestamp(modified_date).strftime("%Y-%m-%dT%H:%M:%S")
    return url, readable_date

def showAll():
    data = {}
    with open(".users") as f:
        users = f.read().splitlines()
        for user in users:
            data[user] = {}
            for device in showDevices(user):
                if not device.startswith('.'):
                    data[user][device] = {}
                    for rom in showRoms(user,device):
                        if not rom.startswith('.'):
                            data[user][device][rom] = {}
                            u, d = showDetails(user, device, rom)
                            for url in u.splitlines():
                                data[user][device][rom]['url'] = url
                            for date in d.splitlines():
                                data[user][device][rom]['date'] = date

    print(json.dumps(data))

def main():
    print("Content-type:application/json\n")
    if mode == 'all':
        showAll()
    else:
        if user:
            if device:
                getRoms(user,device)
            else:
                getDevices(user)
        else:
            getDevs()

if __name__ == "__main__":
     main()
