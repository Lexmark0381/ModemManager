import socket, ping as ping
log = ""
HOST, PORT = '', 8888

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(10)

print ('Serving HTTP on port ' + str(PORT))
modem_state = ""

while True:
	client_connection, client_address = listen_socket.accept()
	request = client_connection.recv(1024).decode("utf-8") 
	request = request.split('\r\n')
	# print(request)
	method = request[0].split()[0]
	dir = request[0].split()[1]
	print(method, dir)
	# print(request)
	if(method == "GET"):

		if(dir == "/"):
			http_response = "HTTP\/1.1 200 OK\n\n"
			f = open("index.html", "r")
			text = f.read()
			f.close()
			http_response += text
			http_response += "\n"
			client_connection.sendall(http_response.encode())
			client_connection.close()

		elif(dir == "/js.js"):
			http_response = "HTTP\/1.1 200 OK\n\n"
			f = open("js.js", "r")
			text = f.read()
			f.close()
			http_response += text + "\n"
			client_connection.sendall(http_response.encode())
			client_connection.close()


		elif(dir == "/style.css"):
			http_response = "HTTP\/1.1 200 OK\n\n"
			f = open("style.css", "r")
			text = f.read()
			f.close()
			http_response += text
			http_response += "\n"
			client_connection.sendall(http_response.encode())
			client_connection.close()

		elif(dir == "/ping"):
			http_response = "HTTP\/1.1 200 OK\n\n"
			delay = ping.verbose_ping("192.168.0.1", 250, 2)
			http_response += str(int(delay))
			# http_response += "\n"
			client_connection.sendall(http_response.encode())
			client_connection.close()

		elif(dir == "/log"):
			http_response = "HTTP\/1.1 200 OK\n\n"
			http_response += log
			http_response += "\n"
			client_connection.sendall(http_response.encode())
			client_connection.close()
		else:
			print(404)
			http_response = "HTTP\/1.1 404 NotFound\n\n"
			client_connection.sendall(http_response.encode())
			client_connection.close()

	elif(method == "POST"):

		if(dir[0: 4] == "/log"):
			log += dir.split("=")[1].replace("%20", " ").replace("%3C", "<").replace("%3E", ">")
			http_response = "HTTP\/1.1 200 OK\n\n"
			client_connection.sendall(http_response.encode())
			client_connection.close()

