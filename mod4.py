#!/usr/bin/python
import os
import shutil
from mod1 import run_cmd
from mod3 import change_owner


def install_httpd():
    """Install the Apache HTTPD server."""
    print("Installing httpd...")
    run_cmd("yum install -y httpd", capture=False)
    print("httpd installed.")

def start_and_enable_httpd():
    """Start and enable the httpd service."""
    print("Starting and enabling httpd service...")
    run_cmd("systemctl start httpd", capture=False)
    run_cmd("systemctl enable httpd", capture=False)
    print("httpd service started and enabled.")

def create_index_html():
    """Copy pre-made index.html and image to /var/www/html/"""
    src_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(src_dir, "index.html")
    img_path = os.path.join(src_dir, "img.webp")

    dest_dir = "/var/www/html"
    dest_html = os.path.join(dest_dir, "index.html")
    dest_img = os.path.join(dest_dir, "img.webp")

    shutil.copy(html_path, dest_html)
    shutil.copy(img_path, dest_img)

    print("index.html and img.webp copied to /var/www/html")

    change_owner(dest_html, "developer1")
    change_owner(dest_img, "developer1")
    change_owner(dest_dir, "developer1")



def verify_website():
    """Verify website accessibility via curl."""
    print("Verifying website accessibility...")
    run_cmd("curl -s http://intranet.xyz.local")
    print("Website is accessible and content is correct.")


def disable_firewalld():
    print("Disabling firewalld...")
    run_cmd("systemctl stop firewalld", capture=False)
    run_cmd("systemctl disable firewalld", capture=False)
    print("firewalld stopped and disabled.")

def disable_selinux():
    print("Disabling SELinux (temporary and permanent)...")
    run_cmd("setenforce 0", capture=False)
    
    # Replace SELINUX=enforcing with SELINUX=disabled in /etc/selinux/config
    with open("/etc/selinux/config", "r") as file:
        config_lines = file.readlines()
    
    with open("/etc/selinux/config", "w") as file:
        for line in config_lines:
            if line.strip().startswith("SELINUX="):
                file.write("SELINUX=disabled\n")
            else:
                file.write(line)
    
    print("SELinux set to permissive now and disabled permanently.")

def main():
    disable_firewalld()
    disable_selinux()
    install_httpd()
    start_and_enable_httpd()
    create_index_html()
    verify_website()

if __name__ == "__main__":
    main()
