import socket

#create a server
def CreateServer(host, port): 
	Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	Server.bind((host,port))
	Server.listen(3)
	return Server

#read the request from client
def ReadRequest(Client):
	re = ""
	Client.settimeout(1)
	try:
		re = Client.recv(1024).decode()
		while (re):
			re = re + Client.recv(1024).decode()
	except socket.timeout:
		if not re:
			print("Didn't receive data! [Timeout]")
	finally:
		return re


#Read http request
def ReadHTTPRequest(Server): 
	re = ""
	while (re == ""):
		Client, address = Server.accept()
		print("Client: ", address," connected with server")
		re = ReadRequest(Client)
	return Client, re


# send file index to client
def SendFileIndex(Client): 
	f = open ("index.html", "rb")
	str = f.read()
	header ="""HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

"""%len(str)
	print("-----------------HTTP respone  Index.html: ")
	print(header)
	header += str.decode()
	Client.send(bytes(header, 'utf-8'))

def MovePageIndex(Client):
	header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8080/index.html

"""
	print("---------------HTTP respone move Index.html: ")
	print(header)
	Client.send(bytes(header,'utf-8'))


# homaepage when access
def MoveHomePage(Server, Client, Request):
	if "GET /index.html HTTP/1.1" in Request: 
		SendFileIndex(Client)
		Server.close()
		return True

	if "GET / HTTP/1.1" in Request:

		#Move Index.html 
		MovePageIndex(Client)
		Server.close()

		#return index.html to client
		Server = CreateServer("localhost", 8080)
		Client, Request = ReadHTTPRequest(Server)
		print("------------------HTTP request: ")
		print(Request)
		MoveHomePage(Server, Client, Request)
		return True

#main function
if __name__ == "__main__":
	while True:
		print("Part 1: return homepage when access")
		Server = CreateServer("localhost",8080)
		Client, Request = ReadHTTPRequest(Server)
		print("----------------HTTP requset: " )
		print(Request)
		MoveHomePage(Server, Client, Request)

		print("Part 2: login - post username and password to server")
		Server = CreateServer("localhost",8080)
		Client, Request = ReadHTTPRequest(Server)
		print("----------------HTTP requset: " )
		print(Request)

		if CheckPass(Request) == True: 
			MoveInfo(Server, Client)
			SendInfo(Server, Client)
		else: 
			Move404(Server, Client)
			Send404(Server, Client)
		
	

