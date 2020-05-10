from math import log2,ceil
from random import randint

'''
Return Type- String
This function takes string as an arguement and perform arithmetic right shift operation on the given input string.
'''
def shift_right(s):
	ans=s[0]
	for i in range(1,len(s)):
		ans+=s[i-1]
	return ans

'''
Return Type- String
This function takes 2 integer as an arguement, where first is number which will be converted to binary and second is
number of bits that binary string should be. If the number is negative, it will return twos complement of that number.
'''
def binary(num,n):
	b=bin(abs(num))[2:]
	b='0'*(n-len(b))+b 										#adding zeroes if binary is not a n-bit string 
	if(num<0):
		return twos_complement(b)							#if negative, return two's complement
	else:
		return b

'''
Return Type- String
This function takes string as an arguement and converts the given binary string to its twos complement form. This is 
needed only in the case of negative numbers.
'''
def twos_complement(b):
	n=len(b)
	for i in range(n):
		b=b[:i]+str(int(b[i])^1)+b[i+1:]					#first converting it in One's complement 
	a='0'*(n-1)+'1'											
	b=add_binary(a,b)										#adding 1 to it to complete the process
	return b

'''
Return Type- String
This function takes 2 strings as an arguement and perform binary addition of strings and returns the answer. In case of
overflow, it ignores the extra bits present on the left side.
'''
def add_binary(s1,s2): 
	result='' 
	carry=0
	for i in range(len(s1)-1,-1,-1): 
		r=carry 
		if(s1[i]=='1'):
			r+=1
		if(s2[i]=='1'):
			r+=1
		result=str(r%2)+result
		if(r<2):
			carry=0
		else:
			carry=1
	if(carry!=0): 
		result='1'+result
	if(len(result)>len(s1)):
		diff=len(result)-len(s1)
		result=result[diff:] 
	return result

'''
Return Type- (String, String)
This function takes two integers as an arguement and perform booth's multiplucation and returns decimal and binary form of
the answer obtained.
'''
def multiplication(n1,n2):
	max_len=11
	n=max_len
	if(abs(n1)>abs(n2)):
		multiplicand=binary(n1,n)
		_multiplicand=binary(-n1,n)
		multiplier=binary(n2,n)

	else:
		multiplicand=binary(n2,n)
		_multiplicand=binary(-n2,n)
		multiplier=binary(n1,n)
	acc='0'*max_len
	q0='0'
	while n!=0:
		if(multiplier[-1]+q0=='01'):
			acc=add_binary(acc,multiplicand)
		elif(multiplier[-1]+q0=='10'):
			acc=add_binary(acc,_multiplicand)
		a=shift_right(acc+multiplier+q0)
		acc=a[:max_len]
		multiplier=a[max_len:max_len*2]
		q0=a[max_len*2]
		n-=1
	ans=acc+multiplier
	if(acc[0]=='1'):
		dec=-int(twos_complement(ans),2)
	else:
		dec=int(ans,2)
	return str(dec),ans

def calc(quotient): # Function to calculate the final quotient
	p="" 
	q=""
	for i in range(len(quotient)):
		if quotient[i]==1:
			p+="1"
			q+="0"
		else:
			p+="0"
			q+="1"
	return ((int(p,2)-int(q,2)))

def calculate(numerator,denominator): # Function to divide two numbers
	num = numerator
	deno = denominator
	n = len(bin(num)[2:]) # To convert the numerator into its binary form
	rem = num # Partial Remainder
	quotient = [0]*n # To store the partial quotient
	deno = deno * (2**n) # Left shift the denominator
	for i in range(n-1,-1,-1): # For loop equal to number of bits
		if rem>=0:
			quotient[n-i-1]=1
			rem=2*rem-deno
		else:
			quotient[n-i-1]=-1
			rem=2*rem+deno
	ans_quotient=calc(quotient) # To find the actual quotient
	ans_remainder = rem//(2**n)
	if ans_remainder<0:
		ans_quotient=ans_quotient-1
		ans_remainder=ans_remainder+denominator
	return ans_quotient,ans_remainder
	


