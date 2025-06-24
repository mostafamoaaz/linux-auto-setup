#!/usr/bin/python


import os
import pwd
import grp

def ensure_dir(path):
    """Create directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
    else:
        print(f"Directory already exists: {path}")

def change_owner(path, user):
    """Change owner and group of the directory."""
    uid = pwd.getpwnam(user).pw_uid
    gid = grp.getgrnam(user).gr_gid
    os.chown(path, uid, gid)
    print(f"Ownership set to {user}:{user} for {path}")

def set_permissions():
    html_dir = "/var/www/html"
    shared_dir = "/var/www/shared"

    # Ensure the directories exist
    ensure_dir(html_dir)
    ensure_dir(shared_dir)

    # Set ownership
    change_owner(html_dir, "developer1")
    change_owner(shared_dir, "admin1")

    # Set permissions: rwxr-xr-x (755)
    os.chmod(html_dir, 0o755)
    os.chmod(shared_dir, 0o755)
    print(f"Permissions set to 755 for both directories")

    print("Permissions and ownership set successfully.")

if __name__ == "__main__":
    set_permissions()

