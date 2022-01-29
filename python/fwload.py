import sys

fwformat = str("Bytestream/Intel HEX (*.hex)")

class HEXFileError(object):
    BEGRECERR = -1
    RECTYPEERR = -2
    CSUMERR = -3
    ADDREXNSUP = -4

class HEXRecordType(object):
    DATA = 0
    EOF = 1
    ADDRSEG = 2
    ADDREX = 4

def symblistpair(symblist): 
    return [symblist[i] + symblist[i+1] for i in xrange(0,len(symblist),2) if i < len(symblist)-1]

def fwload(fwfilename):
    offset = 0
    hexlist = []
    fwfile = open(fwfilename)
    if(fwfilename[-4:] == ".hex"):
        for fwrecnum,fwrec in enumerate(fwfile):
            if(fwrec[0] == ":"): #this is Intel HEX Format
                fwrecstr = list(fwrec)
                fwrecstr.pop(0)
                fwrecstr = symblistpair(fwrecstr)
                fwrecint = [int(irec,16) for irec in fwrecstr]
                fwchecksum = fwrecint.pop()
                checksum = 1 + ~(sum(fwrecint) & 0xFF) & 0xFF
                if(checksum == fwchecksum):
                    if(fwrecint[3] == HEXRecordType.DATA):
                        for i in range(1,fwrecint[0]+1):
                            hexlist.append(fwrecint[3+i])
                    elif(fwrecint[3] == HEXRecordType.EOF):
                        fwfile.close()
                        return hexlist
                    elif(fwrecint[3] == HEXRecordType.ADDRSEG):
                        offset = int(fwrecstr[4] + fwrecstr[5],16)
                    elif(fwrecint[3] == HEXRecordType.ADDREX):
                        fwfile.close()
                        return [ HEXFileError.ADDREXNSUP, fwrecnum ]
                    else:
                        fwfile.close()
                        return [ HEXFileError.RECTYPEERR, fwrecnum ]
                else:
                    fwfile.close()
                    return [ HEXFileError.CSUMERR, fwrecnum ]                     
            else:               #this is ByteStream HEX Format
                hexlist = symblistpair(fwrec)
                hexlist = [int(i,16) for i in hexlist]
                fwfile.close()
                return hexlist
