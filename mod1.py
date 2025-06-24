import subprocess


def run_cmd(cmd, capture=True,check=True):
    """Run a shell command."""
    result = subprocess.run(cmd, shell=True, check=check, capture_output=capture, text=True)
    if capture:
        return result.stdout.strip() 
    else:
        return None


def get_active_interface():
    """Detects the active network interface name (non-loopback, up)."""
    output = run_cmd(" - ", capture=True)
    for line in output.splitlines():
        device, state = line.split(":")
        if state == "connected" and device != "lo":
            return device #ens160
    raise RuntimeError("No active network interface found.")


def get_connection_name(interface):
    """Get the NetworkManager connection name associated with the interface."""
    output = run_cmd("nmcli -t -f NAME,DEVICE connection show", capture=True)
    for line in output.splitlines():
        name, dev = line.split(":")
        if dev == interface:
            return name # ens160
        # ens160:ens160
        # lo:lo
    raise RuntimeError(f"No connection found for interface {interface}")


def get_current_ip(interface):
    """Get the current IP address, gateway, and DNS of the given interface."""
    ip = run_cmd(f"nmcli -g IP4.ADDRESS dev show {interface}", capture=True)
    ip = ip.split("/")
    ip ,subnet= ip[0] ,ip[1]
    gateway = run_cmd(f"nmcli -g IP4.GATEWAY dev show {interface}", capture=True)
    dns = run_cmd(f"nmcli -g IP4.DNS dev show {interface}", capture=True)
    return ip, gateway, dns, subnet
# 192.168.161.135/24
# 192.168.161.2
# 192.168.161.2



def set_hostname(new_hostname):
    """Set and persist the system hostname."""
    print(f"Setting hostname to {new_hostname}")
    run_cmd(f"hostnamectl set-hostname {new_hostname}")


def set_static_ip(connection_name, ip, gateway, dns, subnet):
    """Configure the connection to use static IP."""
    print(f"Setting static IP {ip} for connection {connection_name}")
    run_cmd(f"nmcli con mod '{connection_name}' ipv4.addresses {ip}/{subnet}")
    run_cmd(f"nmcli con mod '{connection_name}' ipv4.gateway {gateway}")
    run_cmd(f"nmcli con mod '{connection_name}' ipv4.dns '{dns}'")
    run_cmd(f"nmcli con mod '{connection_name}' ipv4.method manual")
    # run_cmd(f"nmcli con down '{connection_name}'")
    run_cmd(f"nmcli con up '{connection_name}'")


def update_hosts_file(hostname):
    """Map new hostname to loopback address in /etc/hosts."""
    print(f"Adding {hostname} to /etc/hosts")
    line = f"127.0.0.1 {hostname} \n"
    with open("/etc/hosts", "a") as f:
        f.write(line)


def configure_system(new_hostname):
    """Run all tasks."""
    set_hostname(new_hostname)

    interface = get_active_interface()
    connection = get_connection_name(interface) #ens160
    ip, gateway, dns, subnet = get_current_ip(interface)
    set_static_ip(connection, ip, gateway, dns, subnet)

    update_hosts_file(new_hostname)
    print("Configuration completed successfully.")


# Example usage
if  __name__ == "__main__":
    configure_system("intranet.xyz.local")
