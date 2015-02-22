#!/usr/bin/python

# This creates an API for xfer.AOKP.co
# Allows you to be able to poll for which users are available, which devices
# each user has, and what ROMs are available for download per device.
#
# Usage Examples:
#
# Request all available information: http://xfer.aokp.co/romlistings.py

import json
import os
from datetime import datetime

def listDevices(user):
    return os.listdir(user)

def listRoms(user,device):
    return os.listdir("%s/%s" % (user, device))

def getUrl(user, device, rom):
    return "http://xfer.aokp.co/%s/%s/%s" % (user, device, rom)


def getDate(user, device, rom):
    modified_date = os.path.getmtime("%s/%s/%s" % (user, device, rom))
    return datetime.fromtimestamp(modified_date).strftime("%Y-%m-%dT%H:%M:%S")

def showAll():
    data = {}
    with open('.users') as users_file:
        data['users'] = [
            {
                'name': user,
                'devices': [
                    {
                        'codename': device,
                        'roms': [
                            {
                                'filename': rom,
                                'url': getUrl(user, device, rom),
                                'date': getDate(user, device, rom)
                            }
                            for rom in listRoms(user, device) if not rom.startswith('.') if rom.endswith('zip')
                        ]
                    }
                    for device in listDevices(user) if not device.startswith('.') if os.path.isdir("%s/%s" % (user, device))
                ]
            }
            for user in users_file.read().splitlines()
        ]
    print(json.dumps(data))

def main():
    print("Content-type:application/json\n")
    showAll()

if __name__ == "__main__":
     main()
