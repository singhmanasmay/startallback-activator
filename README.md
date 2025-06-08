# StartAllBack Activator

This script modifies Windows registry entries to reset the trial period for [StartAllBack](https://www.startallback.com/), a popular Windows customization tool.

> [!NOTE]
> This script is intended for educational purposes only. It is recommended to purchase a legitimate license to support the developers.

## Installation

1. Download the latest release from the releases page
3. Run the downloaded file `StartAllBack Activator.exe`

Or run from source:

1. Clone this repository
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Run `StartAllBack Activator.pyw`

> [!TIP]
> A minimal dependency terminal based version is also available as [StartAllBack Activator(basic)](StartAllBack Activator(basic).py)
## Requirements

- Windows 10 1507 and above
- StartAllBack must be installed
- Python 3.x (if running from source)
- Python packages in [requirements.txt](requirements.txt) (if running from source)

## Usage

1. Make sure [StartAllBack](https://www.startallback.com/) is installed on your system
2. Run the script with administrator privileges:
   ```
   python startallback-activator.py
   ```
3. The script will:
   - Search for StartAllBack registry entries
   - Reset the trial period if found
   - Display appropriate messages
4. Press any key to exit after the operation is complete

## [License](LICENSE)
