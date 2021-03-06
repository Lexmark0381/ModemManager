import socket, ping as ping, sys, time, os, signal
outlogfile =  "log/" + time.strftime("%d-%m-%Y") + ".out"
NOGPIOMODE = False
NOLOGMODE = False
modem_state = "on"
log = ""
HOST, PORT = '', 8888

def logToFile(S):
	open(outlogfile, 'a').close()
	separator = "--------------------------------------------------\n"
	f = open(outlogfile, 'a')
	f.write(separator)
	f.write(S)
	f.write('\n')
	f.close()

def help():
	print("--nogpio : run server without using gpio (prints GPIO ON or GPIO OFF)")
	print("--nolog : run server without logging")
	sys.exit()

if("--help" in sys.argv):
	help()

if("--nogpio" in sys.argv):
	print("NO GPIO MODE")
	NOGPIOMODE = True
else:
	import gpio as gpio
	print("GPIO imported")

if("--nolog" in sys.argv):
	print("NO LOG MODE")
	NOLOGMODE = True

if(not(os.path.exists('log'))):
	os.makedirs('log')
	print("LOG DIRECTORY CREATED")



listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(10)

print ('Serving HTTP on port ' + str(PORT))

while True:
	while True:
		client_connection, client_address = listen_socket.accept()
		request = client_connection.recv(1024).decode("utf-8") 
		request = request.split('\r\n')
		try:
			method = request[0].split()[0]
			dir = request[0].split()[1]
		except IndexError:
			if(not(NOLOGMODE)):
				logToFile("UNHANDLED REQUEST : " + str(request) + "\n\t" + str(client_address))
			print("Couldn't retreive method or directory")
			break;

		print(method, dir)
		logToFile("INCOMING REQUEST : \n\tMETHOD : " +method+ "\n\tDIRECTORY : " +dir)

		if(method == "GET"):
			if(dir == "/"):
				print("200 OK")
				http_response = "HTTP\/1.1 200 OK\nContent-Type:text/html\n\n"
				f = open("index.html", "r")
				text = f.read()
				f.close()
				http_response += text
				http_response += "\n"
				client_connection.sendall(http_response.encode())
				client_connection.close()

			elif(dir == "/img/grey.png"):
				print("GET "+ dir)
				print("200 OK")
				f = open("img/grey.png", "rb")
				client_connection.send("HTTP\/1.1 200 OK\nContent-Type : image/png\n\n".encode())
				client_connection.send(f.read())
				client_connection.close()
				f.close()

			elif(dir == "/img/greenn.png"):
				print("GET "+ dir)
				print("200 OK")
				f = open("img/greenn.png", "rb")
				client_connection.send("HTTP\/1.1 200 OK\nContent-Type : image/png\n\n".encode())
				client_connection.send(f.read())
				client_connection.close()
				f.close()

			elif(dir == "/img/red.png"):
				print("GET "+ dir)
				print("200 OK")
				f = open("img/red.png", "rb")
				client_connection.send("HTTP\/1.1 200 OK\nContent-Type : image/png\n\n".encode())
				client_connection.send(f.read())
				client_connection.close()
				f.close()

			elif(dir == "/js.js"):
				print("200 OK")
				http_response = "HTTP\/1.1 200 OK\nContent-Type : text/js\n\n"
				f = open("js.js", "r")
				text = f.read()
				f.close()
				http_response += text + "\n"
				client_connection.sendall(http_response.encode())
				client_connection.close()

			elif(dir == "/style.css"):
				print("200 OK")
				http_response = "HTTP\/1.1 200 OK\nContent-Type : text/css\n\n"
				f = open("style.css", "r")
				text = f.read()
				f.close()
				http_response += text
				http_response += "\n"
				client_connection.sendall(http_response.encode())
				client_connection.close()

			elif(dir == "/404.css"):
				print("200 OK")
				http_response = "HTTP\/1.1 200 OK\nContent-Type : text/css\n\n"
				f = open("404.css", "r")
				text = f.read()
				f.close()
				http_response += text
				http_response += "\n"
				client_connection.sendall(http_response.encode())
				client_connection.close()

				


			elif(dir == "/ping"):
				print("200 OK")
				http_response = "HTTP\/1.1 200 OK\n\n"
				delay = ping.verbose_ping("192.168.0.1", 1000, 4)
				# only for testing
				# delay = ping.verbose_ping("localhost", 250, 2)
				http_response += str(int(delay))
				client_connection.sendall(http_response.encode())
				client_connection.close()

			elif(dir == "/shortping"):
				print("200 OK")
				http_response = "HTTP\/1.1 200 OK\n\n"
				delay = ping.verbose_ping("192.168.0.1", 500, 1)
				http_response += str(int(delay))
				client_connection.sendall(http_response.encode())
				client_connection.close()

			elif(dir == "/log"):
				if(log == ""):
					print("204 NO CONTENT")
					http_response = "HTTP\/1.1 204 NO CONTENT\n\n"
					
				else:
					print("200 OK")
					http_response = "HTTP\/1.1 200 OK\n\n"
					http_response += log
					http_response += "\n"
				client_connection.sendall(http_response.encode())
				client_connection.close()

			elif(dir == "/state"):
				print("200 OK")
				http_response = "HTTP\/1.1 200 OK\n\n"
				http_response += modem_state
				http_response += "\n"
				client_connection.sendall(http_response.encode())
				client_connection.close()
			else:
				logToFile("404 : \n\tMETHOD : " + method+ "\n\tDIRECTORY : " + dir)
				print("404 NOT FOUND")
				http_response = "HTTP\/1.1 200 OK\n"
				http_response += "Content-Type : text/html\n\n"
				f = open('404.html', 'r')
				http_response += f.read() + '\n'
				client_connection.sendall(http_response.encode())
				f.close()
				client_connection.close()

		elif(method == "POST"):

			if(dir[0: 4] == "/log"):
				print("200 OK")
				log += dir.split("=")[1].replace("%20", " ").replace("%3C", "<").replace("%3E", ">")
				http_response = "HTTP\/1.1 200 OK\n\n"
				client_connection.sendall(http_response.encode())
				client_connection.close()

			elif(dir[0: 6] == "/state"):
				print(dir)
				try:
					params = dir.split("&")[1:]
				except:
					print("NO PARAMS")
					break
				for param in params:
					if(param.split("=")[0] == "state"):
						received_state = param.split("=")[1]
						print(received_state)
					if(param.split("=")[0] == "t"):
						t = param.split("=")[1]
						print(t)
				if((received_state == "on") or (received_state == "off") or (received_state == "reboot")):
					logToFile("STATE REQUEST:\n\tHOST : " + str(client_address) + "\n\tSTATE : " + received_state)
					if(received_state == "on"):
						if(NOGPIOMODE):
							print("GPIO ON")
						if(not NOGPIOMODE):
							print(NOGPIOMODE)
							gpio.on()
					elif (received_state == "off"):
						if(NOGPIOMODE):
							print("GPIO OFF")
						if(not NOGPIOMODE):
							print(NOGPIOMODE)
							gpio.off()
					else:
						if(NOGPIOMODE):
							print("GPIO REBOOT")
							try:
								print("Time : ", t)
							except:
								t = 3
								print("Default Time : ", t)
							print("MODEM ON AGAIN AFTER " + str(t) + " second(s).")
						if(not NOGPIOMODE):
							try:
								gpio.reboot(t)
							except:
								print("No reboot time given. 3 seconds of stop.")
								t = 3
								gpio.reboot(t)
					modem_state = received_state
					print("200 OK")
					http_response = "HTTP\/1.1 200 OK\n\n"
					client_connection.sendall(http_response.encode())
					client_connection.close()
				else:
					logToFile("400 : \n\tMETHOD : " + method + "\n\tDIRECTORY: " + dir)
					print("400 BAD REQUEST")
					http_response = "HTTP\/1.1 400 BadRequest\n\n"
					client_connection.sendall(http_response.encode())
					client_connection.close()
			else:
				logToFile("404 : \n\tMETHOD : " + method+ "\n\tDIRECTORY : " + dir)
				print("404 NOT FOUND")
				http_response = "HTTP\/1.1 200 OK\n"
				http_response += "Content-Type : text/html\n\n"
				f = open('404.html', 'r')
				http_response += f.read() + '\n'
				client_connection.sendall(http_response.encode())
				f.close()
				client_connection.close()