file1=open('output_multiply.txt','w+')							#opening file in write mode
i=1
while(True):
	print("Enter two numbers-")
	a=int(input())												#randomly genearting two values to perform multiplication on them
	b=int(input())
	dec,_bin=multiplication(a,b)
	print("Result of Multiplication- "+dec)
	if(int(dec)!=a*b):
		print(a,b,a*b,dec)
		print("ERROR")
	file1.write("Input #"+str(i)+'\n')							#writing and formatting of answer in file.
	file1.write("a="+str(a)+'\n')
	file1.write("b="+str(b)+'\n')
	file1.write("Result of Multiplication:"+'\n')
	file1.write("In decimal: "+str(dec)+'\n')
	file1.write("In binary: "+str(_bin)+'\n\n\n')
	i+=1
	print("Do you want to enter more case-")
	s=input()
	if(s=='no'):
		break
file1.close()

#main program
flag = "yes"
file2=open('output_divide.txt','w+')
i=1
while flag=="yes":
	numerator = int(input("Enter the dividend - "))
	denominator = int(input("Enter the divisor - "))
	file2.write("Input #"+str(i)+'\n')							#writing and formatting of answer in file.
	file2.write("numerator="+str(numerator)+'\n')
	file2.write("denominator="+str(denominator)+'\n')
	file2.write("Result of Division:"+'\n')
	if numerator==0:
		print ("Quotient is - ",0)
		print ("Remainder is - ",0)
		file2.write("Quotient In decimal: "+'0'+'\n')
		file2.write("Quotient In binary: "+'0'+'\n')
		file2.write("Remainder In decimal: "+'0'+'\n')
		file2.write("Remainder In binary: "+'0'+'\n\n\n')
	elif denominator==0:
		print ("Division by 0 not allowed!")
		file2.write("Division by 0 not allowed!\n\n\n")
	else:
		if (denominator<0 and numerator<0):
			ans_quotient,ans_remainder=calculate(-numerator,-denominator)
			ans_remainder=-ans_remainder
		elif denominator<0:
			ans_quotient,ans_remainder=calculate(-numerator,-denominator)
		else:
			ans_quotient,ans_remainder=calculate(numerator,denominator)
		print ("Quotient is - ",ans_quotient,"Binary form -",binary(ans_quotient,11))
		print ("Remainder is - ",ans_remainder,"Binary form - ",binary(ans_remainder,11))
		file2.write("Quotient In decimal: "+str(ans_quotient)+'\n')
		file2.write("Quotient In binary: "+binary(ans_quotient,11)+'\n')
		file2.write("Remainder In decimal: "+str(ans_remainder)+'\n')
		file2.write("Remainder In binary: "+binary(ans_remainder,11)+'\n\n\n')
	flag = input("Do you want to enter another number? (yes/no) - ")
file2.close()

#testing (takes 1-10 seconds)
for i in range(-500,500): # i acts as dividend
	for j in range(-500,500): # j acts as dividend
		if j!=0: # To remove error during testing
			numerator=i 
			denominator=j
			quotient=i//j # Actual Quotient
			remainder=i%j # Actual Remainder
			a=i
			b=j
			dec,_bin=multiplication(a,b) # Calculated answer for multiplication
			if(a*b!=int(dec)): # If actual answer is not equal to calculated answer
				print("Failed for multiplication of "+str(a)+" "+str(b))
				exit()
			if (denominator<0 and numerator<0):
				ans_quotient,ans_remainder=calculate(-numerator,-denominator)
				ans_remainder=-ans_remainder
			elif denominator<0:
				ans_quotient,ans_remainder=calculate(-numerator,-denominator)
				ans_remainder=-ans_remainder
			else:
				ans_quotient,ans_remainder=calculate(numerator,denominator)
			if (quotient!=ans_quotient or remainder!=ans_remainder): # If actual quotient and remainder are not equal to calculated quotient and remainder
				print ("Failed on numerator -",i,"and denominator - ",j)
				print (ans_quotient,quotient,ans_remainder,remainder)
				exit()
print ("Passed")