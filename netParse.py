#!/usr/bin/env python3

import sys
import os
import csv
from datetime import datetime
import ipaddress

# C2 Ports to watch
C2_PORTS = {'1337', '1338', '1339', '1340'}
INTERNAL_SUBNET = "10.10.10."
EXTERNAL_PREFIX = "255."

def is_internal(ip):
    return ip.startswith(INTERNAL_SUBNET)

def is_external(ip):
    return ip.startswith(EXTERNAL_PREFIX)

def epoch_to_date(epoch):
    try:
        return datetime.utcfromtimestamp(int(epoch)).strftime("%Y-%b-%d %H:%M:%S")
    except:
        return "Invalid Time"

def main():
    # Argument check
    if len(sys.argv) != 2:
        print("Error! - No Log File Specified!")
        return

    filename = sys.argv[1]

    # File existence check
    if not os.path.isfile(filename):
        print("Error! - File Not Found!")
        return

    print(f"Source File: {filename}")

    infected_systems = set()
    c2_servers = set()
    c2_data_totals = {}
    earliest_timestamp = None

    try:
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) != 8:
                    continue  # skip malformed rows

                time, src_ip, dst_ip, src_port, dst_port, bytes_sent, _, _ = row

                # Only consider traffic from internal to external on C2 ports
                if is_internal(src_ip) and is_external(dst_ip) and dst_port in C2_PORTS:
                    infected_systems.add(src_ip)
                    c2_servers.add(dst_ip)

                    # Track earliest time
                    ts = int(time)
                    if earliest_timestamp is None or ts < earliest_timestamp:
                        earliest_timestamp = ts

                    # Track bytes sent to C2
                    sent_bytes = int(bytes_sent)
                    c2_data_totals[dst_ip] = c2_data_totals.get(dst_ip, 0) + sent_bytes

        # Output
        print(f"\nSystems Infected: {len(infected_systems)}")
        sorted_infected = sorted(infected_systems, key=lambda ip: ipaddress.IPv4Address(ip))
        print("Infected System IPs:")
        print(sorted_infected)


        print(f"\nC2 Servers: {len(c2_servers)}")
        print("C2 Servers IPs:")
        sorted_C2 = sorted(c2_servers, key=lambda ip: ipaddress.IPv4Address(ip))
        print(sorted_C2)

        print(f"\nFirst C2 Connection: {epoch_to_date(earliest_timestamp)} UTC")

        sorted_c2_totals = sorted(c2_data_totals.items(), key=lambda x: x[1], reverse=True)
        print(f"\nC2 Data Totals: {sorted_c2_totals}")

    except Exception as e:
        print(f"Error during processing: {e}")

if __name__ == "__main__":
    main()
