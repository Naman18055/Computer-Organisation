import sys


# TO CHECK IF LINE IS COMMENTED

def line_commented(line):
	if line[0:2]=="//" or line[0:2]=="/*" or line[0:1]=="#":
		return True
	return False

# TO REMOVE THE COMMENTS IN A LINE

def remove_comments(line):
	if line.find("//")==-1 and line.find("/*")==-1 and line.find("#")==-1:
		return line
	else:
		temp=line.split()
		temp.pop()
		new_line=""
		for i in temp:
			new_line+=i
		return new_line

# TO CHECK IF INSTRUCTION CONTAINS A NEW LABEL

def contains_label(line,all_opcodes):
	if line.split()[0] in all_opcodes:
		if line.split()[0][0:2]=="BR":
			return 1
	if len(line.split())>1:
		if line.split()[1] in all_opcodes:
			if line.split()[0][0:2]=="BR":
				return 2
	return False


# TO CALCULATE LOCATION OF THE LABEL

def offset_of_label(line,all_opcodes):
	if line.split()[0] not in all_opcodes:
		if line.split()[0][-1]==":":
			return True
	return False

# TO CHECK IF INSTRUCTION CONTAINS A OPCODE

def contains_opcode(line,all_opcodes):
	if line.split()[0] in all_opcodes:
		return 1
	if line.split()[1] in all_opcodes:
		return 2 
	return False

# TO CHECK IF INSTRUCTION CONTAINS A VARIABLE

def contains_variable(line,all_opcodes):
	length = len(line.split())
	if line.split()[0] in all_opcodes:
		if line.split()[0][0:2]!="BR" and length>1 and ord(line.split()[1][0])>=65:
			return 1
	if length>1:
		if line.split()[1] in all_opcodes:
			if line.split()[1][0:2]!="BR" and length>2 and ord(line.split()[2][0])>=65:
				return 2
	return False


# TO CHECK IF ALL LABELS HAVE A LOCATION

def error_in_symtable(sym_table):
	for labels in sym_table:
		if sym_table[labels][1]==-1:
			return True
	return False

# TO CHECK IF ALL OPCODES HAVE CORRECT NUMBER OF OPCODES

def error_in_optable(op_table,all_opcodes):
	for i in op_table:
		if i[2]=="" and i[0]!="CLA" and i[0]!="STP":
			return True
	return False




# MAIN PROGRAM --------------------------------------------------------------------

# INITIALISATION

all_opcodes = {}
inputs = []
op_table = []
sym_table = {}
literal_table = {}
line_number = 0
address_alloted = 255
length_of_input = 0
end_statement = 0
system_exit = 0

# READ OPCODES

f = open("opcode.txt","r")
line = f.readline()
while (line):
	temp = line.split()
	all_opcodes[temp[1]] = temp[0]
	line = f.readline()
	length_of_input+=1
f.close()

# READ INPUTS 

f = open("input.txt","r")
line = f.readline()
while (line):
	if (not line_commented(line)):
		inputs.append(remove_comments(line.strip()))
	line = f.readline()
f.close()

# START AND END IN CODE

if "START" not in inputs[0]:
	print ("START NOT FOUND")
	system_exit = 1
	#sys.exit(0)

# BUILD SYMBOL TABLE AND OPCODE TABLE

for lines in inputs:
	try:
		if ("START" in lines):
			continue
		line_number+=1

		if (contains_label(lines,all_opcodes)): # IF A LABEL IS USED FOR THE FIRST TIME IN THE INSTRUCTION
			line = lines.split()
			location = contains_label(lines,all_opcodes)
			if line[location] not in sym_table:
				sym_table[line[location]] = ["LABEL",-1]

		if (offset_of_label(lines,all_opcodes)): # IF A LABEL IS DEFINED IN THE INSTRUCTION
			line = lines.split()
			try:
				if (sym_table[line[0][0:-1]][1]!=-1): # IF A LABEL IS DEFINED MORE THAN ONCE.
					print ("ERROR!!! LABEL HAS ALREADY BEEN DEFINED")
					print ("PLEASE WRITE THE CORRECT LABEL OR REMOVE THE LABEL")
					system_exit = 1
					#sys.exit(0)
				else:
					sym_table[line[0][0:-1]][1] = bin(line_number)[2:]
			except:
				sym_table[line[0][0:-1]] = ["LABEL",bin(line_number)[2:]]

		if (contains_opcode(lines,all_opcodes)):
			location = contains_opcode(lines,all_opcodes)-1
			temp = [lines.split()[location]]
			temp.append(all_opcodes[temp[0]])
			if len(lines.split())>location+1:
				temp.append(lines.split()[location+1])
				try:
					temp_flag=0
					if lines.split()[location+2] and temp[0]!='DIV':
						print ("ERROR!!!")
						print("TOO MANY OPCODES WERE PROVIDED")
						temp_flag=1
						#exit(0)
				except:
					if temp_flag==1:
						system_exit=1
						#exit(0)
			else:
				temp.append("")
			op_table.append(temp)
		else: # IF WRONG OPCODE IS PROVIDED
			print ("ERROR!!! OPCODE NOT FOUND!")
			print ("PLEASE WRITE THE CORRECT OPCODE")
			system_exit = 1
			#sys.exit(0)
		if "STP" in lines or "END" in lines:
			end_statement=1
			break
	except:
		if system_exit == 0:
			print ("ERROR!!! ON LINE NUMBER ",line_number)
			print ("LINE : ",lines)


