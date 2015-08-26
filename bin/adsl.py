# -*- coding: utf-8 -*-
# reboot HINET ADSL VDSL2 DSL-6641K  to get new IP addr

import telnetlib
import time

def reset_adsl(host="192.168.1.1"):
    HOST = host
    user = "cht"
    password = "chtnvdsl"

    tn = telnetlib.Telnet(HOST)
    tn.read_until("login as: ")
    tn.write(user + "\n")
    tn.read_until("password: ")
    tn.write(password + "\n")
    tn.write("reboot\n")
    # block util reboot is done
    time.sleep(10)
    tn.write("exit\n")
    tn.close()

if __name__ == '__main__':
    eval("reset_adsl()")

