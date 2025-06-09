import os
import winreg
import time
import threading
import functools
import customtkinter as ctk  # Custom tkinter for modern UI
import winaccent  # For Windows accent colors
from PIL import ImageColor

def dark(color):
    """Convert a color to a darker shade by reducing RGB values by 40%.
    Used for button hover effects in the UI.
    
    Args:
        color: A hex color string (e.g. '#ffffff')
    
    Returns:
        A hex color string representing the darker shade
    """
    rgb = list(ImageColor.getrgb(color))
    rgb[0], rgb[1], rgb[2]= int(rgb[0]*0.6), int(rgb[1]*0.6), int(rgb[2]*0.6)
    return '#%02x%02x%02x' % tuple(rgb)

def threaded(func):
    """Decorator to automatically launch a function in a thread.
    Used to prevent UI freezing when running long operations.
    
    Args:
        func: The function to be run in a separate thread
    
    Returns:
        wrapper: A function that creates and starts a thread for the given function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

def gui():
    """Creates and configures the main GUI window using customtkinter.
    Sets up the log display, output display, and activation button.
    """
    global textboxlog, textboxoutput, root, activatebutton, logframe
    root= ctk.CTk()

    width = 800
    height = 500
    root.geometry(f'{width}x{height}+{int((root.winfo_screenwidth()/2)-(width/2))}+{int((root.winfo_screenheight()/2)-(height/2))}')
    root.configure(fg_color='black')
    root.title('StartAllBack Activator')
    root.iconbitmap(os.path.join(os.path.dirname(__file__),'icon.ico'))
    ctk.set_appearance_mode("dark")

    logframe = ctk.CTkFrame(master=root,
                                fg_color='black',
                                border_color=winaccent.accent_normal,
                                border_width=2,
                                corner_radius=6)
    logframe.pack(side='top', fill='both', expand=True)
    textboxoutput = ctk.CTkTextbox(master=logframe,
                                    height=100,
                                    fg_color='#171717',
                                    state='disabled',
                                    corner_radius=6,
                                    activate_scrollbars=False,
                                    text_color=winaccent.accent_normal,
                                    font=('Arial',24))
    textboxoutput.pack(side='bottom', fill='x', padx=2, pady=2)
    textboxlog = ctk.CTkTextbox(master=logframe,
                                    fg_color='black',
                                    state='disabled',
                                    corner_radius=6,
                                    activate_scrollbars=False,
                                    font=('Arial',16))
    textboxlog.pack(side='left', fill='both', expand=True,padx=(2,0),pady=2)
    scbar = ctk.CTkScrollbar(master=logframe,
                                command=textboxlog.yview)
    textboxlog.configure(yscrollcommand=scbar.set)
    scbar.pack(side='right', fill='y', padx=(0,2), pady=2)

    buttonframe = ctk.CTkFrame(master=root,
                                height=50,
                                fg_color='black')
    buttonframe.pack(side='bottom', fill='x', expand=False)
    activatebutton = ctk.CTkButton(master=buttonframe,
                                height=50,
                                text='Activate',
                                font=('Segoe UI',20),
                                fg_color=winaccent.accent_normal,
                                text_color='black',
                                hover_color=dark(winaccent.accent_normal),
                                command=activate)
    activatebutton.pack(side='left', padx=(2,1), pady=2, fill='x', expand=True)

    root.mainloop()

init = True  # Flag to track first-time initialization

@threaded
def activate():
    """Main activation function that runs in a separate thread.
    Handles the Minecraft Bedrock activation process:
    1. Checks for admin privileges
    2. Verifies system directory existence
    3. Takes ownership of DLL files
    4. Modifies permissions
    5. Terminates processes using the DLL
    6. Replaces DLL files with modified versions
    """
    global textboxlog, textboxoutput, root, init, activatebutton, logframe

    def log(message):
        """Updates the log textbox with new messages.
        
        Args:
            message: The text message to append to the log
        """
        textboxlog.configure(state='normal')
        textboxlog.insert('end', message+'\n')
        textboxlog.configure(state='disabled')
        textboxlog.see('end')

    def output(message, color):
        """Updates the status output textbox and UI colors.
        
        Args:
            message: The status message to display
            color: The color to use for UI elements
        """
        textboxoutput.configure(state='normal')
        textboxoutput.delete("0.0", "end")
        textboxoutput.insert('end', message)
        textboxoutput.configure(state='disabled')
        textboxoutput.see('end')
        logframe.configure(border_color=color)
        textboxoutput.configure(text_color=color)
        activatebutton.configure(fg_color=color)
        activatebutton.configure(hover_color=dark(color))
        activatebutton.configure(state='disabled')

    if os.path.exists(os.path.join(os.environ['WINDIR'],'SYSTEM32')):
        system32exists = True
    else: system32exists = False

    # Main activation logic
    output('Activating','#0096FF')
    if init:
        init = False
        log('\n'.join(['██████╗░░█████╗░██╗░░░░░███████╗██████╗░░░███╗░░░█████╗░███╗░░██╗',
                       '██╔══██╗██╔══██╗██║░░░░░██╔════╝██╔══██╗░████║░░██╔══██╗████╗░██║',
                       '██████╦╝███████║██║░░░░░█████╗░░██████╔╝██╔██║░░██║░░██║██╔██╗██║',
                       '██╔══██╗██╔══██║██║░░░░░██╔══╝░░██╔══██╗╚═╝██║░░██║░░██║██║╚████║',
                       '██████╦╝██║░░██║███████╗███████╗██║░░██║███████╗╚█████╔╝██║░╚███║',
                       '╚═════╝░╚═╝░░╚═╝╚══════╝╚══════╝╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚══╝','https://github.com/singhmanasmay','\n']))
        log(f'system32 exists= {system32exists}')

    if system32exists:
        try:
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
                        output('StartAllBack trial days reset back to 100.\nPlease restart StartAllBack','#00FF00')
                        os.popen(f'taskkill /f /pid {os.getpid()}')

            # If we reach here, StartAllBack registry entries were not found
            output('StartAllBack is not installed.','#FF0000')
        except Exception as e:
                log(str(e))
                output('An unexpected error occurred.\nPlease report at:\nhttps://github.com/singhmanasmay/minecraftbedrock-activator/issues','#FF0000')
    else:
        output('Unsupported OS\nPlease ensure you are running this script on a Windows system.','#FF0000')

gui()
