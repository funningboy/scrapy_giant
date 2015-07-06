from client import LineClient, LineGroup, LineContact
import os
import time
import threading

try:
    client = LineClient(os.environ['LINE_ACCOUNT'],
                        os.environ['LINE_PASSWD'])
    #client = LineClient(authToken="AUTHTOKEN")
except:
    print "Login Failed"

STOP = False

def receive_and_send_back_msg(sleep=1):
    while True:
        op_list = []

        for op in client.longPoll():
            op_list.append(op)

        for op in op_list:
            # loopback msg  
            sender   = op[0]
            receiver = op[1]
            message  = op[2]
        
            msg = message.text
            # stop at msg received 'stop'
            if msg == 'stop' or STOP:
                break
            receiver.sendMessage("[%s] %s" % (sender.name, msg))

        time.sleep(sleep)


threads = [
    threading.Thread(target=receive_and_send_back_msg, args=(1,))
]
[it.start() for it in threads]
[it.join() for it in threads]
