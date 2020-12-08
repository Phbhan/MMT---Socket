import socket
import os
# 1. Create a server


def CreateServer(host, port):
    Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Server.bind((host, port))
    Server.listen(1)
    return Server

# 3. Read the request from client


def ReadRequest(Client):
    re = ""
    Client.settimeout(1)  # set time out 1 second
    try:
        re = Client.recv(1024).decode()
        while (re):
            re = re + Client.recv(1024).decode()
            # use while cause we wnanna read all of the data, the data may be bigger than 1024
    except socket.timeout:  # after 1 second of no activity- time out
        if not re:
            print("Didn't receive data! [Timeout]")
    finally:
        return re

# 2. Client connect Server + 3. Read HTTP Request


def ReadHTTPRequest(Server):
    re = ""
    while (re == ""):
        Client, address = Server.accept()
        print("Client: ", address, " connected with server")
        re = ReadRequest(Client)
    return Client, re

# I/ 4 + 5. Send page index.html


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

# I/ 4 + 5. Move the indirect


def MovePageIndex(Client):
    header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8080/index.html

"""
    print("---------------HTTP respone move Index.html: ")
    print(header)
    Client.send(bytes(header, 'utf-8'))

# I/ 4. Send HTTP Response  + 5. Close Server


def MoveHomePage(Server, Client, Request):
    if "GET /index.html HTTP/1.1" in Request:
        SendFileIndex(Client)
        Server.close()
        return True
    else:
        if "GET / HTTP/1.1" in Request:
            # Move Index.html
            MovePageIndex(Client)
            Server.close()
            # Tra ve file index.html cho client
            Server = CreateServer("localhost", 8080)
            Client, Request = ReadHTTPRequest(Server)
            print("------------------HTTP request: ")
            print(Request)
            MoveHomePage(Server, Client, Request)
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


def SendFile404(Client):
    f = open("404.html", "rb")
    L = f.read()
    header = """HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

""" % len(L)
    print("-----------------HTTP respone  404.html: ")
    print(header)
    header += L.decode()
    Client.send(bytes(header, 'utf-8'))

# II/ 4. Send HTTP Response  + 5. Close Server


def Move404Page(Server, Client, Request):
    Move404(Server, Client)
    Server.close()
    # 1. Create Server Socket
    Server = CreateServer("localhost", 8080)
    # 2. Client connect Server + 3. Read HTTP Request
    Client, Request = ReadHTTPRequest(Server)
    print("----------------HTTP requset: ")
    print(Request)
    SendFile404(Client)
    Server.close()

# Check username and password


def MoveInfo(Server, Client):
    header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8080/info.html

"""
    print("HTTP respone: ")
    print(header)
    Client.send(bytes(header, "utf-8"))


def SendFileInfo(Client):
    f = open("info.html", "rb")
    L = f.read()
    header = """HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

""" % len(L)
    print("-----------------HTTP respone  infor.html: ")
    print(header)
    header += L.decode()
    Client.send(bytes(header, 'utf-8'))


def SendImg(Client, NameImg):
    f = open(NameImg, "rb")
    L = f.read()
    header = f"HTTP/1.1 200 OK\nContent-Type: image/jpeg\nContent-Length: {len(L)}\r\n\r\n" 
    print("-----------------HTTP respone: ")
    print(header)
    header = header.encode() + L + "\r\n\r\n".encode()
    Client.sendall(header)

# II/ 4. Send HTTP Response  + 5. Close Server


def MoveInfoPage(Server, Client, Request):
    MoveInfo(Server, Client)
    Server.close()
    # 1. Create Server Socket
    Server = CreateServer("localhost", 8080)
    # 2. Client connect Server + 3. Read HTTP Request
    Client, Request = ReadHTTPRequest(Server)
    print("----------------HTTP requset: ")
    print(Request)
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

def checkLogin(Request):
    if "Username=admin&Password=admin" in Request:
        print("Right account, move to info.html")
        return True
    else:
        return False

  


# file.html
    
def MoveFile(Server, Client):
    header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8080/file.html

"""
    print("HTTP respone: ")
    print(header)
    Client.send(bytes(header, "utf-8"))

    
def SendFileDownload(Client, NameDownload):
    f = open(NameDownload, "rb")
    L = f.read()
    header = """HTTP/1.1 200 OK 
Content-Type: text/plain
Transfer-Encoding: chunked
5\r\n
Media\r\n
8\r\n
Services\r\n
4\r\n
Live\r\n
0\r\n
\r\n

""" % len(L)
    print("-----------------HTTP respone  File.html: ")
    print(header)
    header = header.encode() + L + "\r\n\r\n".encode()
    Client.sendall(header)

def SendFileFile(Client):
    f = open("file.html", "rb")
    L = f.read()
    header = """HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

""" % len(L)
    print("-----------------HTTP respone  file.html: ")
    print(header)
    header += L.decode()
    Client.send(bytes(header, 'utf-8'))

def MoveFilePage(Server, Client, Request):
    MoveFile(Server, Client)
    Server.close()
    # 1. Create Server Socket
    Server = CreateServer("localhost", 8080)
    # 2. Client connect Server + 3. Read HTTP Request
    Client, Request = ReadHTTPRequest(Server)
    print("----------------HTTP requset: ")
    print(Request)
    SendFileFile(Client)
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
    Server.close()


# Main function
if __name__ == "__main__":
    while True:
        print("Part 1: return homepage when access")
        # 1. Create Server Socket
        Server = CreateServer("localhost", 8080)
        # 2. Client connect Server + 3. Read HTTP Request
        Client, Request = ReadHTTPRequest(Server)
        print("----------------HTTP requset: ")
        print(Request)
        # 4. Send HTTP Rea + 5. Close Sever
        if MoveHomePage(Server, Client, Request) == True:
            print("Part 2: login")
            # 1. Create Server Socket
            Server = CreateServer("localhost", 8080)
            # 2. Client connect Server + 3. Read HTTP Request
            Client, Request = ReadHTTPRequest(Server)
            print("----------------HTTP requset: ")
            print(Request)
            # 4. Send HTTP Rea + 5. Close Sever
            if checkLogin(Request) == True:
                MoveInfoPage(Server, Client, Request)
            else:
                Move404Page(Server, Client, Request)
        else:
            MoveFilePage(Server, Client, Request)
            Server.close()
