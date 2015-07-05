from client import LineClient, LineGroup, LineContact
import os
import time
from threding.Thread

try:
    client = LineClient(os.environ['LINE_ACCOUNT'],
                        os.environ['LINE_PASSWD'])
    #client = LineClient(authToken="AUTHTOKEN")
except:
    print "Login Failed"

def receive_msg(sleep=1):
while True:
    op_list = []

    for op in client.longPoll():
        op_list.append(op)

    for op in op_list:
        # receive msg from LINE server
        sender   = op[0]
        receiver = op[1]
        message  = op[2]
        
        msg = message.text
        receiver.sendMessage("[%s] %s" % (sender.name, msg))

    time.sleep(sleep)

def send_msg(sleep=1):
while True:
    client.get