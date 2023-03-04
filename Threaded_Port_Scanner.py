import socket
import sys
from datetime import datetime
import threading

# Prompt the user to enter an IP address or hostname and port range
ip_or_hostname = input("Enter the IP address or hostname to scan: ")
start_port = int(input("Enter the start port: "))
end_port = int(input("Enter the end port: "))

# Check if the input is a valid IP address, and convert a hostname to an IP address if necessary
try:
    ip_address = socket.inet_aton(ip_or_hostname)
    ip_address = ip_or_hostname
except socket.error:
    try:
        ip_address = socket.gethostbyname(ip_or_hostname)
    except socket.gaierror:
        print("Invalid IP address or hostname")
        sys.exit()

# Add a banner
print('-' * 50)
print("Scanning Started: "+ip_address)
print("Port Range: {} - {}".format(start_port, end_port))
print("Time Started: "+str(datetime.now()))
print("Made By Asad Iqbal")
print('-' * 50)

# Define a function to scan a range of ports
def scan_ports(start_port, end_port, protocol):
    for port in range(start_port, end_port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM if protocol == 'udp' else socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            result = s.connect_ex((ip_address,port)) if protocol == 'tcp' else s.sendto(b'', (ip_address, port))
            if result == 0:
                print("{} port is open: {}".format(protocol.upper(), port))
            s.close()
        except KeyboardInterrupt:
            print("Scan interrupted by user")
            sys.exit()
        except socket.gaierror:
            print("Hostname could not be resolved. Exiting")
            sys.exit()
        except socket.error:
            print("Could not connect to server")
            sys.exit()

# Create multiple threads to scan different ranges of ports
threads = []
num_threads = 10
ports_per_thread = 10
total_ports = end_port - start_port + 1
ports_per_thread = min(ports_per_thread, total_ports)
for i in range(num_threads):
    thread_start_port = start_port + i * ports_per_thread
    thread_end_port = min(end_port, thread_start_port + ports_per_thread)
    thread = threading.Thread(target=scan_ports, args=(thread_start_port, thread_end_port, 'tcp'))
    threads.append(thread)
    thread.start()
for i in range(num_threads):
    thread_start_port = start_port + i * ports_per_thread
    thread_end_port = min(end_port, thread_start_port + ports_per_thread)
    thread = threading.Thread(target=scan_ports, args=(thread_start_port, thread_end_port, 'udp'))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

# Print a message indicating that the scan is complete
print('-' * 50)
print("Scanning Finished: "+ip_address)
print("Time Finished: "+str(datetime.now()))
print('-' * 50)
