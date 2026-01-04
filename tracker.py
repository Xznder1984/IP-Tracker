import os
import requests
import time
import colorama
import hashlib
from colorama import Fore, Style
from pathlib import Path

# Initialize colorama
colorama.init(autoreset=True)

logo = r"""
  _____ _____    _______ _____            _____ _  ________ _____  
 |_   _|  __ \  |__   __|  __ \     /\   / ____| |/ /  ____|  __ \ 
   | | | |__) |    | |  | |__) |   /  \ | |    | ' /| |__  | |__) |
   | | |  ___/     | |  |  _  /   / /\ \| |    |  < |  __| |  _  / 
  _| |_| |         | |  | | \ \  / ____ \ |____| . \| |____| | \ \ 
 |_____|_|         |_|  |_|  \_\/_/    \_\_____|_|\_\______|_|  \_\   
"""

HASH_FILE = "name.hash"

def hash_name(name):
    """Create SHA-256 hash of name"""
    return hashlib.sha256(name.encode()).hexdigest()

def get_user_name():
    """Get or create user name hash file"""
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, 'r') as f:
            return f.read().strip()
    else:
        print(Fore.YELLOW + "\n👤 First time setup - What's your name?")
        name = input(Fore.GREEN + "Enter your name: ").strip()
        if not name:
            name = "Anonymous"
        
        hashed_name = hash_name(name)
        with open(HASH_FILE, 'w') as f:
            f.write(hashed_name)
        
        print(Fore.CYAN + f"✅ Name saved securely as {HASH_FILE}")
        return hashed_name

def unhash_name(hashed_name):
    """Display user info (name is hashed for privacy)"""
    return f"User-{hashed_name[:8].upper()}"

def check_ip_real(ip):
    """Check if IP is real/public using multiple APIs"""
    apis = [
        f'https://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,isp,query',
        f'http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,isp,query',
        f'https://ipinfo.io/{ip}/json'
    ]
    
    for api_url in apis:
        try:
            r = requests.get(api_url, timeout=5)
            if r.status_code == 200:
                data = r.json()
                
                if 'status' in data:
                    if data['status'] == 'success':
                        return True, data
                    else:
                        return False, data.get('message', 'Unknown error')
                
                elif 'city' in data or 'country' in data:
                    return True, data
                
                return False, 'Invalid response format'
        except:
            continue
    
    return False, 'All APIs failed - No internet or IP blocked'

def main():
    # Get user identity
    user_hash = get_user_name()
    user_display = unhash_name(user_hash)
    
    print(f"\n{Fore.GREEN}👋 Welcome back, {user_display}!")
    time.sleep(1)
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + logo)
        print(Fore.MAGENTA + f"👤 Logged in as: {user_display}")
        os.system('title IP TRACKER - ' + user_display if os.name == 'nt' else '')
        
        print(Fore.YELLOW + "Commands: [Enter IP] to track | 'exit' to quit")
        user_input = input(Fore.GREEN + 'ENTER TARGET IP: ').strip().lower()
        
        if user_input == 'exit':
            print(Fore.RED + f"\n👋 Goodbye, {user_display}!")
            time.sleep(1)
            break
            
        if not user_input:
            print(Fore.YELLOW + "Please enter an IP address or 'exit'")
            input(Fore.CYAN + "Press Enter to continue...")
            continue
        
        print(Fore.BLUE + '🔍 Analyzing IP...')
        time.sleep(1)
        
        is_real, result = check_ip_real(user_input)
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + logo)
        print(Fore.WHITE + f'👤 {user_display}\n')
        print(Fore.WHITE + 'RESULTS\n')
        
        if is_real:
            data = result
            print(Fore.GREEN + '✅ IP IS REAL/PUBLIC')
            print(Fore.WHITE + f'Country: {data.get("country", "N/A")}')
            print(Fore.WHITE + f'Region:  {data.get("regionName", data.get("region", "N/A"))}')
            print(Fore.WHITE + f'City:    {data.get("city", "N/A")}')
            print(Fore.WHITE + f'ZIP:     {data.get("zip", "N/A")}')
            print(Fore.WHITE + f'ISP:     {data.get("org", data.get("isp", "N/A"))}')
            print(Fore.WHITE + f'IP:      {data.get("query", user_input)}')
        else:
            print(Fore.RED + '❌ IP NOT REAL/Fake/Private/Reserved')
            print(Fore.YELLOW + f'Reason: {result}')
        
        print('')
        input(Fore.CYAN + 'Press Enter to Track Another IP...')

if __name__ == "__main__":
    main()