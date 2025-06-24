#!/usr/bin/python
import mod1
import mod2
import mod3
import mod4
import verify_setup


mod1.configure_system("intranet.xyz.local")
mod2.users_adding_process()
mod3.set_permissions()
mod4.main()

verify_setup.verify_all()

show_off()
