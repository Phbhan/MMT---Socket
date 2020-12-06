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
	Client.settimeout(1) # set time out 1 second
	try:
		re = Client.recv(1024).decode()
		while (re):
			re = re + Client.recv(1024).decode()
			# use while cause we wnanna read all of the data, the data may be bigger than 1024
	except socket.timeout: # after 1 second of no activity- time out
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


def SendFileIndex(Client): 
	f = open ("index.html", "rb")
	L = f.read()
	header ="""HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

"""%len(L)
	print("-----------------HTTP respone  Index.html: ")
	print(header)
	header += L.decode()
	Client.send(bytes(header, 'utf-8'))

def MovePageIndex(Client):
	header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8080/index.html

"""
	print("---------------HTTP respone move Index.html: ")
	print(header)
	Client.send(bytes(header,'utf-8'))

#4. Send HTTP Response  + 5. Close Server
def MoveHomePage(Server, Client, Request):
	if "GET /index.html HTTP/1.1" in Request: 
		SendFileIndex(Client)
		Server.close()
		return True
	if "GET / HTTP/1.1" in Request:
		#Move Index.html 
		MovePageIndex(Client)
		Server.close()
		#Tra ve file index.html cho client
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
		# Create Server Socket 
		Server = CreateServer("localhost",8080)
		# Client connect Server + 3. Read HTTP Request
		Client, Request = ReadHTTPRequest(Server)
		print("----------------HTTP requset: " )
		print(Request)
		# Send HTTP Rea + Close Sever
		MoveHomePage(Server, Client, Request)
		
	
	#note: chua chay duoc ham doc file index.html

