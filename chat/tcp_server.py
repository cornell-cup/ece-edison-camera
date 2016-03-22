# TCP Server with Edison
import socket, select

def server_details(sock):
    # Send details about this server to the appropriate socket 
    server_name = 'jEdison'
    server_version = 1
    try :
        msg = '\r' + 'Server name: ' + server_name + '\n'
        msg += 'Server version: ' + str(server_version) +'\n' 
        sock.sendall(msg) 
        #sock.sendall('\r' + 'Server name: ' + server_name + '\n' + 'Server version: ' + str(server_version))
        #sock.send('Server version: ' + str(server_version))# + '/r/n')
    except:
        # broken socket connection 
        sock.close()
        CONNECTION_LIST.remove(sock)

if __name__ == "__main__":
    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 4096
    PORT = 6798

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", PORT))
    server_socket.listen(10)

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
    
    print "Chat server started on port " + str(PORT)

    while True:
        # Get the list of sockets ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])

        for sock in read_sockets:
            # New connection
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr

            # some incoming message from a client
            else: 
                try:
                    data = sock.recv(RECV_BUFFER)
                    if 'server data' in data:
                        server_details(sock)
                    else: 
                        sock.send('This is what you sent: ' + data)
                        #server_details(sock)
                except: 
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue 
    server_socket.close()
