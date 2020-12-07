import socket

# create a server


def CreateServer(host, port):
    Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Server.bind((host, port))
    Server.listen(3)
    return Server

# read the request from client


def ReadRequest(Client):
    re = ""
    Client.settimeout(1)  # set time out 1 second
    try:
        re = Client.recv(1024).decode()
        while (re):
            re = re + Client.recv(1024).decode()
            # use while cause we wanna read all of the data, the data may be bigger than 1024
    except socket.timeout:  # after 1 second of no activity- time out
        if not re:
            print("Didn't receive data! [Timeout]")
    finally:
        return re


# Read http request
def ReadHTTPRequest(Server):
    re = ""
    while (re == ""):
        Client, address = Server.accept()
        print("Client: ", address, " connected with server")
        re = ReadRequest(Client)
    return Client, re


def SendFileIndex(Client):
    f = open("index.html", "rb")
    L = f.read()
    header = """HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

""" % len(L)
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
    Client.send(bytes(header, 'utf-8'))
    Server.close()

# 4. Send HTTP Response  + 5. Close Server


def MoveHomePage(Server, Client, Request):
    if "GET / index.html HTTP/1.1" in Request:
        SendFileIndex(Client)
        Server.close()
        return True
    if "GET / HTTP/1.1" in Request:
        # Move Index.html
        MovePageIndex(Client)
        # Tra ve file index.html cho client
        Server = CreateServer("localhost", 8080)
        Client, Request = ReadHTTPRequest(Server)
        print("------------------HTTP request: ")
        print(Request)
        MoveHomePage(Server, Client, Request)
        return True


def checkLogin(request):
    if "POST / HTTP/1.1" not in Request:
        return False
    if "Username=admin&Password=admin" in Request:
        return True
    else:
        return False


def Move404(Server, Client):
    header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8080/404.html

"""
    print("HTTP respone: ")
    print(header)
    Client.send(bytes(header, "utf-8"))
    Server.close()


def SendFile404(Client):
    f = open("404.html", "rb")
    L = f.read()
    header = """HTTP/1.1 404 Not Found
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d
""" % len(L)
    print("HTTP respone file 404.html: ")
    print(header)
    header += L.decode()
    Client.send(bytes(header, 'utf-8'))


def Send404(Server, Client):
   # Create Server Socket
    Server = CreateServer("localhost", 8080)
    # Client connect Server + 3. Read HTTP Request
    Client, Request = ReadHTTPRequest(Server)
    print("----------------HTTP request: ")
    print(Request)
    if "GET /404.html HTTP/1.1" in Request:
        SendFile404(Client)
    Server.close()


def MoveInfo(Server, Client):
    header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8080/info.html
"""
    print("HTTP respone: ")
    print(header)
    Client.send(bytes(header, "utf-8"))
    Server.close()


def SendFileInfo(Client):
    f = open("info.html", "rb")
    L = f.read()
    header = """HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d
""" % len(L)
    print("-----------------HTTP respone  Info.html: ")
    print(header)
    header += L.decode()
    Client.send(bytes(header, 'utf-8'))


def SendImg(Client, NameImg):
    with open(NameImg, 'rb') as f:
        L = f.read()
        header = """HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d
""" % len(L)
        print("-----------------HTTP respone: ")
        print(header)
        header = bytes(header, 'utf-8') + L
        Client.send(header)


def SendInfo(Server, Client):
    Server = CreateServer("localhost", 8080)
    Client, Request = ReadHTTPRequest(Server)
    print("HTTP Request: ")
    print(Request)
    if "GET /info.html HTTP/1.1" in Request:
        SendFileInfo(Client)
    Server.close()
    # image 1
    Server = CreateServer("localhost", 8080)
    Client, Request = ReadHTTPRequest(Server)
    print("HTTP Request: ")
    print(Request)
    if "GET /pic1.jpg HTTP/1.1" in Request:
        SendImg(Client, "pic1.jpg")
    if "GET /pic2.jpg HTTP/1.1" in Request:
        SendImg(Client, "pic2.jpg")
    # image 2
    Client, Request = ReadHTTPRequest(Server)
    print("HTTP Request: ")
    print(Request)
    if "GET /pic1.jpg HTTP/1.1" in Request:
        SendImg(Client, "pic1.jpg")
    if "GET /pic2.jpg HTTP/1.1" in Request:
        SendImg(Client, "pic2.jpg")
    Server.close()


# main function
if __name__ == "__main__":
    while True:
        print("Part 1: return homepage when access")
        # Create Server Socket
        Server = CreateServer("localhost", 8080)
        # Client connect Server + 3. Read HTTP Request
        Client, Request = ReadHTTPRequest(Server)
        print("----------------HTTP request: ")
        print(Request)
        # Send HTTP Rea + Close Sever
        MoveHomePage(Server, Client, Request)
        print("Part 2: login")
        # Create Server Socket
        Server = CreateServer("localhost", 8080)
        # Client connect Server + 3. Read HTTP Request
        Client, Request = ReadHTTPRequest(Server)
        print("----------------HTTP request: ")
        print(Request)
        # Send HTTP Rea + Close Sever
        if checkLogin(Request) == True:
            MoveInfo(Server, Client)
            SendInfo(Server, Client)
        else:
            Move404(Server, Client)
            Send404(Server, Client)
