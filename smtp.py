from socket import *
import base64
# msg = "\r\n I love computer networks!"
msg = "\r\n Good Morning from Socket Programming!"
endmsg = "\r\n.\r\n"
# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = "smtp.qq.com" # use QQ mail
# sender and receiver
fromaddr = "xxxxxxxxx@qq.com"
toaddr = "xxxxxx@columbia.edu"

# Authentication encoding using base64
username = base64.b64encode(fromaddr.encode()).decode()
password = base64.b64encode("xxxxxxxxxxxxx".encode()).decode()

# Create socket called clientSocket and establish a TCP connection with mailserver

#Fill in start
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, 25))
#Fill in end

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print("hello command receipt:", recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Before sending, need to end the Auth
clientSocket.sendall('AUTH LOGIN\r\n'.encode())
recv = clientSocket.recv(1024).decode()
print("Auth login command:", recv)
if recv[:3] != '334':
    print('334 reply not received from server')

clientSocket.sendall((username + '\r\n').encode())
recv = clientSocket.recv(1024).decode()
print("username informaiton:", recv)
if recv[:3] != '334':
    print('334 reply not received from server')

clientSocket.sendall((password + '\r\n').encode())
recv = clientSocket.recv(1024).decode()
print("password information:", recv)
if recv[:3] != '235':
    # for QQ, need to configure SMTP service first
    # https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256
    # 235 means authentication succeeds
    print('235 reply not received from server')

# Send MAIL FROM command and print server response.
# Fill in start
clientSocket.sendall(('MAIL FROM: <' + fromaddr + '>\r\n').encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server')
# Fill in end


# Send RCPT TO command and print server response.
# Fill in start
clientSocket.sendall(('RCPT TO: <' + toaddr + '>\r\n').encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server')
# Fill in end


# Send DATA command and print server response.
# Fill in start
clientSocket.send('DATA\r\n'.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '354':
    # 354 start mail input
    print('354 reply not received from server')
# Fill in end


# Send message data.
# Fill in start
subject = "Test email from coms 4119 socket programming by Linxiao!"
contenttype = "text/plain"
message = 'from:' + fromaddr + '\r\n'
message += 'to:' + toaddr + '\r\n'
message += 'subject:' + subject + '\r\n'
message += 'Content-Type:' + contenttype + '\t\n'
message += msg  # '\r\n' + msg2
clientSocket.sendall(message.encode())
# Fill in end


# Message ends with a single period.
# Fill in start
clientSocket.sendall(endmsg.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server')
# Fill in end


# Send QUIT command and get server response.
# Fill in start
clientSocket.sendall('QUIT\r\n'.encode())
# Fill in end

# Close connection
clientSocket.close()