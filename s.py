import socket
import threading, Queue

from time import gmtime, strftime
import time


HOST = '127.0.0.1'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))




# This is the buffer string
# when input comes in from a client it is added
# into the buffer string to be relayed later
# to different clients that have connected
# Each message in the buffer is separated by a colon :
buffer = ""

# custom say hello command
def sayHello():
    print "----> The hello function was called"


# sample parser function. The job of this function is to take some input
# data and search to see if a command is present in the text. If it finds a
# command it will then need to extract the command.
def parseInput(data, con):
    print "parsing..."
    print str(data)

    parts = data.split('-')
    user = parts[1]
    message = parts[2].split('>')
    print str(message)

    # Checking for commands
    if "<getservertime>" in data:
        print "command in data.."
        formatted= strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        con.send(str(formatted))

    if "<getusername>" in data:
        print "command in data.."
        con.send(str(user))


    if "<leavechat>" in data:
        print "command in data.."
        con.close()

    if "<getallusers>" in data:
        print "command in data.."
        con.close()


    if "<playgame>" in data:
        print "command in data.."
        con.close()

    if "<kickuser>" in data:
        print "command in data.."
        con.close()



    if "<MOTD>" in data:
        print "command in data.."
        message = "May the force be with you"
        con.send(str(message))


    if "<ping>" in data:
        print "command in data.."
        message = "pong"
        con.send(str(message))


    if "<anon>" in data:
        print "command in data.."
        parts = data.split('-')
        message = parts[2].split('>')
        con.send(str(message))



# we a new thread is started from an incoming connection
# the manageConnection funnction is used to take the input
# and print it out on the server
# the data that came in from a client is added to the buffer.

def manageConnection(conn, addr):
    global buffer
    print 'Connected by', addr


    data = conn.recv(1024)

    parseInput(data, conn)# Calling the parser, passing the connection

    print "rec:" + str(data)
    conn.send(str(data))

    #conn.send(str(buffer))

    conn.close()


while 1:
    s.listen(1)
    conn, addr = s.accept()
    # after we have listened and accepted a connection coming in,
    # we will then create a thread for that incoming connection.
    # this will prevent us from blocking the listening process
    # which would prevent further incoming connections
    t = threading.Thread(target=manageConnection, args = (conn,addr))

    t.start()
