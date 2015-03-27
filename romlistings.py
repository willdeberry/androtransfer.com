#!/usr/bin/python
"""
This creates an API for xfer.AOKP.co
Allows you to be able to poll for which users are available, which devices
each user has, and what ROMs are available for download per device.

Usage Examples:

Request all available information: http://xfer.aokp.co/romlistings.py
"""
from __future__ import print_function
import json
import os
from datetime import datetime
from parse_config import parse_config


class GetDetails(object):
    """Details class for a ROM associated with a device and user """
    def __init__(self, user, device, rom):
        self.user = user
        self.device = device
        self.rom = rom

    def get_url(self):
        """Return the URL string for this ROM"""
        return "http://xfer.aokp.co/%s/%s/%s" % (self.user, self.device,
                                                 self.rom)

    def get_date(self):
        """Return a nicely formatted last-modified string for this ROM"""
        modified_date = os.path.getmtime("%s/%s/%s" % (self.user, self.device,
                                                       self.rom))
        return datetime.fromtimestamp(modified_date).strftime(
            "%Y-%m-%dT%H:%M:%S")

    def get_size(self):
        """Return the file size for this ROM"""
        return os.path.getsize("%s/%s/%s" % (self.user, self.device, self.rom))


def list_devices(user):
    """Return a directory listing of devices for the specified user"""
    return os.listdir(user)


def list_roms(user, device):
    """Return a directory listing of ROMs for the specified user and device"""
    return os.listdir("%s/%s" % (user, device))


def get_config(user, item):
    """Return appropriate user info for a given item or None on failure"""
    try:
        user_info = parse_config('user_info/%s' % (user))
        return user_info[item]
    except IOError:
        pass
    except KeyError:
        pass
    return None


def show_all():
    """Return a JSON string containing all data"""
    data = {}
    with open('.users') as users_file:
        data['users'] = [
            {
                'name': user,
                'github': get_config(user, 'github'),
                'gravatar': get_config(user, 'gravatar'),
                'twitter': get_config(user, 'twitter'),
                'devices': [
                    {
                        'codename': device,
                        'roms': [
                            (lambda g: {
                                'filename': rom,
                                'url': g.get_url(),
                                'date': g.get_date(),
                                'size': g.get_size()
                            })(GetDetails(user, device, rom))
                            for rom in list_roms(user, device)
                            if not rom.startswith('.')
                            if rom.endswith('zip')
                        ]
                    }
                    for device in list_devices(user)
                    if not device.startswith('.')
                    if os.path.isdir("%s/%s" % (user, device))
                ]
            }
            for user in users_file.read().splitlines()
        ]
    return json.dumps(data)


def main():
    """Main function, shows all data as JSON"""
    print("Content-type:application/json\n")
    print(show_all())

if __name__ == "__main__":
    main()
