import os
import subprocess
import platform
import re
import socket
from datetime import datetime

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_platform():
    """Detect the operating system"""
    return platform.system()

def validate_input(user_input, input_type="hostname"):
    """Validate user input to prevent command injection"""
    if not user_input or len(user_input) > 255:
        return False
    
    if input_type == "hostname":
        # Allow valid hostnames and IP addresses
        pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-\.]{0,253}[a-zA-Z0-9])?$'
        return bool(re.match(pattern, user_input))
    elif input_type == "port":
        try:
            port = int(user_input)
            return 1 <= port <= 65535
        except ValueError:
            return False
    return True

def save_output(output, command_name):
    """Save command output to a file"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{command_name}_{timestamp}.txt"
        with open(filename, 'w') as f:
            f.write(output)
        print(f"{Colors.OKGREEN}Output saved to {filename}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}Failed to save output: {e}{Colors.ENDC}")

def print_menu():
    """Display the main menu"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*50}")
    print("   Welcome to the Tech Support Toolbox")
    print(f"{'='*50}{Colors.ENDC}\n")
    print("Your options are:")
    print(f"  {Colors.OKBLUE}(1) Ping              {Colors.ENDC} - Test connectivity to a host")
    print(f"  {Colors.OKBLUE}(2) Network Config    {Colors.ENDC} - Display network configuration")
    print(f"  {Colors.OKBLUE}(3) MAC Address       {Colors.ENDC} - Show MAC addresses")
    print(f"  {Colors.OKBLUE}(4) DNS Lookup        {Colors.ENDC} - Perform DNS lookup")
    print(f"  {Colors.OKBLUE}(5) Traceroute        {Colors.ENDC} - Trace route to destination")
    print(f"  {Colors.OKBLUE}(6) Port Scan         {Colors.ENDC} - Check if a port is open")
    print(f"  {Colors.OKBLUE}(7) Network Interfaces{Colors.ENDC} - List network interfaces")
    print(f"  {Colors.OKBLUE}(q) Quit{Colors.ENDC}\n")

def main():
    """Run the interactive Tech Support Toolbox menu loop"""
    while True:
        print_menu()
        option = input(f"{Colors.OKCYAN}Type an option: {Colors.ENDC}").lower().strip()

        ping = ["1", "ping"]
        netconfig = ["2", "ipconfig", "netconfig", "config"]
        getmac = ["3", "getmac", "mac"]
        nslookup = ["4", "nslookup", "dns", "lookup"]
        traceroute = ["5", "traceroute", "trace", "tracert"]
        portscan = ["6", "port", "portscan", "scan"]
        interfaces = ["7", "interfaces", "if", "ifconfig"]
        quit_cmd = ["q", "quit", "exit"]
        
        if option in ping:
            pingFunc()
        elif option in netconfig:
            netconfigFunc()
        elif option in getmac:
            getmacFunc()
        elif option in nslookup:
            nslookupFunc()
        elif option in traceroute:
            tracerouteFunc()
        elif option in portscan:
            portscanFunc()
        elif option in interfaces:
            interfacesFunc()
        elif option in quit_cmd:
            print(f"{Colors.OKGREEN}Thanks for using Tech Support Toolbox!{Colors.ENDC}")
            break
        else:
            print(f"{Colors.FAIL}Please type a valid option{Colors.ENDC}")
        
        input(f"\n{Colors.WARNING}Press Enter to continue...{Colors.ENDC}")

def pingFunc():
    """Ping a host with cross-platform support"""
    host = input(f"{Colors.OKCYAN}Enter an IP address or hostname to ping: {Colors.ENDC}").strip()
    
    if not validate_input(host):
        print(f"{Colors.FAIL}Invalid hostname or IP address{Colors.ENDC}")
        return 1
    
    os_type = get_platform()
    
    try:
        if os_type == "Windows":
            cmd = ["ping", "-n", "4", host]
        else:  # Linux, Darwin (macOS), etc.
            cmd = ["ping", "-c", "4", host]
        
        print(f"\n{Colors.OKBLUE}Pinging {host}...{Colors.ENDC}\n")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        output = result.stdout + result.stderr
        print(output)
        
        if result.returncode == 0:
            print(f"{Colors.OKGREEN}Ping successful!{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}Ping failed!{Colors.ENDC}")
        
        # Ask if user wants to save output
        save = input(f"{Colors.OKCYAN}Save output to file? (y/n): {Colors.ENDC}").lower()
        if save == 'y':
            save_output(output, "ping")
        
        return result.returncode
    
    except subprocess.TimeoutExpired:
        print(f"{Colors.FAIL}Ping timed out{Colors.ENDC}")
        return 1
    except Exception as e:
        print(f"{Colors.FAIL}Error: {e}{Colors.ENDC}")
        return 1

