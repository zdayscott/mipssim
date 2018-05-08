

import re, sys

class ZSim:

    def __init__(self, mem = 4000, pc=0, instrutions = []):
        self.data = [0 for x in range(mem)]
        self.pc = pc
        self.text = instrutions
        self.registers = {
                        '$0' : 0, '$at': 0, '$v0': 0, '$v1': 0,
                        '$a0': 0, '$a1': 0, '$a2': 0, '$a3': 0,
                        '$t0': 0, '$t1': 0, '$t2': 0, '$t3': 0,
                        '$t4': 0, '$t5': 0, '$t6': 0, '$t7': 0,
                        '$s0': 0, '$s1': 0, '$s2': 0, '$s3': 0,
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

    def GetRegister(self, reg):
        try: return self.registers[reg]
        except: print "You done' broke it!"

        #def RunLine/Lines

    def execute(self, line):
        if re.compile('^.*:').match(line[0]): return
        elif re.compile('^syscall').match(line[0]): self.Syscall()
        elif re.compile('^(beq|bne)').match(line[0]):self.Branch(line)
        elif re.compile('(j|b|jr|jal)').match(line[0]): self.Jump(line)
        elif re.compile('^(lw|sw)').match(line[0]): self.LoadStore(line)
        elif re.compile('^(slt|slti)').match(line[0]): self.SetLessThan(line)
        elif re.compile('^move').match(line[0]): self.Move(line)
        elif re.compile('^[a-zA-Z]{2,4}').match(line[0]): self.LogicArith(line)


    def LogicArith(self,line):
        instruction = re.compile()
