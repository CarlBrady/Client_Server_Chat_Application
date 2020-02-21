
# Echo client program
import socket
import threading

HOST = '127.0.0.1'    # The remote host
PORT = 50007          # The same port as used by the server



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))



# when we send data to the server, we are using a colon
# at the end of a sentence to mark the end of the current sentence
# later when the input comes back, we will then be breaking the input
# into individual parts using the colon : to separate the lines
def readInput(s):

    print "Input Username:"
    name = raw_input()

    print "type input:"
    text = raw_input()

    # <msg-name-actualmessage>
    if "<anon>" in text:
        print "command in data.."
        s.sendall('<msg-'+ text + ">")


    else:
        s.sendall('<msg-'+ name +'-'+ text + ">")


t = threading.Thread(target=readInput, args = (s,))
t.start()

data = s.recv(80000)


print "Response:" + str(data)

s.close()