# IF END STATEMENT WAS PROVIDED

if end_statement==0:
	print ("ERROR!!!")
	print ("END STATEMENT WAS NOT PROVIDED")
	system_exit = 1
	#sys.exit(0)

# TO ALLOT ADDRESSES TO THE VARIABLES

for op in op_table:
	flag=0
	if op[2]!="" and op[2].isalpha() and op[0]!="INP":
		for symbol in sym_table:
			if op[2]==symbol:
				flag=1
				break
		if flag==0:
			print ("ERROR!!!")
			print ("SYMBOL NOT DEFINED")
			system_exit = 1
			#sys.exit(0)
	elif op[2]!="" and op[2].isalpha() and op[0]=="INP":
		sym_table[op[2]]=["VARIABLE",bin(address_alloted)[2:]]
		address_alloted-=1
		flag=1


# CHECK IF THERE IS ERROR IN TABLES OR PRINT THE TABLES

if (error_in_symtable(sym_table)): # A SYMBOL HAS BEEN USED BUT NOT DEFINED
	print ("THE ASSEMBLY CODE IS INCOMPLETE")
	print ("LOCATION OF ALL LABELS WAS NOT FOUND")
	system_exit = 1
	exit(0)
elif (error_in_optable(op_table,all_opcodes)): # NO OPERAND WAS PROVIDED FOR AN OPCODE
	print ("ERROR!!!")
	print ("NO OPERAND WAS PROVIDED FOR AN OPCODE")
	system_exit = 1
	exit(0)
else:
	# PRINT TABLES
	print ("SYMBOL TABLE -----------")
	for i in sym_table:
		print ("{0:5}{1:12}{2:2}".format(i,sym_table[i][0],sym_table[i][1]))
	print ("OPCODE TABLE -----------")
	print ("{0:10}{1:10}{2:10}".format("OPCODE","CODE","OPERAND"))
	for i in range(len(op_table)):
		print ("{0:10}{1:10}{2:10}".format(op_table[i][0],op_table[i][1],op_table[i][2]))


if system_exit==1:
	exit(0)

LC=0
VIRTUALMEM=[None]*(2**8)#Allocated mem that can be used by program
def is_psuedo_instr(line):
	if line.split()[0] in ("STP","START"):
		return True
	else:
		return False
def get_opcode(line):
	return all_opcodes[line.split()[0]]
def eval_line(line):
	#Returns object code for the input line
	if ":" in line: ###Definitions

		return eval_line(line.split(":")[1])

	if(is_psuedo_instr(line)):##Checking 
		# print("Is a psuedo instr")
		return eval_psuedo_instr(line)
	else:
		if is_MRI(line):
			# print("is an MRI")
			return eval_MRI(line)
		else:
			# print("is an NON MRI instr")
			return get_opcode(line.split()[0])+(8*"0")


def is_MRI(line):
	# print(len(line),line.split())
	# return line.split()[0]==line
	return len(line)!=3 ###For 3 length label	

def search_symtable(label):
	#print(label)
	try:
		# print("Found", bin(sym_table[label][1]))
		return "0"*(8-len(sym_table[label][1]))+sym_table[label][1]
		
	except:
		return None
def eval_MRI(line):
	#Direct Addressing covered ie : NO bit reserved for addressing mode
	object_code=get_opcode(line)#Setting the first four bits for opcode
	# print(line)
	label_address=search_symtable(line.split()[1])

	if (label_address!=None):
		object_code+=str(label_address)
	else:
		binary=bin(int(line.split()[1]))
		#print(binary)
		if len(binary)>10:
			print("ERRRORR!! Value larger than 2**8 not acceptable for this operand")
		else:
			x=(8-(len(binary)-2))*"0"
			binary=x+binary[2:]
			object_code+=binary
	# print(object_code)
	return object_code






def eval_psuedo_instr(line):
	if line.split()[0]=="START":
		setLC(int(line.split()[1]))
		return
	elif line=="STP":
		print("End of program reached")
		return




def setLC(a):
	LC=a

#Main read starts from here
LC=0
#print(sym_table)
for line in inputs:
	# print("########")
	# print(line)
	VIRTUALMEM[LC]=eval_line(line)
	# print(eval_line(line))
	LC+=1
MEM=0

# WRITE MACHINE CODE INTO FILE AND PRINT THE MACHINE CODE

f = open("machinecode.txt","w")
print ("MACHINE CODE -----------")
for object_code in VIRTUALMEM:
	if object_code==None:
		continue
	memoryAddress=bin(MEM)[2:]
	memoryAddress="0"*(4-len(memoryAddress))+memoryAddress
	f.write(str(memoryAddress)+str(object_code)+"\n")
	print(memoryAddress,end="")
	print(object_code)
	MEM+=1
f.close()



