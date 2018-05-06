import binascii

# Parsing
def Parser():
    with open('Test.txt', 'r') as f:
        content = f.readlines()

        content = [x.strip() for x in content]

        #print content

        i = 0
        for c in content:
            if (c == 'DATA SEGMENT'):
                break
            intC = int(c, 16)
            content[i] = bin(intC)[2:].zfill(32)

            i += 1

        #print content

        return content

def Decoder(content):

    RtypOps = {
        '0':'sll', '2':'srl','3':'sra','4':'sllv','6':'srlv','7':'srav',
        '8':'jr','9':'jalr',
        '10':'movz','11':'movn','12':'syscall',
        '16':'mfhi','17':'mthi','18':'mflo','19':'mtlo',
        '24':'mult', '25':'multu', '26':'div','27':'divu','32':'add','33':'addu','34':'sub','35':'subu',
        '36':'and','37':'or','38':'xor','39':'nor',
        '42':'slt','43':'sltu'
    }

    for c in content:
        if c == 'DATA SEGMENT':
            break
        #R-type
        #print c[0:5]
        if (c[0:5] == '00000'):
            temp = [0]*6
            temp[0] = c[0:6] #6 bit op code
            temp[1] = c[6:11] #5 bit rs
            temp[2] = c[11:16] #5 bit rt
            temp[3] = c[16:21] #5 bit rd
            temp[4] = c[21:26] #5 bit shamt
            temp[5] = c[26:32] #6 bit funct

            textCode = [0]*4
            textCode[0] = RtypOps[str(int(temp[5],2))]
            print textCode







Decoder(Parser())