"""
    Description: Home devices discovery.
"""

import os
import socket
import subprocess
from datetime import datetime

from library.customkv import StorageWrapper
    

def gather_homenetwork_devices(subnet="192.168.1.0/24"):

    results = []; allhosts = []; allips = []

    #---------------------------#
    # Initialize storage caches #
    #---------------------------#
    homeips = StorageWrapper("iplkup")
    homehosts = StorageWrapper("hostlkup")


    #------------------------#
    # Execute fping commands #
    #------------------------#
    proc = subprocess.Popen(f'fping -g {subnet}'.split(),
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT
                            )

    stdout_value = proc.communicate()[0]

    #----------------#
    # Gather results #
    #----------------#
    for aline in stdout_value.decode('utf-8').split("\n"):

        if "is alive" in aline:
            hstinfo = {}

            hstinfo['ipaddr'] = aline.split()[0]
            hstinfo['hostname'] = socket.getfqdn(hstinfo['ipaddr'])
            hstinfo['timestamp'] = f"{datetime.now()}" 

            hstkey = hstinfo['hostname'].replace(".fios-router.home", "").lower()

            # Collect into various formats
            results.append(hstinfo)
            allhosts.append(hstkey)
            allips.append(hstinfo['ipaddr']);
            homeips.add_kv(hstinfo['ipaddr'], hstinfo)
            homehosts.add_kv(hstkey, hstinfo)

    homeips.add_kv("allips", allips)
    homehosts.add_kv("allhosts", allhosts)


def test_hostlookup(hostname):

    # Sample lookup
    homehosts = StorageWrapper("hostlkup")
    key, value = homehosts.get_kv(hostname.lower())
    print(f"Current ip address - Bose {value['ipaddr']}")


if __name__ == '__main__':

    gather_homenetwork_devices()
    test_hostlookup("cuckoosoundtouch")
