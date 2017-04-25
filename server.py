import socket, ping as ping, gpio as gpio
log = ""
HOST, PORT = '', 8888

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(10)

print ('Serving HTTP on port ' + str(PORT))
modem_state = "on"

while True:
	client_connection, client_address = listen_socket.accept()
	print(client_connection, client_address)
	request = client_connection.recv(1024).decode("utf-8") 
	request = request.split('\r\n')
	method = request[0].split()[0]
	dir = request[0].split()[1]
	print(method, dir)
	if(method == "GET"):
		if(dir == "/"):
			print("200 OK")
			http_response = "HTTP\/1.1 200 OK\n\n"
			f = open("index.html", "r")
			text = f.read()
			f.close()
			http_response += text
			http_response += "\n"
			client_connection.sendall(http_response.encode())
			client_connection.close()





		# elif(dir == "/img/grey.png"):
		# 	my_bytes = bytearray()
		# 	print("200 OK")
		# 	f = open("img/grey.png", "rb")
		# 	my_bytes.append(f.read())
		# 	print(my_bytes)
		# 	f.close()
		# 	client_connection.send(my_bytes)
		# 	client_connection.close()

		# elif(dir == "/img/red.png"):
		# 	my_bytes = bytearray()
		# 	print("200 OK")
		# 	f = open("img/red.png", "rb")
		# 	my_bytes.append(f.read())
		# 	print(my_bytes)
		# 	f.close()
		# 	client_connection.send(my_bytes)
		# 	client_connection.close()

		# elif(dir == "/img/green.png"):
		# 	my_bytes = bytearray()
		# 	print("200 OK")
		# 	f = open("img/green.png", "rb")
		# 	my_bytes.append(f.read())
		# 	print(my_bytes)
		# 	f.close()
		# 	client_connection.send(my_bytes)
		# 	client_connection.close()





		elif(dir == "/js.js"):
			print("200 OK")
			http_response = "HTTP\/1.1 200 OK\n\n"
			f = open("js.js", "r")
			text = f.read()
			f.close()
			http_response += text + "\n"
			client_connection.sendall(http_response.encode())
			client_connection.close()

		elif(dir == "/style.css"):
			print("200 OK")
			http_response = "HTTP\/1.1 200 OK\n\n"
			f = open("style.css", "r")
			text = f.read()
			f.close()
			http_response += text
			http_response += "\n"
			client_connection.sendall(http_response.encode())
			client_connection.close()

		elif(dir == "/ping"):
			print("200 OK")
			http_response = "HTTP\/1.1 200 OK\n\n"
			delay = ping.verbose_ping("192.168.0.1", 250, 2)
			# only for testing
			# delay = ping.verbose_ping("localhost", 250, 2)
			http_response += str(int(delay))
			client_connection.sendall(http_response.encode())
			client_connection.close()

		elif(dir == "/log"):
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
			print("404 NOT FOUND")
			http_response = "HTTP\/1.1 404 NotFound\n\n"
			client_connection.sendall(http_response.encode())
			client_connection.close()

	elif(method == "POST"):

		if(dir[0: 4] == "/log"):
			print("200 OK")
			log += dir.split("=")[1].replace("%20", " ").replace("%3C", "<").replace("%3E", ">")
			http_response = "HTTP\/1.1 200 OK\n\n"
			client_connection.sendall(http_response.encode())
			client_connection.close()
		elif(dir[0: 6] == "/state"):
			received_state = dir.split("=")[1]
			print(received_state)
			if((received_state == "on") or (received_state == "off") or (received_state == "reboot")):
				if(received_state == "on"):
					gpio.on()
				elif (received_state == "off"):
					gpio.off()
				else:
					try:
						t = int(dir.split("=")[2])
					except:
						print("No timeout given, setting to 3")
						t = 3
					gpio.reboot(t)
				modem_state = received_state
				print("200 OK")

				http_response = "HTTP\/1.1 200 OK\n\n"
				client_connection.sendall(http_response.encode())
				client_connection.close()
			else:
				print("400 BAD REQUEST")

				http_response = "HTTP\/1.1 400 BadRequest\n\n"
				client_connection.sendall(http_response.encode())
				client_connection.close()
		else:
			print("404 NOT FOUND")
			http_response = "HTTP\/1.1 404 NotFound\n\n"
			client_connection.sendall(http_response.encode())
			client_connection.close()
