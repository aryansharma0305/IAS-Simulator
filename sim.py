import sys

memory=["0"*40]*1000   #IAS computer had 1000 memory locations 40 bit wide each

registers={ "MBR":"0"*40,           # Memory Buffer Register
            "MAR":"0"*12,           # Memory Address Register
            "IBR":"0"*20,           # Instruction Buffer Register (RHS)
            "IR" :"0"*8 ,           # Instruction Register (OpCode)
            "PC" :"0"*12,           # Program Counter
            "AC" :"0"*40,           # Accumulator
            "MQ" :"0"*40,           # Multiply/quotient
        }




def store():
    print("Store")
    memory[binaryToDecimal(registers["MAR"])]=registers["AC"]
    
def load():
    print("load")
    registers["AC"]=memory[binaryToDecimal(registers["MAR"])]

def loadMQ():
    print("LOAD MQ")
    registers["AC"]=registers["MQ"]

def jumpL():
    print("JUMPL")
    registers["PC"]=registers["MAR"]
    registers["IBR"]="0"*20

def jumpR():
    print("JUMPR")
    registers["PC"]=registers["MAR"]
    registers["IBR"]=memory[binaryToDecimal(registers["MAR"])][20:40]

def jumpLplus():
    print("JUMPL+")
    if(binaryToDecimalWITHSIGN(registers["AC"])>0):
        registers["PC"]=registers["MAR"]
        registers["IBR"]="0"*20

def jumpRplus():
    print("JUMPR+")
    if(binaryToDecimalWITHSIGN(registers["AC"])>0):        
        registers["PC"]=registers["MAR"]
        registers["IBR"]=memory[binaryToDecimal(registers["MAR"])][20:40]


def add():
    print("ADD")
    registers["AC"]=toBinary40(binaryToDecimalWITHSIGN(registers["AC"])+binaryToDecimal(memory[binaryToDecimal(registers["MAR"])]))
    # print(binaryToDecimalWITHSIGN(registers["AC"]))

def sub():
    print("SUB")
    registers["AC"]=toBinary40(binaryToDecimalWITHSIGN(registers["AC"])-binaryToDecimalWITHSIGN(memory[binaryToDecimal(registers["MAR"])]))
    
def mul():
    print("MUL")
    registers["AC"]=toBinary40(binaryToDecimalWITHSIGN(registers["AC"])*binaryToDecimal(memory[binaryToDecimal(registers["MAR"])]))


def div():
    print("DIV")
    registers["AC"]=toBinary40(binaryToDecimalWITHSIGN(registers["AC"])%binaryToDecimal(memory[binaryToDecimal(registers["MAR"])]))
    registers["MQ"]=toBinary40(binaryToDecimalWITHSIGN(registers["AC"])/binaryToDecimal(memory[binaryToDecimal(registers["MAR"])]))


def lsh():
    print("LSH")
    registers["AC"]=registers["AC"][0]+registers["AC"][2:40]+"0"

def rsh():
    print("RSH")
    registers["AC"]=registers["AC"][0]+"0"+registers["AC"][1:39]

def halt():
    print("HALT")
    sys.exit()
    print("EXITED")

def loadIM():
    print("LOADIM")
    registers["AC"]=toBinary40(binaryToDecimal(registers["MAR"]))

def addIM():
    print("ADDIM")
    registers["AC"]=toBinary40(binaryToDecimalWITHSIGN(registers["AC"])+binaryToDecimal(registers["MAR"]))

def subIM():
    print("SUBIM")
    registers["AC"]=toBinary40(binaryToDecimalWITHSIGN(registers["AC"])-binaryToDecimal(registers["MAR"]))


opDict = {
    "00100001": store,
    "00000001": load,
    "00000100": loadMQ,
    "00001101": jumpL,
    "00001110": jumpR,
    "00001111": jumpLplus,
    "00010000": jumpRplus,
    "00000101": add,
    "00000110": sub,
    "00001011": mul,
    "00001100": div,
    "00001000": lsh,
    "00001001": rsh,
    "11111111": halt,
    "10000000": loadIM,
    "11000000": addIM,
    "11100000": subIM
}



#=============================================================================================================

