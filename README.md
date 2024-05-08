# Python-Gcode-Sender: A G-Code Command Line Interface

Python-Gcode-Sender is a command-line tool designed to interact with the Moonraker API, enabling users to send G-code commands to 3D printers controlled by the Klipper firmware. It allows users to manage a list of IP addresses or hostnames for multiple printers, select a device from the list, and send commands directly from the console.

## Features

- **Manage IP Addresses/Hostnames**: Add, select, and delete IP addresses or hostnames from a saved list.
- **Send G-Code Commands**: Directly send G-code commands to your 3D printer via Moonraker's API.

## Installation

To use Pyraker, you'll need Python and the `requests` library installed on your machine. If you haven't already installed `requests`, you can do so using pip:

```bash
pip install requests

```


## Usage
To start the tool, simply run the script from your command line:

```bash
python pyraker.py

```
