# Import required Windows-specific modules
import winreg  # For Windows registry operations
import time    # For getting current timestamp
import msvcrt  # For handling keyboard input
import os

init= True
if os.path.exists(os.path.join(os.environ['WINDIR'],'SYSTEM32')):
    system32exists = True
else: system32exists = False

if init:
    init = False
    print('\n'.join(['██████╗░░█████╗░██╗░░░░░███████╗██████╗░░░███╗░░░█████╗░███╗░░██╗',
                     '██╔══██╗██╔══██╗██║░░░░░██╔════╝██╔══██╗░████║░░██╔══██╗████╗░██║',
                     '██████╦╝███████║██║░░░░░█████╗░░██████╔╝██╔██║░░██║░░██║██╔██╗██║',
                     '██╔══██╗██╔══██║██║░░░░░██╔══╝░░██╔══██╗╚═╝██║░░██║░░██║██║╚████║',
                     '██████╦╝██║░░██║███████╗███████╗██║░░██║███████╗╚█████╔╝██║░╚███║',
                     '╚═════╝░╚═╝░░╚═╝╚══════╝╚══════╝╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚══╝','https://github.com/singhmanasmay','\n']))
    print(f'system32 exists= {system32exists}\n')
if not system32exists:
    print('Unsupported OS\nPlease ensure you are running this script on a Windows system.\nPress any key to continue...')
    msvcrt.getch()  # Wait for user input before closing
    quit()

def subkeys(registry, key):
    """
    Generator function that enumerates all subkeys of a given Windows registry key
    Args:
        registry: The registry hive to search in (e.g., HKEY_CURRENT_USER)
        key: The path to the registry key
    Yields:
        String: Name of each subkey, or None if no subkeys exist
    """
    # Open the registry key with full access permissions
    _key = winreg.OpenKey(winreg.ConnectRegistry(None, registry), key, 0, winreg.KEY_ALL_ACCESS)
    try:
        i = 0
        while True:
            # Enumerate through all subkeys
            subkey_name = winreg.EnumKey(_key, i)
            yield subkey_name
            i += 1
    except:
        # If no subkeys found (i=0), yield None
        if i == 0:
            yield None
        # Always close the registry key when done
        winreg.CloseKey(_key)

# Search for StartAllBack registry entries in Windows Explorer CLSID
for subkey in subkeys(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\CLSID"):
    # For each CLSID key, check its subkeys
    for sub_subkey in subkeys(winreg.HKEY_CURRENT_USER, f"Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\CLSID\\{subkey}"):
        # Skip system-related subkeys
        if sub_subkey != 'DefaultIcon' and sub_subkey != 'ShellFolder':
            # Update the activation timestamp to reset trial period
            winreg.SetValueEx(
                winreg.OpenKey(winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER), 
                              f"Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\CLSID\\{subkey}", 
                              0, 
                              winreg.KEY_ALL_ACCESS),
                'activator',                # Value name
                0,                          # Reserved parameter
                winreg.REG_QWORD,          # Value type (64-bit integer)
                int(time.time())           # Current timestamp
            )
            print('Startallback trial days reset back to 100.\nPress any key to continue...')
            msvcrt.getch()  # Wait for user input
            quit()

# If we reach here, StartAllBack registry entries were not found
print('Startallback is not installed.\nPress any key to continue...')
msvcrt.getch()  # Wait for user input before closing
