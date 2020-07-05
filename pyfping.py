"""
    Description: Home devices discovery.
"""

import os
import socket
import subprocess

from datetime import datetime

from library.customkv import StorageWrapper
    

def gather_homenetwork_devices(subnet="192.168.1.0/24"):
    """
        Description: Actual logic of gathering ips and hostnames
        are implemented here.
    """
    results = []; allhosts = None; allips = None 

    #---------------------------#
    # Initialize storage caches #
    #---------------------------#
    homeips = StorageWrapper("iplkup")
    homehosts = StorageWrapper("hostlkup")

    # Continue to store/maintain previously discovered hosts
    _, allips = homeips.get_kv("allips")
    _, allhosts = homehosts.get_kv("allhosts")

    # Following maybe applicable only the first time
    if not allips: allips = []
    if not allhosts: allhosts = []

    for idx, ahost in enumerate(allhosts):
        print(f"host[{idx}]: {ahost}")

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
            hstinfo = {} #Initializing only if a valid host

            hstinfo['ipaddr'] = aline.split()[0]
            hstinfo['hostname'] = socket.getfqdn(hstinfo['ipaddr'])
            hstinfo['last discovered'] = f"{datetime.now()}" 

            hstkey = hstinfo['hostname'].replace(".fios-router.home", "").lower()

            # Collect/update into various formats
            results.append(hstinfo)
            homeips.add_kv(hstinfo['ipaddr'], hstinfo)
            homehosts.add_kv(hstkey, hstinfo)

            # Prevent duplicates
            if hstkey not in allhosts:
                allhosts.append(hstkey)

            if hstinfo['ipaddr'] not in allips:
                allips.append(hstinfo['ipaddr']);

    homeips.add_kv("allips", allips)
    homehosts.add_kv("allhosts", allhosts)


def test_hostlookup(hostname):
    """ 
        Description: Test a lookup by hostname
    """
    # Sample lookup
    homehosts = StorageWrapper("hostlkup")
    key, value = homehosts.get_kv(hostname.lower())
    print(f"\n\nTesting - Speaker ip address - Bose {value['ipaddr']}")


if __name__ == '__main__':

    gather_homenetwork_devices()
    test_hostlookup("cuckoosoundtouch")