def netconfigFunc():
    """Display network configuration with cross-platform support"""
    os_type = get_platform()
    
    try:
        if os_type == "Windows":
            cmd = ["ipconfig", "/all"]
        else:  # Linux, macOS
            cmd = ["ifconfig"] if os_type == "Darwin" else ["ip", "addr"]
        
        print(f"\n{Colors.OKBLUE}Network Configuration:{Colors.ENDC}\n")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        output = result.stdout
        print(output)
        
        if result.returncode == 0:
            print(f"{Colors.OKGREEN}Command executed successfully{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}Command failed{Colors.ENDC}")
        
        # Ask if user wants to save output
        save = input(f"{Colors.OKCYAN}Save output to file? (y/n): {Colors.ENDC}").lower()
        if save == 'y':
            save_output(output, "netconfig")
        
        return result.returncode
    
    except FileNotFoundError:
        print(f"{Colors.FAIL}Command not found. Trying alternative...{Colors.ENDC}")
        # Fallback for Linux if ip command not available
        if os_type == "Linux":
            try:
                result = subprocess.run(["ifconfig"], capture_output=True, text=True)
                print(result.stdout)
                return result.returncode
            except FileNotFoundError:
                print(f"{Colors.FAIL}No network configuration command available{Colors.ENDC}")
                return 1
    except Exception as e:
        print(f"{Colors.FAIL}Error: {e}{Colors.ENDC}")
        return 1

def getmacFunc():
    """Display MAC addresses with cross-platform support"""
    os_type = get_platform()
    
    try:
        if os_type == "Windows":
            cmd = ["getmac"]
        elif os_type == "Darwin":  # macOS
            cmd = ["ifconfig"]
        else:  # Linux
            cmd = ["ip", "link", "show"]
        
        print(f"\n{Colors.OKBLUE}MAC Addresses:{Colors.ENDC}\n")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        output = result.stdout
        print(output)
        
        if result.returncode == 0:
            print(f"{Colors.OKGREEN}Command executed successfully{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}Command failed{Colors.ENDC}")
        
        # Ask if user wants to save output
        save = input(f"{Colors.OKCYAN}Save output to file? (y/n): {Colors.ENDC}").lower()
        if save == 'y':
            save_output(output, "mac")
        
        return result.returncode
    
    except Exception as e:
        print(f"{Colors.FAIL}Error: {e}{Colors.ENDC}")
        return 1

def nslookupFunc():
    """Perform DNS lookup with cross-platform support"""
    host = input(f"{Colors.OKCYAN}Enter a hostname or IP address to look up: {Colors.ENDC}").strip()
    
    if not validate_input(host):
        print(f"{Colors.FAIL}Invalid hostname or IP address{Colors.ENDC}")
        return 1
    
    try:
        cmd = ["nslookup", host]
        
        print(f"\n{Colors.OKBLUE}DNS Lookup for {host}:{Colors.ENDC}\n")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

        output = result.stdout + result.stderr
        print(output)

        # Ask if user wants to save output
        save = input(f"{Colors.OKCYAN}Save output to file? (y/n): {Colors.ENDC}").lower()
        if save == 'y':
            save_output(output, "nslookup")

        return result.returncode

    except subprocess.TimeoutExpired:
        print(f"{Colors.FAIL}DNS lookup timed out{Colors.ENDC}")
        return 1
    except Exception as e:
        print(f"{Colors.FAIL}Error: {e}{Colors.ENDC}")
        return 1

