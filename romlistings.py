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
import sys; sys.path = ["/var/www/androtransfer.com/public_html"] + sys.path
from datetime import datetime
from parse_config import parse_config

class getDetails:
    def __init__(self, user, device, rom):
        self.user = user
        self.device = device
        self.rom = rom

    def getUrl(self):
        return "http://xfer.aokp.co/%s/%s/%s" % (self.user, self.device, self.rom)

    def getDate(self):
        modified_date = os.path.getmtime("%s/%s/%s" % (self.user, self.device, self.rom))
        return datetime.fromtimestamp(modified_date).strftime("%Y-%m-%dT%H:%M:%S")

    def getSize(self):
        return os.path.getsize("%s/%s/%s" % (self.user, self.device, self.rom))

def listDevices(user):
    return os.listdir(user)

def listRoms(user,device):
    return os.listdir("%s/%s" % (user, device))

def getConfig(user, item):
    user_info = parse_config('user_info/%s' % (user))
    return user_info[item]

def showAll():
    data = {}
    with open('.users') as users_file:
        data['users'] = [
            {
                'name': user,
                'github': getConfig(user, 'github'),
                'gravatar': getConfig(user, 'gravatar'),
                'twitter': getConfig(user, 'twitter'),
                'devices': [
                    {
                        'codename': device,
                        'roms': [
                            (lambda g: {
                                'filename': rom,
                                'url': g.getUrl(),
                                'date': g.getDate(),
                                'size': g.getSize()
                            })(getDetails(user, device, rom))
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
