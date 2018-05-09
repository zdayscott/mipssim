import binascii, re, sys

class ZSim:

    def __init__(self, pc=0, instrutions = []):
        self.data = {}
        self.pc = pc
        self.text = instrutions
        self.registers = {
                        '$0' : 0, '$at': 0, '$v0': 0, '$v1': 0,
                        '$a0': 0, '$a1': 0, '$a2': 0, '$a3': 0,
                        '$t0': 0, '$t1': 0, '$t2': 0, '$t3': 0,
                        '$t4': 0, '$t5': 21500, '$t6': 25605, '$t7': 0,
                        '$s0': 268500992, '$s1': 0, '$s2': 0, '$s3': 0,
                        '$s4': 0, '$s5': 0, '$s6': 0, '$s7': 0,
                        '$t8': 0, '$t9': 0, '$k0': 0, '$k1': 0,
                        '$gp': 0, '$sp': 0, '$s8': 0, '$ra': 0
                         }

        self.functLookUp = {
                        'add':'+',  'addi':'+',  'sub':'-',  'subi':'-',
                        'and':'&',  'andi':'&',   'or':'|',   'ori':'|',
                        'sll':'<<', 'sllv':'<<', 'srl':'>>', 'srlv':'>>',
                        'div':'/',   'mul':'*',  'xor':'^',  'xori':'^'
                           }
        itr = 0
        for i in instrutions:
            address = bin(int('400000', 16) + itr*4)
            print address
            self.data[address] = i
            print self.data[address]
            itr += 1

            self.Execute(i)
            self.pc += 4



    def GetRegister(self, reg):
        try: return self.registers[reg]
        except: print "You done' broke it!"

        #def RunLine/Lines

    def Execute(self, line):
        if re.compile('^.*:').match(line[0]): return
        elif re.compile('^syscall').match(line[0]): self.Syscall()
        elif re.compile('^(beq|bne)').match(line[0]):self.Branch(line)
        elif re.compile('(j|b|jr|jal)').match(line[0]): self.Jump(line)
        elif re.compile('^(lw|sw)').match(line[0]): self.LoadStore(line)
        elif re.compile('^(slt|slti)').match(line[0]): self.SetLessThan(line)
        elif re.compile('^move').match(line[0]): self.Move(line)
        elif re.compile('^[a-zA-Z]{2,4}').match(line[0]): self.LogicArith(line)


    def LogicArith(self,line):
        print "LogicArith: " + line[0]
        funct = self.functLookUp[line[0]]
        reg1, reg2 = line[1], line[2]
        if 'i' in line[0] or line[0] in ('sll','srl'):
            self.registers[reg1] = eval(reg2 + funct + line[3])
        else:
            reg3 = line[3]
            self.registers[reg1] = eval(str(self.GetRegister(reg2))+funct+str(self.GetRegister(reg3)))
            print reg1 + ' = ' + reg2+funct+reg3
            print str(self.GetRegister(reg1)) + ' = ' + str(self.GetRegister(reg2))+funct+str(self.GetRegister(reg3))

    def Syscall(self):
        print "syscall: " + line[0]

    def Branch(self,line):
        print "Branch: " + line[0]
        print self.pc
        reg1, reg2 = line[1], line[2]
        if self.registers[reg1] == self.registers[reg2]:
            if line[0] == 'beq':
                self.pc = self.pc + int(line[3])*4
        else:
            if line[0] == 'bne':
                self.pc = self.pc + int(line[3])*4

        print self.pc



    def Jump(self, line):
        '''print "Jump: " + line[0]
        print bin(int(line[1]))
        print str(bin(int(line[1])))[:2].zfill(26)
        address = bin(line[1])
'''
        pcRollover = str(self.pc).zfill(32)[:4]

        if line[0] == 'jr':
            reg = line[1]
            self.pc = self.registers(reg)
        elif line[0] == 'jal':
            self.registers['$ra'] = self.pc + 4
            address = pcRollover + str(bin(line[1])[:2].zfill(26))+ '0'
            self.pc = address
        else:
            address = pcRollover + str(bin(line[1])[:2].zfill(26))+ '0'
            self.pc = address





    def LoadStore(self,line):
        print "LoadStore: " + line[0]

    def SetLessThan(self,line):
        print "SetLessThan: " + line[0]
        if line[0] == 'slt':
            reg1, reg2, reg3 = line[1], line[2], line[3]
            if self.GetRegister(reg2) < self.GetRegister(reg3):
                self.registers[reg1] = 1
            else:
                self.registers[reg1] = 0
        elif line[0] == 'slti':
            reg1, reg2 = line[1], line[2]
            immidiate = line[3]
            if self.GetRegister(reg2) < immidiate:
                self.registers[reg1] = 1
            else:
                self.registers[reg1] = 0

    def Move(self, line):
        print "Move: " + line[0]
        reg1, reg2 = line[1], line[2]
        self.registers[reg1] = self.GetRegister(reg2)




###------------------------------------------------PARSER_DECODER----------------------------------------------------###


# Parsing
def Parser():
    with open('Test.txt', 'r') as f:
        content = f.readlines()

        content = [x.strip() for x in content]

        #print content

        i = 0
        for c in content:
            if (c == 'DATA SEGMENT'):
                del content[i:len(content)]
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

        textCode = [0] * 4

        #R-type
        if temp[0] == '000000':
            temp[1] = c[6:11]  # 5 bit rs
            temp[2] = c[11:16]  # 5 bit rt
            temp[3] = c[16:21]  # 5 bit rd
            temp[4] = c[21:26]  # 5 bit shamt
            temp[5] = c[26:32]  # 6 bit funct


            textCode[0] = RtypOps[str(int(temp[5],2))]
            textCode[1] = RegCodes[str(int(temp[3], 2))]
            textCode[2] = RegCodes[str(int(temp[1], 2))]
            textCode[3] = RegCodes[str(int(temp[2], 2))]


            #print textCode
        #J-type
        elif 0 < int(temp[0],2) <= 3:
            textCode[0] = JtypOps[str(int(temp[0], 2))]
            textCode[1] = str(int(c[6:32], 2))
            textCode[2:] = []

        #I-type
        elif 3 < int(temp[0],2) <= 46:
            temp[1] = c[6:11]
            temp[2] = c[11:16]
            temp[3] = c[16:32]
            textCode[0] = ItypOps[str(int(temp[0], 2))]
            textCode[1] = RegCodes[str(int(temp[2], 2))]
            textCode[2] = RegCodes[str(int(temp[1], 2))]
            textCode[3] = str(int(temp[3], 2))



        content[i] = textCode
        textCode = 0
        i+=1
    #print content

    i = 0
    '''
        for c in content:
        content[i] = ' '.join(c)
        i += 1
    '''

    print content
    return content



s = ZSim(0,Decoder(Parser()))