import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, init

init(autoreset=True)

def print_nethak_logo():
    red = Fore.RED
    yellow = Fore.YELLOW
    print(f'''{red}
███╗   ██╗███████╗████████╗██╗  ██╗ █████╗ ██╗  ██╗
████╗  ██║██╔════╝╚══██╔══╝██║  ██║██╔══██╗╚██╗██╔╝
██╔██╗ ██║█████╗     ██║   ███████║███████║ ╚███╔╝ 
██║╚██╗██║██╔══╝     ██║   ██╔══██║██╔══██║ ██╔██╗ 
██║ ╚████║███████╗   ██║   ██║  ██║██║  ██║██╔╝ ██╗
╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
                                                             
                            {yellow}GitHub: @gbdvdgu
                            MadeBy: Harsh Pratap Singh
''')

class TCPPortScanner:
    def __init__(self, target, start_port=1, end_port=1024, max_threads=100, timeout=1):
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.max_threads = max_threads
        self.timeout = timeout
        self.open_ports = []

    def scan_port(self, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((self.target, port))
            sock.close()
            if result == 0:
                return port
        except socket.error as e:
            print(f"Error scanning port {port}: {e}")
        except KeyboardInterrupt:
            print("\nUser interrupted the scan.")
            exit(1)
        return None

    def run(self):
        print(f"Starting scan on {self.target} from port {self.start_port} to {self.end_port}...\n")
        start_time = datetime.now()

        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = {executor.submit(self.scan_port, port): port for port in range(self.start_port, self.end_port + 1)}

            for future in as_completed(futures):
                port = futures[future]
                if future.result() is not None:
                    self.open_ports.append(port)
                    print(f"Port {port} is open on {self.target}.")

        end_time = datetime.now()
        total_time = (end_time - start_time).total_seconds()

        self.display_results(total_time)

    def display_results(self, total_time):
        print("\nScan completed!\n")
        if self.open_ports:
            print(f"Open ports on {self.target}:")
            for port in sorted(self.open_ports):
                service = self.get_service_name(port)
                print(f"Port {port}: Open ({service})")
        else:
            print(f"No open ports found on {self.target} in the range {self.start_port}-{self.end_port}.")
        print(f"\nScan completed in {total_time:.2f} seconds.")

    @staticmethod
    def get_service_name(port):
        try:
            return socket.getservbyport(port)
        except:
            return "Unknown Service"


def main():
    # Print Net-Hak logo before starting the scan
    print_nethak_logo()
    
    target = input("Enter the target IP address or hostname to scan: ").strip()

    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"Error resolving the hostname: {target}")
        return

    start_port = int(input("Enter the start port (default 1): ") or 1)
    end_port = int(input("Enter the end port (default 1024): ") or 1024)
    max_threads = int(input("Enter the number of threads (default 200): ") or 200)
    timeout = float(input("Enter the timeout in seconds (default 1): ") or 1)

    scanner = TCPPortScanner(target=target_ip, start_port=start_port, end_port=end_port, max_threads=max_threads, timeout=timeout)
    scanner.run()


if __name__ == '__main__':
    main()
