#simple client server building from scratch again. 
#with threads in mind 

import socket
import sys
import threading, Queue
import hashlib
import urllib2
import random
import datetime
from time import gmtime, strftime
import time

#Create socket for server and bind it

HOST = '127.0.0.1' #localhost
PORT = 50010 if len(sys.argv) < 2 or not sys.argv[1].isdigit() or int(sys.argv[1]) not in range(65536) else int(sys.argv[1])
COUNT = 0
users = {}
kicked = []
quotes = urllib2.urlopen("https://raw.githubusercontent.com/hashanp/qotd-server/master/qotd.txt").read().strip().split("\n")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', PORT))

# custom say hello command
def do_game(data, con):
	global game, rand
	print ("the secret answer = %d" % rand)
	guess = data.split('-')[2]
	if guess in ("exit", "quit"):
		game = False
	print(repr(guess))
	if not guess.isdigit() or int(guess) not in range(101):
		con.send("enter a number between 0 and 100")
	else:
		diff = int(guess) - rand
		if diff == 0:
			con.send("here's a rose --,-'-{@")
			game = False
		elif diff > 0:
			con.send("go lower")
		elif diff < 0: 
			con.send("go higher")

def ping_pong(data,con):
	start = time.time()
	response = strftime("%S") #%f is for milliseconds
	print ('message recieved at : ' + str(response) + 'seconds')
	print str(response)
	end = time.time()
	send_all('pong :' + str(start - end))

def count_messages(data, con):
	   print("count total messages ^{}^".format(COUNT))

def whoami(data,con):
		#List Comprehension Lesson
	findUser = [user for user in users if users[user] == con][0]
	# OR
	findUser = {v:k for k,v in users.items()}.get(con, "[no such user]")
	# Above is the same as below:
	# findUser = []
	# for user in users:
		# if users[user] == con:
			# findUser.append(user)
	# findUser = findUser[0]

	con.send("You are " + findUser)

#lets try parse the hash function here				  
def parse_hash(data, con):
	#ServerTotal = 1
	print "Hashing started .. " 
	if "-" in data: #sifting the hashed message with test
		print "Server: found a dash"
		hash, username, text = data.split('-', 2)
		if hash == hashlib.sha224(text).hexdigest():
			#total = 0
			#for count, item in enumerate(str(toHash)):
			print ("Server: HASH CHECK COMPLETE") #, count, "for message: ", item)  
			#print ("Server: HASH CHECK COMPLETE")
			#total += count + 1
			#print ("counting hash" + repr(toHash.count(data)))
			#ServerTotal = total / total 
			formatted = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
			response = "Server: Secure message verified hash from " + formatted + "-" + username + "-" + text
			print(response)
			#con.send(response)
			#print("Server: total messages =" + repr(ServerTotal))
		else:
			print "HASH CHECK FAILED"
			con.send("you have been banned")
	#print ("Outside the loops = " + repr(ServerTotal))
#the parse input command test the server to call this 
#function over and over 
          
def parse_input(data, con):
    print repr(data)
    #print time.time()
    with open("servertime.txt", "w+") as f:
	if "time" in data:
		print "command in data.."
		formatted = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
		print str(formatted)
		con.send(str(formatted))
		f.write("This is line %d\n" + formatted)

#a quit function using the sys call
def leave_chat(data, con):
    with open("quitServer.log", "w+") as f:
		print "command in data.."
		formatted = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
		print str("user" + repr(addr) + "left the chat on " + formatted)        
		con.sendi("see you later" + repr(addr))			
		f.write("Someone left the chat on " + formatted)

#edging in a little read out function here 
def help(data, con): 
    f = open("commandlist.txt", "r+")
    if "help" in data:
            commandlist = f.read()
            print repr(commandlist)
            print "command in data.."
            print str(commandlist)        
            con.send(str(commandlist))
            #f.read()
    f.close()
	
def read_out_user(data, con):
    f = open("getUserLog.txt", "r+")
    if "names" in data:
            userlist = f.read()
            print repr(userlist)
            print "command in data.."
            print str(userlist)        
            con.send(str(userlist))
            #f.read()
    f.close()

def names(data, con):
	con.send('Users\n-----\n' + '\n'.join(users))

def motd(data, con): 
	con.send(random.choice(quotes))

def send_all(m):
	for u in users:
		users[u].send(m)

#manage connection will only deal with parse input at the moment 
#the idea will be to try wrap this area in a while loop to try 
#and capture each command over and over
def manage_connection(conn, addr):
	global buffer, COUNT, game, rand
	with open("getIpAndPort.txt", "w+") as f:
		for x in range(50):
			f.write("This is line %d\r\n" % (x+1) +  repr(addr))
	username = conn.recv(1024)
	# Connection from IP:port username
	print 'Connection from {}:{} by {}'.format(addr[0], addr[1], username)
	send_all("* {} * has joined the chat ;)".format(username))
	users[username] = conn
	game = False

	try:
		while True:
			data = conn.recv(1024)
			COUNT += 1
			parse_input(data, conn)# Calling the parser, passing the connection
			with open("getTextLog.txt", "a+") as f:
					 f.write("This is the server record : %d\r\n" % (x+1) + repr(data))

			hash, _, text = data.split('-', 2)

			parse_hash(data,conn)

			if username in kicked:
				conn.close()
				del users[username]
				return

			if game:
				do_game(data, conn)
				continue

			if text.startswith('/kick ') and text[6:]:
				user = text[6:]
				if user in users:
					users[user].send('*you got banned homie*')
					kicked.append(user)
					print "Kicking user " + user
				else:
					conn.send("User does not exist. Kick yourself!")
			elif text == '/game':
				game = True
				rand = random.randint(0,101)
				conn.send("Guess a number between 0 and 100")
			elif text == '/motd':
				motd(data,conn)
			elif text == '/count':
				count_messages(data,conn)
			elif text == '/whoami':
				whoami(data,conn)
			elif text == '/quit':
				del users[username]
				send_all('* {} * has left the chat :('.format(username))
				leave_chat(data,conn)
			elif text == '/help':
				help(data, conn) #calling the read out from text file function
			elif text == '/names':
				names(data, conn)
			elif text == '/ping': 
			    ping_pong(data,conn)
			else:
				send_all('<{}> {}'.format(username, text))

				

			#previous flag, unmute to print server side message
			#print stPORT = 50010 if len(sys.argv) < 2 or not sys.argv[1].isdigit() or int(sys.argv[1]) not     in range(65536) else int(sys.argv[1])r(data) #prints it for the server
		   # buffer += repr(data)

			# conn.send("i'm a user: " + str(data))
	except KeyboardInterrupt:
		return
        
    #conn.close()
try:
	while True:
		s.listen(1)
		conn, addr = s.accept()
    # after we have listened and accepted a connection coming in,
    # we will then create a thread for that incoming connection.
    # this will prevent us from blocking the listening process
    # which would prevent further incoming connections
		t = threading.Thread(target=manage_connection, args = (conn,addr))
		t.daemon = True
		t.start()
except KeyboardInterrupt:
	sys.exit(1)


