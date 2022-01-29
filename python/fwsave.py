import sys

fwformat = str("Intel HEX (*.hex)")

numOfBytes = 16

def fwsave(fwfilename,hexlist):
    fwfile = open(fwfilename,'w')
    address = 0
    checksum = 0
    for i,x in enumerate(hexlist):
        if hexlist[i] < 0:
            hexlist[i] += 256
    for i in range(0,len(hexlist),numOfBytes):
        if(i+numOfBytes > len(hexlist)):
            hexlist.extend([ 0 for i in range(len(hexlist),i+numOfBytes) ])
        checksum = 1 + ~((sum(hexlist[i:i+numOfBytes]) + numOfBytes + (address >> 8) + (address & 0x00FF)) & 0xFF) & 0xFF
        line = ':' + format(numOfBytes,'x').upper() + '{:04x}'.format(address).upper() + "00" + "".join('{:02x}'.format(x) for x in hexlist[i:i+numOfBytes]).upper() + '{:02x}'.format(checksum).upper() + '\n'
        fwfile.write(line)
        address += numOfBytes
        #print line
    return
