import requests
import os
import re


def manage_ip_addresses(mode='r', new_ip=None):
    #Manage IP addresses or hostnames stored in a file.
    file_path = 'saved_ips.txt'
    if mode == 'r':  # Read IPs from the file
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                ips = file.read().splitlines()
            return ips
        else:
            return []
    elif mode == 'w' and new_ip:  # Write a new IP to the file
        with open(file_path, 'a') as file:
            file.write(new_ip + '\n')
        return new_ip


def send_gcode_command(ip_address, command):
    # Send a G-code command to the Moonraker API.
    url = f"http://{ip_address}:7125/printer/gcode/script"
    data = {'script': command}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {'error': str(e)}


def classify_input(input_string):
    ip_regex = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
    hostname_regex = r"\b[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+\b"
    index_regex = r"^\d+$"

    if re.match(ip_regex, input_string):
        return "IP Address"
    elif re.match(hostname_regex, input_string):
        return "Hostname"
    elif re.match(index_regex, input_string):
        return "Index"
    return "Unknown format"


def main():
    print("Pyraker G-code command line tool")
    selected_ip = None
    while True:
        ips = manage_ip_addresses()

        if ips:
            print("-----------------------------------------------------------")
            print("Saved IP Addresses or Hostnames:")
            for idx, ip in enumerate(ips):
                print(f"{idx+1}. {ip}")
            print("Type 'exit' to quit, or 'delete <index>' to remove an IP address or hostname.")
            choice = input("Select an IP or hostname from the list (or type a new one): ")
            input_type = classify_input(choice)
            if choice.lower() == "exit":
                quit()
            elif input_type == "Index":
                print("Selected IP address or hostname:", ips[int(choice) - 1])
                selected_ip = ips[int(choice) - 1]
            elif input_type == "IP Address" or input_type == "Hostname":
                print("Selected IP address or hostname:", choice)
                selected_ip = choice
            elif choice.lower() == "delete " + str(idx + 1):
                ips.pop(idx)
                with open('saved_ips.txt', 'w') as file:
                    for ip in ips:
                        file.write(ip + '\n')
                print("IP address or hostname deleted.")
            else:
                print("Unknown input format. Please enter a valid IP address, hostname, or index from the list.")
        else:
            selected_ip = input("Enter a new IP address or hostname for your Moonraker server: ")
            manage_ip_addresses('w', selected_ip)

        print("Type 'exit' to quit.")
        while selected_ip is not None:
            command = input("Enter G-code command: ")
            if command.lower() == 'exit':
                break
            result = send_gcode_command(selected_ip, command)
            print("Response from Moonraker:", result)


if __name__ == "__main__":
    main()
