import os
import subprocess

print("\033[1m" + "Welcome to the Tech Support Toolbox" + "\033[0m" + " \n Your options are: \n  (1) Ping \n  (2) IPConfig \n  (3) GetMac \n  (4) NSLookup")

def main():
    option = input("Type an option: ").lower()

    ping = ["1", "ip", "hostname", "ping"]
    ipconfig = ["2", "ipconfig", "ipconf"]
    getmac = ["3", "getmac", "mac", "whatmac"]
    nslookup = ["4", "nslookup", "ns", "lookup"]    
    
    if option in ping:
        pingFunc()
    elif option in ipconfig:
        ipconfigFunc()
    elif option in getmac:
        getmacFunc()
    elif option in nslookup:
        nslookupFunc()
    else:
        print("Please type a valid option")

def pingFunc():
    ip = input("Enter an IP address or Hostname to ping: ")
    pingOutput = os.system("ping -n 3 " + ip)
    if pingOutput == 1:
        print(ip + " isn't a valid IP or Hostname")
    else:
        print("Ping COMMAND ran successfully. This doesn't mean I pinged anything though!")
    return pingOutput

def ipconfigFunc():
    ipConfigOutput = os.system("ipconfig /all")
    print (ipConfigOutput)
    if ipConfigOutput == 1:
        print("Something went wrong but it really shouldn't have....")
    return ipConfigOutput

def getmacFunc():
    os.system("getmac")

def nslookupFunc():
    ip = input("Enter an IP address or Hostname to look up: ")
    os.system("nslookup " + ip)

if __name__ == "__main__":
    main()
