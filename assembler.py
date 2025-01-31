import sys


opDict = {
    "STOR": "00100001",        # Transfers content of accumulator to memory location X
    "LOAD": "00000001",        # Transfers content of memory location X to the accumulator
    "LOADMQ": "00000100",      # Transfers the content of the MQ register to the accumulator
    "JUMPL": "00001101",       # Unconditionally jump to the instruction at the left half of memory location X
    "JUMPR": "00001110",       # Unconditionally jump to the instruction at the right half of memory location X
    "JUMPL+": "00001111",      # Conditionally jump to the instruction at the left half of memory location X if AC >= 0
    "JUMPR+": "00010000",      # Conditionally jump to the instruction at the right half of memory location X if AC >= 0
    "ADD": "00000101",         # Add the contents of memory location X to the accumulator (AC); put the result in AC
    "SUB": "00000110",         # Subtract the contents of memory location X from the accumulator (AC); put the result in AC
    "MUL": "00001011",         # Multiply the contents of memory location X by the MQ register
    "DIV": "00001100",         # Divide the accumulator (AC) by memory location X
    "LSH": "00001000",         # Multiply the accumulator (AC) by 2, shifting left one bit position
    "RSH": "00001001",         # Divide the accumulator (AC) by 2, shifting right one bit position
    "HALT": "11111111",        # Stops the program                                          
    "LDIM": "10000000",        # Load an immediate value X directly into the accumulator              #CUSTOM ISA
    "ADIM": "11000000",        # Add an immediate value X with the content in the accumulator         #CUSTOM ISA
    "SBIM": "11100000"         # Subtract an immediate value X from the content in the accumulator    #CUSTOM ISA
}


#=============================================================================================================

if not len(sys.argv) == 3:
    print("\nINVALID SYNTAX!! ,  USE: python assembler.py <input filename> <output filename> \n")
    sys.exit()
    
filename = sys.argv[1]  
outFilename=sys.argv[2]

#=============================================================================================================

def toBinary(int_str):
    try:
        number = int(int_str)
        if number < 0 or number > 4095:
            print( "\nError: Number out of range for 12-bit representation.\n")
            sys.exit()
        return format(number, '012b')
    except ValueError:
        print ("\nError: Invalid integer input.\n")
        sys.exit()


#=============================================================================================================

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read().strip()
        return content.split('\n')
    except FileNotFoundError:
        print(f"\nError: The file '{file_path}' was not found.\n")
        sys.exit()
    except Exception as e:
        print(f"\nError\n")
        sys.exit()


#=============================================================================================================


fileContent=read_file(filename)

code=""
printCode=""

for line in fileContent:
    instr=line.split(",")
    if(len(instr)==0 or not(instr[0]) ) : 
        continue
    if(len(instr)>2):   
        print("\nThere can only be 1 or 2 instructions per line")
        sys.exit()

    if(len(instr)==2):
        if(not instr[0] or not instr[1]):
            print('\nSyntax Error at -> ',instr,"\n")
            sys.exit()
        LHS=instr[0].strip()
        RHS=instr[1].strip()
        opcode=""
        try:
            opcode=opDict[LHS.split()[0].strip()]
        except:
            print("\n Invalid Operation \n")
            sys.exit()
       
        code+=opcode
        printCode+="\033[31m"+opcode
        opcodesForWhichAddressNotRequired=['00000100','00001000','00001001','11111111']
        if(opcode in opcodesForWhichAddressNotRequired):
            code+='000000000000'
            printCode+="\033[93m"+'000000000000'
        else: 
            code+=toBinary(LHS.split()[1].strip()[2:-1])
            printCode+="\033[93m"+toBinary(LHS.split()[1].strip()[2:-1])

        


        try:
            opcode=opDict[RHS.split()[0].strip()]
        except:
            print("\n Invalid Operation \n")
            sys.exit()
       
        code+=opcode
        printCode+="\033[31m"+opcode

        if(opcode in opcodesForWhichAddressNotRequired):
            printCode+="\033[93m"+'000000000000'
            code+='000000000000'
        else: 
            code+=toBinary(RHS.split()[1].strip()[2:-1])
            
            printCode+="\033[93m"+toBinary(RHS.split()[1].strip()[2:-1])
        
        printCode+="\n"
        code+="\n"

    
    else:
        RHS=instr[0].strip()
        if(not RHS):
            print('\nSyntax Error at -> ',instr,"\n")
            sys.exit()
        
        code+='00000000000000000000'
        printCode+="\033[93m"+'00000000000000000000'

        try:
            opcode=opDict[RHS.split()[0].strip()]
        except:
            print("\n Invalid Operation \n")
            sys.exit()
       
        code+=opcode

        if(opcode in opcodesForWhichAddressNotRequired):
            code+='000000000000'
            
            printCode+="\033[93m"+'000000000000'
        else: 
            code+=toBinary(RHS.split()[1].strip()[2:-1])
            
            printCode+="\033[93m"+toBinary(RHS.split()[1].strip()[2:-1])
        
        printCode+='\n'
        
        code+="\n"
       

#=============================================================================================================
        


code=code.strip()

def generateOutPutFile():
    with open(outFilename, 'w') as file:
        file.write(code)


generateOutPutFile()

print(printCode,"\033[0m")




#=============================================================================================================