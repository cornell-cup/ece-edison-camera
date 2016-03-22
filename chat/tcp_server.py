# TCP Server with Edison
import socket
import select
import thread 
import mraa

def server_details(sock):
    # Send details about this server to the appropriate socket 
    server_name = 'Edison - Judy'
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

def read_pin(pin_num):
    # returns a value from the pin
    x = mraa.Gpio(pin_num)
    x.dir(mraa.DIR_IN)
    return x.read()


def write_pin(pin_num, val):
    # writes value to pin
    x = mraa.Gpio(pin_num)
    x.dir(mraa.DIR_OUT)
    x.write(val)
    print 'Value written to pin: %s' % str(pin_num)



# CURRENTLY UNUSED BECAUSE IT DOES NOT FIT WITH THIS CODE
def client_thread(sock):
    # Send message to connected client
    sock.send('Connected to the server. Type something and hit enter\n')

    # infinite loop so thread does not end
    while True:
        data = sock.recv(4096)
        msg = 'You sent: ' + data
        if not data:
            break
        sock.sendall(msg)
    sock.close()

if __name__ == "__main__":
    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 4096
    PORT = 6789

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
                    if 'read_pin' in data:
                        aRead = read_pin(11)
                        sock.send('Pin value ' + str(aRead))
                    else: 
                        sock.send('This is what you sent: ' + data)
                        #server_details(sock)
                except: 
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue 
    server_socket.close()
