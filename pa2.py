#! /usr/bin/python

import random as r

#  Programming assignment 1 

#	Submitted by :- Amal Majeed (200415928) 

# Just a function to map character flag to boolean flag
def mp(x):
	if x == 'y':
		return True
	else:
		return False

def PRGA(s,i,j,n):
	'''
		PRGA Algorithm RC4
		input : 256 bit state
	'''
	print("\n\n\t\t\t\t PRGA Logic \t\t\t\t\t\n\n")
	inp = raw_input("\nDo you want to see next state ?(PRESS y - Yes , n - No)  ")
	sequence1 = []
	for x in range(0,n):
		i = (i+1)%256
		j = (j+s[i])%256
		s[i],s[j] = s[j],s[i]
		sequence1.append(s)
		print "Indices swapped : ",i," & ",j,"\n"
		if(mp(inp)):
			print(s)
			print("\n")
			if(x!=n-1):
				inp = raw_input("\nDo you want to see next state ?(PRESS y - Yes , n - No)  ")
	return sequence1,s,i,j

def IPRGA(s,i,j,n):
	print("\n\n\t\t\t\t IPRGA Logic \t\t\t\t\t\n\n")
	inp = raw_input("\nDo you want to see next state ?(PRESS y - Yes , n - No)  ")
	sequence2 = []
	for x in range(0,n):
		s[i],s[j] = s[j],s[i]
		sequence2.append(s)
		print "Indices swapped : ",i," & ",j,"\n"
		j = (j-s[i]+256)%256
		i=(i-1)%256
		if(mp(inp)):
			print(s)
			print("\n")
			if(x!=n-1):
				inp = raw_input("\nDo you want to see next state ?(PRESS y - Yes , n - No)  ")
	return sequence2,s

def diffr(l1,l2):
	print "\nl1:",l1,"\nl2:",l2
	if(l1==l2):
		print True

print("\n\n\t\t\t\t Programming Assignment 1\t\t\t\t\t\n\n")



# Let 'S' be the random array with the initial state after KSA
S = r.sample(range(0,256),256) 
sequence1, sequence2 = [],[]
print("\nInitial Random state 'S' after KSA \n\n")
print(S)
print("\n\n")

n = input("Enter the number of steps to proceed along PRGA : ")
i = input("Enter the current state of pointer 'i' : ")
j = input("Enter the current state of pointer 'j'  : ")

sequence1,S,i,j = PRGA(S,i,j,n)
print("\nRandom state 'S' after PRGA \n\n")
print(S)
print("\n\n")

sequence2,S = IPRGA(S,i,j,n)
print("\nRandom state 'S' after IPRGA \n\n")
print(S)
print("\n\n")

diffr(sequence1,sequence2)

