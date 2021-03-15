from socket import *
import base64
import os
# msg = "\r\n I love computer networks!"
msg = "Hello world. This is the face when I finish the assignment"
endmsg = "\r\n.\r\n"
# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = "smtp.qq.com" # use QQ mail
# sender and receiver
fromaddr = "xxxxxxxxx@qq.com"
fromname = "Linxiao Wu"
toaddr = "xxxxxx@columbia.edu"
toname = "Linxiao Wu"
image_name = "cute.png"

# Authentication encoding using base64
username = base64.b64encode(fromaddr.encode()).decode()
password = base64.b64encode("xxxxxxxxxxxxxx".encode()).decode()

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
# use MIME version
# https://docs.microsoft.com/en-us/previous-versions/office/developer/exchange-server-2010/aa563375(v=exchg.140)
message = ""

subject = "Test email from coms 4119 socket programming by Linxiao!"
message += 'From: ' + fromname + ' <' + fromaddr + '>' + '\r\n'
message += 'To: ' + toname + ' <' + toaddr + '>' + '\r\n'
message += 'Subject: ' + subject + '\r\n'

message += 'MIME-Version: 1.0' + '\r\n'
message += 'Content-Type: multipart/mixed;' + ' boundary="frontier"'
# message += 'boundary="frontier"'
message += '\r\n'
message += 'This is a multipart message in MIME format.' + '\r\n'
message += '\r\n'

message += '--frontier' + '\r\n'
message += 'Content-Type: text/plain' + '\r\n'
message += '\r\n'
message += msg + '\r\n'
message += '\r\n'


attach_file_name = os.path.join("images", image_name)
attach_file = open(attach_file_name, 'rb')
image_byte = attach_file.read()
message += '--frontier' + '\r\n'
message += 'Content-Type: image/png;' + '\r\n'
message += 'Content-Disposition: attachment;' + ' filename="' + image_name + '"\r\n'
message += 'Content-Transfer-Encoding: base64' + '\r\n'
# print(message)
message += '\r\n'
message += (base64.b64encode(image_byte)).decode('ascii') + '\r\n'
message += '\r\n'
message += '--frontier' + '\r\n'

"""
Base64 is a group of binary-to-text encoding schemes that represent binary data
(more specifically, a sequence of 8-bit bytes) in an ASCII string format by
translating the data into a radix-64 representation
"""

clientSocket.sendall(message.encode())
# attach_file.close()
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