
# These are all built-in, no 'pip install' needed!
import argparse         # For parsing command-line arguments (e.g., --file)
import subprocess       # For running the 'ping' command
import platform         # For checking if the OS is Windows or Linux/macOS
import concurrent.futures 


def ping_ip(ip, timeout_sec, timeout_ms):
    """
    Pings a single IP address and returns 'UP' or 'DOWN'.
    """
    

    if platform.system().lower() == 'windows':
        
        command = ['ping', '-n', '1', '-w', '1000', ip]
    else:
        
        command = ['ping', '-c', '1', '-W', '1', ip]

    try:
        result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        
        if result.returncode == 0:
            print(f"{ip} is UP")
            return (ip, "UP")
        else:
            print(f"{ip} is DOWN")
            return (ip, "DOWN")
            
    except Exception as e:
      
        print(f"Error pinging {ip}: {e}")
        return (ip, "ERROR")


def get_args():
    """
    Sets up and parses command-line arguments.
    """
    parser = argparse.ArgumentParser(description="A fast, multi-threaded IP ping utility.")
    
    parser.add_argument("-f", "--file", dest="filename", required=True,
                        help="File containing a list of IP addresses.")
    
  
    parser.add_argument("-t", "--timeout", dest="timeout", type=int, default=1,
                        help="Ping timeout in seconds. Default is 1.")
    
    parser.add_argument("-o", "--output", dest="outfile",
                        help="Optional: File to write results to.")
  
    
    return parser.parse_args()


def main():

    args = get_args()
    
    timeout_ms = str(args.timeout * 1000) 
    timeout_sec = str(args.timeout)
    print(f"--- Pinging IPs from {args.filename} (Multi-Threaded) ---")
    
    # Read all IPs from the file
    try:
        with open(args.filename, 'r') as f:
        
            ips = [line.strip() for line in f if line.strip()]
            
    except FileNotFoundError:
        print(f"Error: File '{args.filename}' not found.")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        
        print("Starting parallel ping...")
            
          
        results = list(executor.map(lambda ip: ping_ip(ip, timeout_sec, timeout_ms), ips))
       

    print("--- Ping complete ---")

    if args.outfile:
            print(f"Writing results to {args.outfile}...")
            try:
                with open(args.outfile, 'w') as f:
                    f.write("--- NetProbe Results ---\n")
                    for ip, status in results:
                        f.write(f"{ip}: {status}\n")
                print("Done.")
            except Exception as e:
                print(f"Error writing to file: {e}")
if __name__ == "__main__":
    main()