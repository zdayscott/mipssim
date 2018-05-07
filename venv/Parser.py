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

    RegCodes = {
        '0':'$zero','1':'$at',
        '2':'$v0','3':'$v1',
        '4':'$a0','5':'$a1','6':'$a2','7':'$a3',
        '8':'$t0','9':'$t1','10':'$t2','11':'$t3','12':'$t4','13':'$t5','14':'$t6','15':'$t6',
        '16':'$s0','17':'$s1','18':'$s2','19':'$s3','20':'$s4','21':'$s5','22':'$s6','23':'$s7',
        '24':'$t8','25':'$t9',
        '26':'$k0','27':'$k1',
        '28':'$gp','29':'$sp','30':'$fp','31':'$ra'
    }

    RtypOps = {
        '0':'sll', '2':'srl','3':'sra','4':'sllv','6':'srlv','7':'srav',
        '8':'jr','9':'jalr',
        '10':'movz','11':'movn','12':'syscall',
        '16':'mfhi','17':'mthi','18':'mflo','19':'mtlo',
        '24':'mult', '25':'multu', '26':'div','27':'divu','32':'add','33':'addu','34':'sub','35':'subu',
        '36':'and','37':'or','38':'xor','39':'nor',
        '42':'slt','43':'sltu'
    }

    ItypOps = {
        '4':'beq','5':'bne','6':'blez','7':'bgtz',
        '8':'addi','9':'addiu',
        '10':'slti','11':'sltiu',
        '12':'andi','13':'ori','14':'xori',
        '15':'lui','32':'lb','33':'lh','35':'lw','36':'lbu','37':'lhu',
        '40':'sb','41':'sh','43':'sw'
    }

    JtypOps = {
        '2':'j','3':'jal'
    }

    i = 0
    for c in content:
        if c == 'DATA SEGMENT':
            break
        temp = [0] * 6
        temp[0] = c[0:6]  # 6 bit op code
        temp[1] = c[6:11]  # 5 bit rs
        temp[2] = c[11:16]  # 5 bit rt
        temp[3] = c[16:21]  # 5 bit rd
        temp[4] = c[21:26]  # 5 bit shamt
        temp[5] = c[26:32]  # 6 bit funct
        textCode = [0] * 4

        #R-type
        if temp[0] == '00000':



            textCode[0] = RtypOps[str(int(temp[5],2))]
            textCode[1] = RegCodes[str(int(temp[3], 2))]
            textCode[2] = RegCodes[str(int(temp[1], 2))]
            textCode[3] = RegCodes[str(int(temp[2], 2))]


            #print textCode
        #J-type
        elif 0 < int(temp[0],2) <= 3:
            textCode[0] = RtypOps[str(int(temp[0], 2))]


        content[i] = textCode
        textCode = 0
        i+=1
    print content







Decoder(Parser())