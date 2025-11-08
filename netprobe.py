# --- 1. Import all the libraries you need ---
# These are all built-in, no 'pip install' needed!
import argparse         # For parsing command-line arguments (e.g., --file)
import subprocess       # For running the 'ping' command
import platform         # For checking if the OS is Windows or Linux/macOS
import concurrent.futures # We won't use this one today, but we will tomorrow

# --- 2. The function that does the pinging ---
def ping_ip(ip):
    """
    Pings a single IP address and returns 'UP' or 'DOWN'.
    """
    
    # Check the operating system to build the right command
    # -n 1 (Windows) or -c 1 (Linux/macOS) sends just ONE ping packet.
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', ip]

    # Run the ping command
    # We hide the output (stdout=subprocess.DEVNULL) because we only
    # care if it was successful (returncode == 0) or not.
    try:
        result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Check the result
        if result.returncode == 0:
            print(f"{ip} is UP")
            return (ip, "UP")
        else:
            print(f"{ip} is DOWN")
            return (ip, "DOWN")
            
    except Exception as e:
        # Catch any other errors
        print(f"Error pinging {ip}: {e}")
        return (ip, "ERROR")

# --- 3. The function that gets command-line arguments ---
def get_args():
    """
    Sets up and parses command-line arguments.
    """
    # Create the parser object
    parser = argparse.ArgumentParser(description="A fast, multi-threaded IP ping utility.")
    
    # Add the '--file' argument.
    # 'required=True' means the script won't run without it.
    parser.add_argument("-f", "--file", dest="filename", required=True,
                        help="File containing a list of IP addresses.")
    
    # Get the arguments from the command line
    return parser.parse_args()

# --- 4. The main part of your script ---
def main():
    """
    The main function to run the script.
    """
    # Get the --file argument
    args = get_args()
    
    print(f"--- Pinging IPs from {args.filename} (Sequential) ---")
    
    # Read all IPs from the file
    try:
        with open(args.filename, 'r') as f:
            # .strip() removes any blank lines or extra whitespace
            ips = [line.strip() for line in f if line.strip()]
            
    except FileNotFoundError:
        print(f"Error: File '{args.filename}' not found.")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # --- This is the simple, slow loop for Day 1 ---
    # We will replace this tomorrow
    for ip in ips:
        ping_ip(ip) # Ping the IPs one by one
    # ---

    print("--- Ping complete ---")

# --- 5. The entry point of the script ---
# This line says: "If this script is run directly (not imported),
# then call the main() function." This is standard Python practice.
if __name__ == "__main__":
    main()