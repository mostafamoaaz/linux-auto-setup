#!/usr/bin/python

import subprocess
import crypt
from mod1 import run_cmd


def user_exists(username):
    try:
        run_cmd(f"id {username}")
        return True
    except subprocess.CalledProcessError:
        return False

def create_user(username):
    if user_exists(username):
        print(f"User '{username}' already exists.")
    else:
        run_cmd(f"useradd {username}", capture=False)
        print(f"User '{username}' created.")

def set_password(username, password):
    run_cmd(f'echo "{username}:{password}" | chpasswd', capture=False)
    print(f"Password set for '{username}'.")


def add_to_sudo(username):
    run_cmd(f"usermod -aG wheel {username}", capture=False)
    print(f"'{username}' added to sudo group.")

def users_adding_process():
    print("Starting user setup...")

    # Define users
    users = ["admin1","developer1","viewer1"]

    for user in users:
        create_user(user)
        
        # Prompt for password securely (or use a decrypt() function here)
        pw = "1234"
        set_password(user, pw)

        if user == "admin1":
            add_to_sudo(user)

    print("User setup complete.")

if __name__ == "__main__":
    users_adding_process()
