# This is a submission for Sree Lalith Pullapantula and Abhishek Aryal
# In the included screenshots, one is to uiowa.edu and the other one is for dbs.com.
# uiowa.edu is located in the United States while dbs is located in Singapore. 

import socket
import time
import struct

def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0
    while count < countTo:
        thisVal = ord(string[count+1]) * 256 + ord(string[count])
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2
    if countTo < len(string):
        csum = csum + ord(string[len(string) - 1])
        csum = csum & 0xffffffff
    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def makePackets(flag, seq):
    CODE = 0
    CKSM = 0
    ID = 2
    SEQ = seq

    if flag == 0:
        TYPE = 8
    else:
        TYPE = 0

    initial = b''
    initial += TYPE.to_bytes(1, 'little')
    initial += CODE.to_bytes(1, 'little')
    initial += CKSM.to_bytes(2, 'little')
    initial += ID.to_bytes(2,'little')
    initial += SEQ.to_bytes(2,'little')

    CKSM = checksum(initial.decode('utf-8'))
    
    final = b''
    final += TYPE.to_bytes(1, 'little')
    final += CODE.to_bytes(1, 'little')
    final += socket.htons(CKSM).to_bytes(2, 'little')
    final += ID.to_bytes(2,'little')
    final += SEQ.to_bytes(2,'little')    

    return final


def ping(addr, seq):
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    req = makePackets(0, seq)
    res = makePackets(1, seq)

    s.connect((addr, 80))
    s.sendall(req)
    start = time.time()
    resp = s.recv(20571)
    while(time.time() - start < 1):
##        print('resp: ' , resp) # debugging. Remove later
##        print('resp[20:]: ', resp[20:]) # debugging. Remove later
##        print('sequence: ', resp[26]) # debugging. Remove later

        # check if the sequence # are the same
##        if resp[20:] == res[20:]:
##            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

        ip = socket.gethostbyname(addr)
        delta = time.time() - start
        delta = round(delta, 8)
        print('dest IP:', ip, '  seq #: ', seq, '  time diff: ', delta)
        break

if __name__ == '__main__':
    seq = 0
    addr = input("ping to: ")
    while True:
        time.sleep(1.5)
        ping(addr, seq)
        seq+=1