def tracerouteFunc():
    """Trace route to a host with cross-platform support"""
    host = input(f"{Colors.OKCYAN}Enter an IP address or hostname to trace: {Colors.ENDC}").strip()
    
    if not validate_input(host):
        print(f"{Colors.FAIL}Invalid hostname or IP address{Colors.ENDC}")
        return 1
    
    os_type = get_platform()
    
    try:
        if os_type == "Windows":
            cmd = ["tracert", host]
        else:  # Linux, macOS
            cmd = ["traceroute", host]
        
        print(f"\n{Colors.OKBLUE}Tracing route to {host}...{Colors.ENDC}")
        print(f"{Colors.WARNING}(This may take a while){Colors.ENDC}\n")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        output = result.stdout + result.stderr
        print(output)
        
        if result.returncode == 0:
            print(f"{Colors.OKGREEN}Trace complete!{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}Trace failed or incomplete{Colors.ENDC}")
        
        # Ask if user wants to save output
        save = input(f"{Colors.OKCYAN}Save output to file? (y/n): {Colors.ENDC}").lower()
        if save == 'y':
            save_output(output, "traceroute")
        
        return result.returncode
    
    except subprocess.TimeoutExpired:
        print(f"{Colors.FAIL}Traceroute timed out{Colors.ENDC}")
        return 1
    except FileNotFoundError:
        print(f"{Colors.FAIL}Traceroute command not found{Colors.ENDC}")
        return 1
    except Exception as e:
        print(f"{Colors.FAIL}Error: {e}{Colors.ENDC}")
        return 1

def portscanFunc():
    """Check if a specific port is open on a host"""
    host = input(f"{Colors.OKCYAN}Enter an IP address or hostname: {Colors.ENDC}").strip()
    
    if not validate_input(host):
        print(f"{Colors.FAIL}Invalid hostname or IP address{Colors.ENDC}")
        return 1
    
    port_input = input(f"{Colors.OKCYAN}Enter port number (1-65535): {Colors.ENDC}").strip()
    
    if not validate_input(port_input, "port"):
        print(f"{Colors.FAIL}Invalid port number{Colors.ENDC}")
        return 1
    
    port = int(port_input)
    
    try:
        print(f"\n{Colors.OKBLUE}Scanning port {port} on {host}...{Colors.ENDC}\n")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(3)
            result = sock.connect_ex((host, port))

        if result == 0:
            print(f"{Colors.OKGREEN}Port {port} is OPEN on {host}{Colors.ENDC}")

            # Try to get service name
            try:
                service = socket.getservbyport(port)
                print(f"{Colors.OKCYAN}Common service: {service}{Colors.ENDC}")
            except OSError:
                pass

            return_code = 0
        else:
            print(f"{Colors.FAIL}Port {port} is CLOSED on {host}{Colors.ENDC}")
            return_code = 1

        return return_code
    
    except socket.gaierror:
        print(f"{Colors.FAIL}Could not resolve hostname{Colors.ENDC}")
        return 1
    except socket.timeout:
        print(f"{Colors.FAIL}Connection timed out{Colors.ENDC}")
        return 1
    except Exception as e:
        print(f"{Colors.FAIL}Error: {e}{Colors.ENDC}")
        return 1

def interfacesFunc():
    """Display detailed network interface information"""
    try:
        print(f"\n{Colors.OKBLUE}Network Interfaces:{Colors.ENDC}\n")
        
        hostname = socket.gethostname()
        print(f"{Colors.OKGREEN}Hostname: {hostname}{Colors.ENDC}")
        
        try:
            local_ip = socket.gethostbyname(hostname)
            print(f"{Colors.OKGREEN}Local IP: {local_ip}{Colors.ENDC}\n")
        except socket.gaierror:
            print(f"{Colors.WARNING}Could not determine local IP{Colors.ENDC}\n")
        
        # Use platform-specific commands for detailed info
        os_type = get_platform()
        
        if os_type == "Windows":
            result = subprocess.run(["ipconfig"], capture_output=True, text=True)
        elif os_type == "Darwin":
            result = subprocess.run(["ifconfig"], capture_output=True, text=True)
        else:  # Linux
            try:
                result = subprocess.run(["ip", "addr"], capture_output=True, text=True)
            except FileNotFoundError:
                result = subprocess.run(["ifconfig"], capture_output=True, text=True)
        
        print(result.stdout)
        
        # Ask if user wants to save output
        save = input(f"{Colors.OKCYAN}Save output to file? (y/n): {Colors.ENDC}").lower()
        if save == 'y':
            save_output(result.stdout, "interfaces")
        
        return result.returncode
    
    except Exception as e:
        print(f"{Colors.FAIL}Error: {e}{Colors.ENDC}")
        return 1

if __name__ == "__main__":
    main()
