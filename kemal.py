# import socket module
from socket import *
import ssl

"""
Prepare a server socket
"""
sock = socket(AF_INET, SOCK_STREAM)

# serverSocket = ssl.wrap_socket(sock, certfile='server.crt', keyfile='server.key', ssl_version=ssl.PROTOCOL_TLSv1_2)
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('server.crt', keyfile='server.key', password='1150377')
context.set_ciphers('ALL:!DH:!kDH:!EDH:!ADH:!ECDH')     # 'ALL:!DH:!ECDH' is sufficient
serverSocket = context.wrap_socket(sock)

# Your code
HOST, PORT = '', 3340
# AF_INET = Address Family
serverSocket.bind((HOST, PORT))
serverSocket.listen(1)
while True:
    # Establish the connection
    print 'Ready to serve...'
    connectionSocket, addr = serverSocket.accept()  # Your code

    try:
        message = connectionSocket.recv(4096)       # Your code
        reqArray = message.split()
        filename = reqArray[1]
        f = open(filename[1:], 'rb')
        outputdata = f.read()                       # Your code
        """
        Send one HTTP header line into socket
        """
        # Your code
        connectionSocket.send("HTTP/1.0 200 OK\r\n")
        # connectionSocket.send("HTTP/1.1 200 OK\nContent-Type: application/octet-stream\n\n")

        # "HTTP/1.1 200 OK\nContent-Type: text/html\n\n"
        print "Serving page " + filename
        # for i in range(1, len(reqArray)):
        #     print str(i) + ": " + str(reqArray[i])

        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i])
            #print outputdata[i]
        connectionSocket.send("\r\n")
        connectionSocket.send("\r\n")
        # Close the client connection socket

        connectionSocket.close()
        f.close()

    except IOError:
        """
        Send response message for file not found
        """
        # Your code
        message = ['HTTP/1.0 404 Not Found\n\n404 Not Found']
        for i in range(0, len(message)):
            connectionSocket.send(message[i])

    """
    Close client socket 
    """
    # Your code
    connectionSocket.close()

serverSocket.close() 
