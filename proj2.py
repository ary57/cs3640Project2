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

def makePackets(flag):
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
    final += CKSM.to_bytes(2, 'little')
    final += ID.to_bytes(2,'little')
    final += SEQ.to_bytes(2,'little')    

    return final


def ping(addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    req = makePackets(0)
    res = makePackets(1)

    s.connect((addr, 80))
    s.sendall(req)
    start = time.time()
    resp = s.recv(20571)
    while(time.time() - start < 1):
        if resp[20:] == res:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        print(time.time() - start)
        break

if __name__ == '__main__':
    while True:
        ping('www.uiowa.edu')
