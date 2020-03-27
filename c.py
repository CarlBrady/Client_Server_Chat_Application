import socket
import sys
import threading 
import hashlib
from time import gmtime, strftime
import time

HOST = '127.0.0.1' #localhost
PORT = 50010 if len(sys.argv) < 2 or not sys.argv[1].isdigit() or int(sys.argv[1]) not in range(65536) else int(sys.argv[1])

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT)) #we call bind on the server and connect on the client
global name1

def read_input(s):
	while True:
		print "\n" + s.recv(1024)
		print "\nMessage: ",
		sys.stdout.flush()

def main():
	print "Welcome to the room <3"
	with open("getUserLog.txt", "a+") as f:
		for y in range(1):
			username = raw_input("Enter your username: ").replace("-", "_")
			f.write("%d\r\n"%(y+1) + repr(username)) #"This is the server record of USER names: %d\r\n"   

	print "Loading hit return ^__^"
	welcome = raw_input("type welcome message to all: ")
	s.send(username)

	t = threading.Thread(target=read_input, args = (s,))
	t.daemon = True
	t.start()

	while True:
		text = raw_input("Message: ").rstrip()
		s.send("{}-{}-{}".format(hashlib.sha224(text).hexdigest(), username, text))

if __name__ == "__main__":
	try:
		main()
	except (KeyboardInterrupt, EOFError):
		print()