def updateFile():
    try:
        with open("memory.txt", 'w') as file:
            for content in memory:
                file.write(content+"\n")

        with open("registers.txt", 'w') as file:
            for register, content in registers.items():
                if register in["MBR","IBR"]:
                    file.write(f"{register}: {content[0:8]+" "+content[8:20]+" "+content[20:28]+" "+content[28:40]}\n")
                else:
                    file.write(f"{register}: {content}\n")
    except Exception as e:
        print(f"An error occurred: {e}")


#=============================================================================================================

def loadProgram(filename):
    with open(filename,'r') as file:
        content=file.readlines()
        for i in range(0,len(content)):
           memory[i]=content[i].strip("\n")
    updateFile()

#=============================================================================================================

def toBinary12(int_str):
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

def toBinary40(int_str):
    try:
        number = int(int_str)
    
        if number < -(2**39) or number >= 2**39:
            print("\nError: Number out of range for 40-bit signed representation.\n")
            sys.exit()
        
        if number >= 0:
            sign_bit = '0'
            magnitude = format(number, '039b')
        else:
            sign_bit = '1'
            magnitude = format(abs(number), '039b')
        
        return sign_bit + magnitude
    except ValueError:
        print("\nError: Invalid integer input.\n")
        sys.exit()


    if not all(char in '01' for char in binary_str):
        raise ValueError("Input string must only contain '0' or '1'.")
    return int(binary_str, 2)


#=============================================================================================================

def binaryToDecimalWITHSIGN(binary_str):
    if not all(char in '01' for char in binary_str):
        raise ValueError("Input string must only contain '0' or '1'.")
    if(binary_str[0]=='0'):
        return int(binary_str[1:], 2)
    else:
        return 0-int(binary_str[1:],2)


#=============================================================================================================

def binaryToDecimal(binary_str):
    if not all(char in '01' for char in binary_str):
        raise ValueError("Input string must only contain '0' or '1'.")
    return int(binary_str, 2)
    

#=============================================================================================================

def executeNext():
    #FETCH PHASE
    if registers["IBR"]=="0"*20:                              # INSTRUCTION NOT IN IBR = Fetch new
        registers["MAR"]=registers["PC"]
        registers["MBR"]=memory[binaryToDecimal(registers["MAR"])]
        
        if(registers["MBR"][0:20]=="0"*20):          # LEFT INSTRUCTION NOT PRESENT
            registers["IR"]=registers["MBR"][20:28]
            registers["MAR"]=registers["MBR"][28:40]
            registers["PC"]=toBinary12(binaryToDecimal(registers["PC"])+1)

        else:                                          #LEFT INSTRUCTION PRESENT
            registers["IR"]=registers["MBR"][0:8]
            registers["MAR"]=registers["MBR"][8:20]
            registers["IBR"]=registers["MBR"][20:40]
    
    else :                                     #INSTRUCTION IN IBR
        registers["IR"]=registers["IBR"][0:8]
        registers["MAR"]=registers["IBR"][8:20]
        registers["IBR"]="0"*20
        registers["PC"]=toBinary12(binaryToDecimal(registers["PC"])+1)
    updateFile()


    
    #Execute Phase
    try:
        opDict[registers["IR"]]()
    except SystemExit:
        sys.exit()
    except:
        print("WRONG INSTRUCTION ")
        sys.exit()

    
    finally:
        updateFile()
    
        


#=============================================================================================================

def run():
    
    registers["PC"]=toBinary12(0)
    if(flag=="-a"):
        while True:
            executeNext()
    else:
        while True:
            ch=input("Press 1 to continue , 0 to HALT the program :  ").strip()
            if(ch=='1'):
                executeNext()
            else:
                sys.exit()


#=============================================================================================================


#=============================================================================================================

if __name__=="__main__":
    
    if  len(sys.argv) == 3:
        filename = sys.argv[1]  
        flag=sys.argv[2]
    elif len(sys.argv)==2:
        filename=sys.argv[1]
        flag=None
    else:
        print("\nINVALID SYNTAX!! ,  USE: python sim.py <filename> -<flag>\n")
        sys.exit()
        

    loadProgram(filename)
    updateFile()
    run()