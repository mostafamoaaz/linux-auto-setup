#!/usr/bin/python
import os
import subprocess
import pwd
import grp
import stat
import re
from mod1 import run_cmd
from colorama import init, Fore, Style

init(autoreset=True)

LOCAL_HOST = "intranet.xyz.local"

def log_step(description):
    print(f"{Fore.CYAN} ---> {description}...", end="", flush=True)

def log_success():
    print(f" {Fore.GREEN}[  OK  ]")

def log_fail(reason):
    print(f" {Fore.RED}[FAILED] {Style.RESET_ALL}- {reason}")

# --- MOD1: Hostname + Static IP ---
def check_hostname(expected_hostname=LOCAL_HOST):
    log_step("Checking hostname")
    actual_hostname = run_cmd("hostnamectl --static")
    if actual_hostname == LOCAL_HOST:
        log_success()
    else:
        log_fail(f"Expected '{LOCAL_HOST}', got '{actual_hostname}'")

def check_hosts_file(expected_hostname=LOCAL_HOST):
    log_step("Checking /etc/hosts mapping")
    try:
        with open("/etc/hosts") as f:
            content = f.read()
            if f"127.0.1.1 {expected_hostname}" in content or f"127.0.0.1 {expected_hostname}" in content:
                log_success()
            else:
                log_fail("Expected hostname mapping not found in /etc/hosts")
    except Exception as e:
        log_fail(str(e))

def get_static_ip_from_nmconnection():
    connection_dir = "/etc/NetworkManager/system-connections/"
    try:
        for file in os.listdir(connection_dir):
            full_path = os.path.join(connection_dir, file)
            with open(full_path, "r") as f:
                content = f.read()
                if "method=manual" in content:
                    for line in content.splitlines():
                        if line.startswith("address"):
                            return line.split("=")[1].split("/")[0]
    except Exception as e:
        log_fail(f"Error reading nmconnection: {e}")
    return None

def get_current_ip():
    output = run_cmd("ip a")
    matches = re.findall(r"inet (\d+\.\d+\.\d+\.\d+)/\d+", output)
    for ip in matches:
        if not ip.startswith("127."):
            return ip
    return None

def check_static_ip():
    log_step("Checking static IP")
    static_ip = get_static_ip_from_nmconnection()
    current_ip = get_current_ip()
    if static_ip and current_ip and static_ip == current_ip:
        log_success()
    else:
        log_fail(f"Configured: {static_ip}, Current: {current_ip}")

# --- MOD2: Users + Permissions ---
def check_user_exists(username):
    log_step(f"Checking user '{username}' existence")
    try:
        pwd.getpwnam(username)
        log_success()
    except KeyError:
        log_fail(f"User '{username}' not found")

def check_user_in_group(user, group):
    log_step(f"Checking '{user}' in group '{group}'")
    groups = run_cmd(f"groups {user}")
    if group in groups.split():
        log_success()
    else:
        log_fail(f"{user} is not in {group}")

# --- MOD3: Directory Ownerships + Perms ---
def check_ownership(path, expected_user):
    log_step(f"Checking ownership of {path}")
    try:
        stat_info = os.stat(path)
        actual_user = pwd.getpwuid(stat_info.st_uid).pw_name
        if actual_user == expected_user:
            log_success()
        else:
            log_fail(f"Owner is {actual_user}, expected {expected_user}")
    except FileNotFoundError:
        log_fail(f"{path} not found")

def check_permissions(path, expected_mode):
    log_step(f"Checking permissions of {path}")
    try:
        actual_mode = oct(os.stat(path).st_mode & 0o777)
        if actual_mode == oct(expected_mode):
            log_success()
        else:
            log_fail(f"Got {actual_mode}, expected {oct(expected_mode)}")
    except FileNotFoundError:
        log_fail(f"{path} not found")

# --- MOD4: Apache + Firewall/Selinux ---
def check_httpd_service():
    log_step("Checking httpd service status")
    active = run_cmd("systemctl is-active httpd")
    enabled = run_cmd("systemctl is-enabled httpd")
    if active == "active" and enabled == "enabled":
        log_success()
    else:
        log_fail(f"httpd - active: {active}, enabled: {enabled}")

def check_index_with_curl():
    log_step("Verifying Apache via curl")
    response = run_cmd(f"curl -s -o /dev/null -w '%{{http_code}}' http://{LOCAL_HOST}")
    if response == "200":
        log_success()
    else:
        log_fail(f"Curl returned HTTP {response}")

def check_selinux():
    log_step("Checking SELinux status")
    status = run_cmd("getenforce")
    if status.lower() == "disabled" or status == "Permissive":
        log_success()
    else:
        log_fail(f"SELinux is {status}")

def check_firewalld():
    log_step("Checking firewalld status")
    state = run_cmd("systemctl is-enabled firewalld", check=False)
    if state != "enabled":
        log_success()
    else:
        log_fail("Firewalld is still enabled")

# --- RUN ALL ---
def verify_all():
    print(f"{Fore.YELLOW}\nVerifying system setup...\n{'-' * 40}\n")

    # MOD1
    check_hostname()
    check_hosts_file()
    check_static_ip()

    # MOD2
    check_user_exists("admin1")
    check_user_exists("developer1")
    check_user_exists("viewer1")
    check_user_in_group("admin1", "wheel")

    # MOD3
    check_ownership("/var/www/html", "developer1")
    check_permissions("/var/www/html", 0o755)

    check_ownership("/var/www/shared", "admin1")
    check_permissions("/var/www/shared", 0o755)

    # MOD4
    check_httpd_service()
    check_index_with_curl()
    check_firewalld()
    check_selinux()

    print(f"\n{Fore.GREEN}✔️  All checks completed.\n")

if __name__ == "__main__":
    verify_all()








    
def show_off(image_path="ezgif.jpg", width=125):
    # Step 1: Install dependencies
    deps = "gcc make git autoconf automake libjpeg-devel"
    print("Installing dependencies...")
    run_cmd(f"sudo dnf install -y {deps}", capture=False)

    # Step 2: Clone jp2a if not already
    if not os.path.exists("jp2a"):
        print("Cloning jp2a repository...")
        run_cmd("git clone https://github.com/cslarsen/jp2a.git", capture=False)
    else:
        print("'jp2a' folder already exists. Skipping clone.")

    # Step 3: Build jp2a
    print("Building jp2a...")
    run_cmd("autoreconf --install", capture=False, check=False)
    run_cmd("./configure", capture=False, check=False)
    run_cmd("make", capture=False, check=False)
    run_cmd("sudo make install", capture=False, check=False)

    # Step 4: Display the image as ASCII
    print(f"\nShowing {image_path} as ASCII art:\n")
    run_cmd(f"jp2a --colors --width={width} {image_path}", capture=False)