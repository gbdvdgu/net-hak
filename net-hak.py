import socket
import threading
from queue import Queue
import re  
from colorama import Fore, init


init(autoreset=True)


def print_nethak_logo():
    red = Fore.RED
    yellow = Fore.YELLOW
    print(rf'''{red}

$$\   $$\            $$\     $$\   $$\           $$\       
$$$\  $$ |           $$ |    $$ |  $$ |          $$ |      
$$$$\ $$ | $$$$$$\ $$$$$$\   $$ |  $$ | $$$$$$\  $$ |  $$\ 
$$ $$\$$ |$$  __$$\\_$$  _|  $$$$$$$$ | \____$$\ $$ | $$  |
$$ \$$$$ |$$$$$$$$ | $$ |    $$  __$$ | $$$$$$$ |$$$$$$  / 
$$ |\$$$ |$$   ____| $$ |$$\ $$ |  $$ |$$  __$$ |$$  _$$<  
$$ | \$$ |\$$$$$$$\  \$$$$  |$$ |  $$ |\$$$$$$$ |$$ | \$$\ 
\__|  \__| \_______|  \____/ \__|  \__| \_______|\__|  \__|
                               
                            {yellow}GitHub: @gbdvdgu
                            MadeBy: Harsh Pratap Singh
''')


port_services = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    111: "RPC",  
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    5900: "VNC",
    8080: "HTTP Proxy",
    
}


queue = Queue()


def scan_port(ip, port, scan_type, timeout):
    try:
        if scan_type == 'TCP':
            
            tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_sock.settimeout(timeout)
            result_tcp = tcp_sock.connect_ex((ip, port))
            if result_tcp == 0:
               
                try:
                    tcp_sock.send(b'Hello\r\n')
                    banner = tcp_sock.recv(1024).decode('utf-8').strip()

                    
                    if re.search(r'<html>', banner, re.IGNORECASE):
                        banner = "HTML Response Truncated"

                except socket.timeout:
                    banner = 'No Banner'
                except socket.error:
                    banner = 'Error retrieving banner'

                
                service = port_services.get(port, "Unknown Service")
                print(f"Port {port}/TCP is open - {service} | Banner: {banner}")
            tcp_sock.close()

        elif scan_type == 'SYN':
            
            syn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            syn_sock.settimeout(timeout)
            result_syn = syn_sock.connect_ex((ip, port))
            if result_syn == 0:
                service = port_services.get(port, "Unknown Service")
                print(f"Port {port}/SYN is open - {service}")
            syn_sock.close()

    except Exception as e:
        pass


def thread_worker(ip, scan_type, timeout):
    while not queue.empty():
        port = queue.get()
        scan_port(ip, port, scan_type, timeout)
        queue.task_done()

def start_scanning(ip, start_port, end_port, scan_type, threads, timeout):
    print(f"Starting {scan_type} scan on {ip} from port {start_port} to {end_port}")

    
    for port in range(start_port, end_port + 1):
        queue.put(port)

    
    for _ in range(threads):
        thread = threading.Thread(target=thread_worker, args=(ip, scan_type, timeout))
        thread.daemon = True  
        thread.start()

    queue.join()  
    print("Scan complete!")


def get_user_input():
    ip = input("Enter IP address to scan: ")

    
    start_port = input("Enter start port [default 1]: ").strip() or 1
    end_port = input("Enter end port [default 65535]: ").strip() or 65535

    
    start_port = int(start_port)
    end_port = int(end_port)

    
    threads = input("Enter number of threads [default 200]: ").strip() or 200
    threads = int(threads)

    
    timeout = input("Enter timeout in seconds [default 1]: ").strip() or 1
    timeout = float(timeout)

    
    scan_type = input("Choose scan type (TCP/SYN): ").strip().upper()
    if scan_type not in ['TCP', 'SYN']:
        print("Invalid scan type, defaulting to TCP.")
        scan_type = 'TCP'

    return ip, start_port, end_port, scan_type, threads, timeout


if __name__ == "__main__":
    
    print_nethak_logo()
    ip, start_port, end_port, scan_type, threads, timeout = get_user_input()
    start_scanning(ip, start_port, end_port, scan_type, threads, timeout)
